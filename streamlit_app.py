import streamlit as st
import json
import uuid
import os
import base64
import mimetypes
from datetime import datetime
from sheets_db import load_sheet_data, save_sheet_data, preview_sheet_structure

# -----------------------------------------------
# Funções utilitárias
# -----------------------------------------------
def load_json(path):
    """Carrega dados do Google Sheets (com fallback para JSON local)."""
    sheet_name = path.replace('.json', '')
    data = load_sheet_data(sheet_name)
    # Se retornar vazio, garante estrutura mínima
    if not data:
        return {}
    return data

def save_json(path, data):
    """Salva dados no Google Sheets (com fallback para JSON local)."""
    sheet_name = path.replace('.json', '')
    result = save_sheet_data(sheet_name, data)
    # Limpa cache após salvar para forçar reload
    if result:
        carregar_todos_dados.clear()
    return result


def _rounded_image_html(path, width=120):
    """Retorna um HTML <img> com border-radius aplicado e imagem embutida em base64.
    Usa o caminho do arquivo local `path` e dimensiona para `width` (px).
    """
    try:
        if not path:
            return ""
        # se for uma URL, usa src direto (não embutir)
        if isinstance(path, str) and path.startswith(("http://", "https://")):
            src = path
            html = f'<img src="{src}" style="border-radius:50%; width:{width}px; height:{width}px; object-fit:cover; background: transparent;"/>'
            return html
        # caso contrário, tenta ler arquivo local e embutir em base64
        with open(path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = "image/png"
        html = f'<img src="data:{mime};base64,{b64}" style="border-radius:50%; width:{width}px; height:{width}px; object-fit:cover; background: transparent;"/>'
        return html
    except Exception:
        return ""


def make_bingo_grid(items, cols=3, rows=5):
    """Retorna uma lista de linhas (cada linha é lista de tamanho `cols`) preenchida com
    os primeiros `cols*rows` itens de `items`. Se houver menos itens, preenche com None.
    """
    total = cols * rows
    sliced = list(items)[:total]
    # pad
    while len(sliced) < total:
        sliced.append(None)
    grid = [sliced[i * cols:(i + 1) * cols] for i in range(rows)]
    return grid

# Carrega dados uma única vez com cache
@st.cache_data(ttl=60)
def carregar_todos_dados():
    """Carrega todos os dados de uma vez para evitar múltiplas chamadas à API."""
    return {
        "participantes": load_json("participantes.json"),
        "apostas": load_json("apostas.json"),
        "revelacoes": load_json("revelacoes.json"),
        "identidades": load_json("identidades.json"),
        "vinculos": load_json("codigos_identidade.json")
    }

# Carrega todos os dados
dados = carregar_todos_dados()
participantes = dados["participantes"]
nomes_reais = participantes.get("nomes_reais", [])

# Pega lista de personagens da aba identidades
identidades = dados["identidades"]
personagens = list(identidades.keys()) if isinstance(identidades, dict) else []

apostas = dados["apostas"]
revelacoes = dados["revelacoes"]
vinculos = dados["vinculos"]

st.set_page_config(page_title="Amigo Secreto Swifities Idosos!", layout="centered")

# Adiciona imagem de fundo + estilo do título com glitter laranja suave e contorno preto
st.markdown(
    '''
    <style>
    .stApp {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXKOiGBTCBwZQg0_RpXfxQQ268gOg6jIiIeA&s");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
        /* Suaviza contraste para melhor leitura */
        box-shadow: inset 0 0 0 2000px rgba(0,0,0,0.25);
        position: relative;
    }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXKOiGBTCBwZQg0_RpXfxQQ268gOg6jIiIeA&s");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        z-index: -1;
    }
    /* Deixa caixas principais mais legíveis */
    .stMarkdown, .stDataFrame, .stTextInput, .stSelectbox, .stButton, .stHeader, .stSubheader, .stRadio, .stAlert {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 12px;
        padding: 12px 16px !important;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    /* Textos gerais - mais legíveis */
    .stMarkdown, p, span, label, .stText {
        color: #1a1a1a !important;
        font-size: 1.05em;
        line-height: 1.6;
    }
    /* Headers e subheaders */
    h2, h3, h4, h5, h6, .stHeader, .stSubheader {
        color: #ff8800 !important;
        font-weight: bold;
        text-shadow: 0 1px 2px rgba(255,255,255,0.5);
    }
    /* Selectbox e input mais legíveis */
    .stSelectbox > div > div, .stTextInput > div > div {
        background: white !important;
    }
    input, select, textarea {
        color: #1a1a1a !important;
        background: white !important;
        border: 2px solid #ff8800 !important;
        border-radius: 8px;
    }
    /* Selectbox aumentado */
    .stSelectbox {
        font-size: 1.2em !important;
    }
    .stSelectbox > div > div > div > div {
        min-height: 50px !important;
        padding: 15px !important;
    }
    select {
        min-height: 50px !important;
        padding: 12px !important;
        font-size: 1.1em !important;
        color: #1a1a1a !important;
    }
    /* Força texto escuro em todos os selects, opções e entradas do selectbox */
    .stSelectbox div[data-baseweb="select"] * {
        color: #1a1a1a !important;
        background: white !important;
        font-weight: 600 !important;
    }
    .stSelectbox input::placeholder {
        color: #1a1a1a !important;
        opacity: 1 !important;
    }
    .stSelectbox input {
        color: #1a1a1a !important;
        background: white !important;
        font-weight: 600 !important;
    }
    .stSelectbox span {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    /* Remove fundo branco das imagens */
    .stMarkdown img {
        background: transparent !important;
        padding: 0 !important;
    }
    /* Markdown contendo imagens sem fundo branco */
    .stMarkdown:has(img) {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    /* Título laranja elegante com glitter sofisticado estilo tipografia */
    h1 {
        color: #ff8800;
        font-family: 'Georgia', 'Garamond', 'Palatino', serif;
        font-weight: bold;
        font-style: italic;
        letter-spacing: 2px;
        text-shadow: 
            -1px -1px 0 rgba(0,0,0,0.2),
            1px -1px 0 rgba(0,0,0,0.2),
            -1px 1px 0 rgba(0,0,0,0.2),
            1px 1px 0 rgba(0,0,0,0.2),
            0 0 10px rgba(255, 200, 100, 0.6),
            0 0 20px rgba(255, 150, 50, 0.4),
            0 0 30px rgba(255, 200, 100, 0.3);
        font-size: 2.8em;
        animation: elegant-glitter 3.5s ease-in-out infinite;
    }
    @keyframes elegant-glitter {
        0%, 100% { 
            filter: brightness(0.9) drop-shadow(0 0 6px rgba(255, 200, 100, 0.4));
        }
        25% { 
            filter: brightness(1.15) drop-shadow(0 0 12px rgba(255, 200, 100, 0.6));
        }
        50% { 
            filter: brightness(1.05) drop-shadow(0 0 16px rgba(255, 150, 50, 0.5));
        }
        75% { 
            filter: brightness(1.2) drop-shadow(0 0 14px rgba(255, 200, 100, 0.6));
        }
    }
    h2, h3, .stTitle {
        color: #b71c1c;
        text-shadow: 1px 1px 0 #fff, 2px 2px 4px #388e3c44;
    }
    /* Botões - Branco com efeito laranja ao clicar */
    .stButton > button {
        background: white !important;
        color: #ff8800 !important;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #ff8800 !important;
        padding: 12px 24px;
        box-shadow: 0 4px 8px rgba(255, 136, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: rgba(255, 136, 0, 0.1) !important;
        box-shadow: 0 6px 16px rgba(255, 136, 0, 0.4) !important;
        transform: translateY(-2px);
    }
    .stButton > button:active {
        background: rgba(255, 136, 0, 0.2) !important;
        box-shadow: 0 2px 8px rgba(255, 136, 0, 0.3) !important;
    }
    /* Sidebar - garantir que fique visível e legível */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        z-index: 999 !important;
    }
    section[data-testid="stSidebar"] .stRadio > label {
        color: #1a1a1a !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label {
        color: #1a1a1a !important;
        font-size: 1.05em !important;
    }
    </style>
    ''', unsafe_allow_html=True)

st.title("Bingo Amigo Secreto Swifities Idosos")

# Verifica se Google Sheets está configurado
try:
    _ = st.secrets["gcp_service_account"]
    sheets_ativo = True
except:
    sheets_ativo = False
    with st.sidebar:
        st.info("💡 Usando arquivos locais. Para dados persistentes, configure Google Sheets.")

# Menu de debug (só aparece se Sheets estiver ativo)
if sheets_ativo:
    with st.sidebar:
        with st.expander("🔍 Debug - Estrutura das Planilhas"):
            if st.button("Ver estrutura de 'participantes'"):
                info = preview_sheet_structure("participantes")
                if info:
                    st.json(info)
            
            if st.button("Recarregar dados do Google Sheets"):
                st.cache_resource.clear()
                st.rerun()

menu = st.sidebar.radio("Menu", ["Fazer Aposta", "Revelar Identidades", "Ranking"])

# Detecta se está na tela inicial
if menu == "Fazer Aposta":
    st.markdown(
        '''
        <style>
        .stApp {
            background-image: url("https://i.pinimg.com/originals/00/ea/e1/00eae19fb5b8a573bd61d81d30270436.jpg") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            filter: none !important;
        }
        .stApp::before {
            filter: none !important;
        }
        </style>
        ''', unsafe_allow_html=True)

# -----------------------------------------------
# Página - Apostas
# -----------------------------------------------
if menu == "Fazer Aposta":

    st.header("✨Faça suas apostas:✨")
    st.write("Você receberá um código anônimo para usar depois no ranking.")

    user_id = st.text_input("Digite seu código (ou deixe em branco para gerar)")

    if not user_id:
        if st.button("Gerar novo código"):
            user_id = uuid.uuid4().hex
            st.success(f"Seu código anônimo é:\n\n*{user_id}*\n\n⚠️ Salve esse código, é sua identidade no jogo!")
            st.stop()

    if user_id:
        st.info(f"Você está apostando como: *{user_id}*")

        # Vínculo do código ao nome real disponível apenas no dia 14/12
        hoje = datetime.now()
        pode_vincular = (hoje.day == 4 and hoje.month == 12)
        if pode_vincular:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.9); border-radius: 12px; padding: 16px; margin: 8px 0;'>
                <b style='color:#ff8800'>Vincular código ao seu nome real (disponível hoje)</b>
            </div>
            """, unsafe_allow_html=True)

            opcoes_nomes = ["Selecione seu nome real"] + nomes_reais
            atual = vinculos.get(user_id)
            idx_nome = opcoes_nomes.index(atual) if atual in nomes_reais else 0
            nome_escolhido = st.selectbox(
                "Seu nome real:", opcoes_nomes, index=idx_nome, key=f"vinc_{user_id}")
            if st.button("Salvar vínculo", use_container_width=True, key=f"btn_vinc_{user_id}"):
                if nome_escolhido == "Selecione seu nome real":
                    st.warning("Selecione um nome válido para vincular.")
                else:
                    vinculos[user_id] = nome_escolhido
                    save_json("codigos_identidade.json", vinculos)
                    st.success(f"Código vinculado ao nome real: {nome_escolhido}")

        # Carrega apostas anteriores (se existirem) e pré-preenche os selectboxes
        aposta_temp = {}
        saved = apostas.get(user_id, {}) if isinstance(apostas, dict) else {}

        st.write("Preencha a possível identidade de cada personagem:")
        
        # Rastreia quais nomes já foram escolhidos - preenche com as escolhas salvas primeiro
        nomes_ja_escolhidos = set()
        for personagem in personagens:
            escolha_salva = saved.get(personagem)
            if escolha_salva and escolha_salva in nomes_reais:
                nomes_ja_escolhidos.add(escolha_salva)

        # monta cartela 3x5
        grid = make_bingo_grid(personagens, cols=3, rows=5)
        for row in grid:
            cols = st.columns(3)
            for col, p in zip(cols, row):
                with col:
                    if p:
                        # Container padronizado para cada personagem
                        st.markdown(
                            f"""
                            <div style='text-align: center; background: rgba(255,255,255,0.9); 
                            border-radius: 12px; padding: 16px; margin-bottom: 12px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
                                <b style='color: #1a1a1a; font-size: 1.1em;'>{p}</b>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        
                        # mostra foto arredondada (se houver) - CENTRALIZADA
                        foto = None
                        if isinstance(identidades, dict):
                            data = identidades.get(p, {})
                            foto = data.get("foto") if isinstance(data, dict) else None
                        if foto:
                            try:
                                html = _rounded_image_html(foto, width=120)
                                if html:
                                    st.markdown(f"<div style='text-align: center; margin: 8px 0;'>{html}</div>", unsafe_allow_html=True)
                            except Exception:
                                pass

                        # Nomes disponíveis = todos exceto os já escolhidos (mas mantém o default)
                        default = saved.get(p) if p in saved else None
                        
                        # Monta lista de opções disponíveis
                        nomes_disponiveis = [n for n in nomes_reais if n not in nomes_ja_escolhidos or n == default]
                        options = ["Faça sua aposta"] + nomes_disponiveis
                        
                        if default in nomes_reais and default in options:
                            idx = options.index(default)
                        else:
                            idx = 0
                            
                        sel = st.selectbox(
                            f"Quem é {p}?",
                            options,
                            index=idx,
                            key=f"ap_{user_id}_{p}",
                            label_visibility="collapsed"
                        )
                        
                        # Salva a escolha
                        aposta_temp[p] = "" if sel == "Faça sua aposta" else sel
                        if sel != "Faça sua aposta":
                            nomes_ja_escolhidos.add(sel)
                            aposta_temp[p] = sel
                        else:
                            aposta_temp[p] = ""
                    else:
                        st.write("")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Salvar minhas apostas", use_container_width=True):
                apostas[user_id] = aposta_temp
                save_json("apostas.json", apostas)
                st.success("Apostas registradas com sucesso!")

