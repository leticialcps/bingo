"""
Módulo para integração com Google Sheets como banco de dados.
Substitui os arquivos JSON por planilhas do Google Sheets.
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
    except Exception as e:
        st.error(f"Erro ao conectar com Google Sheets: {e}")
        st.info("Usando arquivos JSON locais como fallback.")
        return None

def get_spreadsheet():
    """
    Retorna a planilha do Bingo ou None se não conseguir conectar.
    """
    client = get_google_sheets_client()
    if client is None:
        return None
    
    try:
        # Tenta abrir a planilha pelo nome ou cria uma nova
        sheet_name = st.secrets.get("sheet_name", "Bingo Amigo Secreto")
        try:
            spreadsheet = client.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            # Se não existir, cria uma nova planilha
            spreadsheet = client.create(sheet_name)
            # Compartilha com você para poder editar
            spreadsheet.share('', perm_type='anyone', role='writer')
            st.success(f"Nova planilha criada: {sheet_name}")
        
        return spreadsheet
    except Exception as e:
        st.error(f"Erro ao acessar planilha: {e}")
        return None

def load_sheet_data(sheet_name):
    """
    Carrega dados de uma aba específica da planilha.
    Retorna um dicionário (equivalente ao JSON).
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
            return {}
        
        # Lê todos os dados da aba
        records = worksheet.get_all_records()
        
        # Converte para dicionário
        result = {}
        for record in records:
            key = record.get('key')
            value_str = record.get('value', '')
            if key:
                try:
                    # Tenta fazer parse do JSON se o valor for um objeto/array
                    result[key] = json.loads(value_str) if value_str else ''
                except json.JSONDecodeError:
                    result[key] = value_str
        
        return result
    except Exception as e:
        st.error(f"Erro ao ler dados da planilha {sheet_name}: {e}")
        return load_json_fallback(f"{sheet_name}.json")

def save_sheet_data(sheet_name, data):
    """
    Salva dados em uma aba específica da planilha.
    data deve ser um dicionário (equivalente ao JSON).
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
        
        # Prepara os dados para escrita
        rows = [['key', 'value']]  # Header
        for key, value in data.items():
            # Converte valores complexos para JSON string
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, ensure_ascii=False)
            else:
                value_str = str(value)
            rows.append([str(key), value_str])
        
        # Escreve todos os dados de uma vez
        worksheet.update(f'A1:B{len(rows)}', rows)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados na planilha {sheet_name}: {e}")
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
