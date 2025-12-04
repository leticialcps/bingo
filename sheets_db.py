"""
Módulo para integração com Google Sheets como banco de dados.
Substitui os arquivos JSON por planilhas do Google Sheets.

Formatos suportados:
1. Key-Value: Coluna A = "key", Coluna B = "value" (formato JSON serializado)
2. Tabular: Primeira linha = nomes das colunas, dados nas linhas seguintes
"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# Escopos necessários para acessar Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_google_sheets_client():
    """
    Conecta ao Google Sheets usando credenciais do Streamlit secrets.
    As credenciais devem estar em .streamlit/secrets.toml
    """
    try:
        # Tenta obter credenciais do Streamlit secrets
        credentials_dict = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        return gspread.authorize(credentials)
    except KeyError:
        # Secrets não configurados - modo silencioso
        return None
    except Exception as e:
        # Outros erros - modo silencioso também
        return None

def get_spreadsheet():
    """
    Retorna a planilha do Bingo ou None se não conseguir conectar.
    """
    client = get_google_sheets_client()
    if client is None:
        return None
    
    try:
        # Tenta abrir a planilha pelo nome
        sheet_name = st.secrets.get("sheet_name", "dados_amigosecreto_idosos")
        try:
            spreadsheet = client.open(sheet_name)
            return spreadsheet
        except gspread.SpreadsheetNotFound:
            st.error(f"❌ Planilha '{sheet_name}' não encontrada no Google Sheets.")
            st.info(f"Por favor, crie uma planilha chamada '{sheet_name}' e compartilhe com: {st.secrets['gcp_service_account']['client_email']}")
            return None
        
    except Exception as e:
        st.error(f"Erro ao acessar planilha: {e}")
        return None

def load_sheet_data(sheet_name):
    """
    Carrega dados de uma aba específica da planilha.
    Retorna um dicionário (equivalente ao JSON).
    Se a aba estiver vazia, sincroniza com dados do JSON local.
    
    Suporta dois formatos:
    1. Formato key-value: coluna A = chave, coluna B = valor JSON
    2. Formato tabular: primeira linha = headers, dados nas linhas seguintes
    """
    spreadsheet = get_spreadsheet()
    if spreadsheet is None:
        # Fallback para JSON local
        return load_json_fallback(f"{sheet_name}.json")
    
    try:
        # Tenta abrir a aba, ou cria se não existir
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            # Inicializa com headers
            worksheet.update('A1:B1', [['key', 'value']])
            
            # Tenta sincronizar com JSON local na primeira execução
            local_data = load_json_fallback(f"{sheet_name}.json")
            if local_data:
                save_sheet_data(sheet_name, local_data)
                return local_data
            return {}
        
        # Lê todos os valores da planilha
        all_values = worksheet.get_all_values()
        
        # Se estiver vazia, sincroniza com JSON local
        if not all_values or len(all_values) <= 1:
            local_data = load_json_fallback(f"{sheet_name}.json")
            if local_data:
                save_sheet_data(sheet_name, local_data)
                return local_data
            return {}
        
        # Detecta o formato da planilha
        headers = all_values[0] if all_values else []
        
        # Formato apostas: ID | Personagem | Pessoa
        if sheet_name == "apostas" and len(headers) >= 3 and headers[0].upper() == 'ID':
            result = {}
            for row in all_values[1:]:
                if len(row) >= 3 and row[0] and row[1]:
                    user_id = row[0]
                    personagem = row[1]
                    pessoa = row[2] if len(row) > 2 else ''
                    
                    if user_id not in result:
                        result[user_id] = {}
                    result[user_id][personagem] = pessoa
            return result
        
        # Formato codigos_identidade: ID | Responsável
        elif sheet_name == "codigos_identidade" and len(headers) >= 2 and headers[0].upper() == 'ID':
            result = {}
            for row in all_values[1:]:
                if len(row) >= 2 and row[0]:
                    user_id = row[0]
                    responsavel = row[1] if len(row) > 1 else ''
                    if responsavel:
                        result[user_id] = responsavel
            return result
        
        # Formato identidades: Personagem | Nome Real | URL da Foto
        elif sheet_name == "identidades" and len(headers) >= 2 and headers[0].lower() in ['personagem']:
            result = {}
            for row in all_values[1:]:
                if len(row) >= 1 and row[0]:
                    personagem = row[0]
                    result[personagem] = {
                        "nome": row[1] if len(row) > 1 else '',
                        "foto": row[2] if len(row) > 2 else ''
                    }
            return result
        
        # Formato revelacoes: Personagem | Pessoa
        elif sheet_name == "revelacoes" and len(headers) >= 2 and headers[0].lower() in ['personagem']:
            result = {}
            for row in all_values[1:]:
                if len(row) >= 2 and row[0]:
                    personagem = row[0]
                    pessoa = row[1] if len(row) > 1 else 'Ainda não revelado'
                    result[personagem] = pessoa
            return result
        
        # Formato key-value (usado pelo nosso sistema)
        elif len(headers) >= 2 and headers[0].lower() in ['key', 'chave']:
            result = {}
            for row in all_values[1:]:
                if len(row) >= 2:
                    key = row[0]
                    value_str = row[1] if len(row) > 1 else ''
                    if key:
                        try:
                            # Tenta fazer parse do JSON se o valor for um objeto/array
                            result[key] = json.loads(value_str) if value_str else ''
                        except json.JSONDecodeError:
                            result[key] = value_str
            return result
        
        # Formato tabular genérico - tenta converter para estrutura apropriada
        # Para participantes.json: espera colunas "personagens" e "nomes_reais"
        else:
            # Se tem colunas específicas, monta estrutura adequada
            if headers:
                # Verifica se é formato de lista simples (uma coluna)
                if len(headers) == 1:
                    return {headers[0]: [row[0] for row in all_values[1:] if row]}
                
                # Formato com múltiplas colunas - agrupa por coluna
                result = {}
                for col_idx, header in enumerate(headers):
                    if header:  # Ignora headers vazios
                        result[header] = [row[col_idx] if col_idx < len(row) else '' 
                                         for row in all_values[1:] if row]
                        # Remove valores vazios do final
                        while result[header] and not result[header][-1]:
                            result[header].pop()
                return result
            
            return {}
            
    except Exception as e:
        # Erro silencioso - usa fallback JSON
        return load_json_fallback(f"{sheet_name}.json")

def save_sheet_data(sheet_name, data):
    """
    Salva dados em uma aba específica da planilha.
    data deve ser um dicionário (equivalente ao JSON).
    
    Formatos suportados:
    - apostas: {user_id: {personagem: pessoa}} -> ID | Personagem | Pessoa
    - codigos_identidade: {user_id: responsavel} -> ID | Responsável
    - identidades: {personagem: {nome, foto}} -> Personagem | Nome Real | URL da Foto
    - revelacoes: {personagem: pessoa} -> Personagem | Pessoa
    - participantes: {personagens: [], nomes_reais: []} -> formato colunar
    """
    spreadsheet = get_spreadsheet()
    if spreadsheet is None:
        # Fallback para JSON local
        return save_json_fallback(f"{sheet_name}.json", data)
    
    try:
        # Tenta abrir a aba, ou cria se não existir
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
        
        # Limpa a aba
        worksheet.clear()
        
        # Formato apostas: ID | Personagem | Pessoa
        if sheet_name == "apostas" and isinstance(data, dict):
            rows = [['ID', 'Personagem', 'Pessoa']]
            for user_id, palpites in data.items():
                if isinstance(palpites, dict):
                    for personagem, pessoa in palpites.items():
                        if pessoa:
                            rows.append([str(user_id), str(personagem), str(pessoa)])
            
            if len(rows) > 1:
                worksheet.update(f'A1:C{len(rows)}', rows)
            else:
                worksheet.update('A1:C1', rows)
            return True
        
        # Formato codigos_identidade: ID | Responsável
        elif sheet_name == "codigos_identidade" and isinstance(data, dict):
            rows = [['ID', 'Responsável']]
            for user_id, responsavel in data.items():
                if responsavel:
                    rows.append([str(user_id), str(responsavel)])
            
            if len(rows) > 1:
                worksheet.update(f'A1:B{len(rows)}', rows)
            else:
                worksheet.update('A1:B1', rows)
            return True
        
        # Formato identidades: Personagem | Nome Real | URL da Foto
        elif sheet_name == "identidades" and isinstance(data, dict):
            rows = [['Personagem', 'Nome Real', 'URL da Foto']]
            for personagem, info in data.items():
                if isinstance(info, dict):
                    nome = info.get('nome', '')
                    foto = info.get('foto', '')
                    rows.append([str(personagem), str(nome), str(foto)])
            
            if len(rows) > 1:
                worksheet.update(f'A1:C{len(rows)}', rows)
            else:
                worksheet.update('A1:C1', rows)
            return True
        
        # Formato revelacoes: Personagem | Pessoa
        elif sheet_name == "revelacoes" and isinstance(data, dict):
            rows = [['Personagem', 'Pessoa']]
            for personagem, pessoa in data.items():
                rows.append([str(personagem), str(pessoa)])
            
            if len(rows) > 1:
                worksheet.update(f'A1:B{len(rows)}', rows)
            else:
                worksheet.update('A1:B1', rows)
            return True
        
        # Formato key-value padrão para outros casos
        else:
            rows = [['key', 'value']]
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    value_str = json.dumps(value, ensure_ascii=False)
                else:
                    value_str = str(value)
                rows.append([str(key), value_str])
            
            worksheet.update(f'A1:B{len(rows)}', rows)
            return True
    except Exception:
        # Erro silencioso - usa fallback JSON
        return save_json_fallback(f"{sheet_name}.json", data)

# Funções de fallback para JSON local (caso Google Sheets não esteja disponível)
def load_json_fallback(path):
    """Fallback: carrega dados de arquivo JSON local."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json_fallback(path, data):
    """Fallback: salva dados em arquivo JSON local."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

# Função auxiliar para debug
def preview_sheet_structure(sheet_name, max_rows=5):
    """
    Mostra a estrutura da planilha para debug.
    Retorna as primeiras linhas e headers detectados.
    """
    spreadsheet = get_spreadsheet()
    if spreadsheet is None:
        return None
    
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        all_values = worksheet.get_all_values()
        
        if not all_values:
            return {"error": "Planilha vazia"}
        
        headers = all_values[0] if all_values else []
        sample_data = all_values[1:min(max_rows + 1, len(all_values))]
        
        return {
            "sheet_name": sheet_name,
            "headers": headers,
            "num_columns": len(headers),
            "num_rows": len(all_values) - 1,
            "sample_data": sample_data,
            "format_detected": "key-value" if (len(headers) >= 2 and headers[0].lower() in ['key', 'chave']) else "tabular"
        }
    except Exception as e:
        return {"error": str(e)}