# -----------------------------------------------
# Página - Revelação (Admin)
# -----------------------------------------------
elif menu == "Revelar Identidades":

    st.markdown(
        '''
        <style>
        .stApp {
            background-image: url("https://www.rollingstone.com/wp-content/uploads/2025/10/taylor-swift-takeaways.jpg?w=1581&h=1054&crop=1") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            filter: contrast(1.1) brightness(1.05) !important;
        }
        .stApp::before {
            background-image: url("https://www.rollingstone.com/wp-content/uploads/2025/10/taylor-swift-takeaways.jpg?w=1581&h=1054&crop=1") !important;
            filter: contrast(1.1) brightness(1.05) !important;
        }
        </style>
        ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.header("🔓 Revelação Oficial")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        senha = st.text_input("Senha de admin:", type="password")

    if senha == "admin123":  # você pode trocar
        st.success("Acesso liberado!")

        st.write("Selecione as revelações oficiais:")
        
        # Rastreia quais nomes já foram revelados
        st.write("Selecione as revelações oficiais:")
        
        # Rastreia quais nomes já foram revelados - preenche primeiro com revelações existentes
        nomes_ja_revelados = set()
        for personagem in personagens:
            revelacao_existente = revelacoes.get(personagem, "Ainda não revelado")
            if revelacao_existente != "Ainda não revelado" and revelacao_existente in nomes_reais:
                nomes_ja_revelados.add(revelacao_existente)
        
        # monta cartela 3x5 para revelações
        grid = make_bingo_grid(personagens, cols=3, rows=5)
                with col:
                    if p:
                        # Container padronizado para cada personagem
                        st.markdown(
                            f"""
                            <div style='text-align: center; background: rgba(255,255,255,0.9); 
                            border-radius: 12px; padding: 16px; margin-bottom: 12px; 
                            box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
                                <b style='color: #1a1a1a; font-size: 1.1em;'>{p}</b>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        
                        # mostra foto arredondada (se houver) - CENTRALIZADA
                        foto = None
                        if isinstance(identidades, dict):
                            data = identidades.get(p, {})
                            foto = data.get("foto") if isinstance(data, dict) else None
                        if foto:
                            try:
                                html = _rounded_image_html(foto, width=120)
                                if html:
                                    st.markdown(f"<div style='text-align: center; margin: 8px 0;'>{html}</div>", unsafe_allow_html=True)
                            except Exception:
                                pass

                        current = revelacoes.get(p, "Ainda não revelado")
                        
                        # Nomes disponíveis = todos exceto os já revelados (mas mantém o current)
                        nomes_disponiveis = [n for n in nomes_reais if n not in nomes_ja_revelados or n == current]
                        options = ["Ainda não revelado"] + nomes_disponiveis
                        
                        try:
                            idx = options.index(current)
                        except ValueError:
                            idx = 0
                            
                        sel = st.selectbox("Quem é?", options, index=idx, key=f"rev_{p}", label_visibility="collapsed")
                        
                        revelacoes[p] = sel
                    else:
                        st.write("")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Confirmar Revelações", use_container_width=True):
                save_json("revelacoes.json", revelacoes)
            st.balloons()
            st.success("Revelações registradas!")

    else:
        st.warning("Senha incorreta ou não informada.")

# -----------------------------------------------
# Página - Ranking
# -----------------------------------------------
elif menu == "Ranking":
    st.markdown(
        '''
        <style>
        .stApp {
            background-image: url("https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2024/02/GettyImages-1986535927-e1707118230218.jpg?w=1200&h=900&crop=1") !important;
            background-size: cover !important;
            background-position: center top !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            filter: none !important;
        }
        .stApp::before {
            filter: none !important;
        }
        </style>
        ''', unsafe_allow_html=True)

    st.header("🏆 Ranking Parcial / Final")

    if len(revelacoes) == 0 or all(v == "Ainda não revelado" for v in revelacoes.values()):
        st.info("Nenhuma revelação ainda.")
    else:
        resultados = []

        for apostador, palpites in apostas.items():
            pontos = 0
            acertados = []
            for personagem, revelado in revelacoes.items():
                if revelado != "Ainda não revelado" and palpites.get(personagem) == revelado:
                    pontos += 1
                    acertados.append(personagem)
            resultados.append((apostador, pontos, acertados))

        resultados = sorted(resultados, key=lambda x: x[1], reverse=True)

        st.subheader("📈 Placares")
        
        # Verifica se hoje é 14/12 para revelar nomes reais independente das revelações
        hoje = datetime.now()
        dia_revelacao = (hoje.day == 4 and hoje.month == 12)
        
        for i, (player, score, acertados) in enumerate(resultados, 1):
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
            nome_real_vinculado = vinculos.get(player)
            
            if dia_revelacao and nome_real_vinculado:
                # No dia 14/12, mostra o nome real se o vínculo existir
                exibicao = nome_real_vinculado
            else:
                # Fora do dia, revela o nome real somente se o personagem dessa pessoa já tiver sido revelado
                nomes_revelados = set(v for v in revelacoes.values() if v != "Ainda não revelado")
                pode_revelar_nome = nome_real_vinculado in nomes_revelados if nome_real_vinculado else False
                exibicao = nome_real_vinculado if pode_revelar_nome else player
            
            st.write(f"{medalha} *{exibicao}* — {score} pontos")

            if acertados:
                st.write("**Personagens acertados:**")
                for p in acertados:
                    st.write(f"- {p}")
                    # tenta exibir foto associada ao personagem (se houver)
                    foto = None
                    if isinstance(identidades, dict):
                        data = identidades.get(p, {})
                        foto = data.get("foto") if isinstance(data, dict) else None
                    if foto:
                        try:
                            html = _rounded_image_html(foto, width=120)
                            if html:
                                st.markdown(html, unsafe_allow_html=True)
                            else:
                                st.write("(Imagem não encontrada)")
                        except Exception:
                            st.write("(Imagem não encontrada)")
            else:
                st.write("_Nenhum acerto ainda_")

        st.write("---")
        st.caption("Ranking atual baseado nas revelações divulgadas.")
