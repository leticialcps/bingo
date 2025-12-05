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
# if sheets_ativo:
#     with st.sidebar:
#         with st.expander("🔍 Debug - Estrutura das Planilhas"):
#             if st.button("Ver estrutura de 'participantes'"):
#                 info = preview_sheet_structure("participantes")
#                 if info:
#                     st.json(info)
#             
#             if st.button("Recarregar dados do Google Sheets"):
#                 st.cache_resource.clear()
#                 st.rerun()

menu = st.sidebar.radio("Menu", ["Fazer Aposta", "Revelar Identidades", "Ranking"])# Detecta se está na tela inicial
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
    
    # Verifica se é dia 14/12 às 17h ou depois (horário de Brasília UTC-3)
    from datetime import timezone, timedelta
    brasilia_tz = timezone(timedelta(hours=-3))
    agora_brasilia = datetime.now(brasilia_tz)
    
    apostas_bloqueadas = (agora_brasilia.day == 14 and 
                         agora_brasilia.month == 12 and 
                         agora_brasilia.hour >= 17)
    
    # Se apostas bloqueadas, pede senha de admin
    acesso_apostas = not apostas_bloqueadas
    
    if apostas_bloqueadas:
        st.warning("⏰ Apostas encerradas! Hoje é 14/12 após 17h.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            senha_apostas = st.text_input("Senha de admin para acessar:", type="password", key="senha_apostas")
        
        if senha_apostas == "taylorswift13":
            acesso_apostas = True
            st.success("Acesso administrativo liberado!")
        else:
            st.info("Apenas administradores podem fazer apostas após o encerramento.")
    
    if not acesso_apostas:
        st.stop()
    
    st.write("Você receberá um código anônimo para usar depois no ranking.")

    user_id = st.text_input("Digite seu código (ou deixe em branco para gerar)")

    if not user_id:
        if st.button("Gerar novo código"):
            user_id = uuid.uuid4().hex
            st.success(f"Seu código anônimo é:\n\n*{user_id}*\n\n⚠️ Salve esse código, é sua identidade no jogo!")
            st.stop()

    if user_id:
        # Verifica se já existem apostas para este ID
        apostas_existentes = apostas.get(user_id, {}) if isinstance(apostas, dict) else {}
        if apostas_existentes:
            qtd_apostas = sum(1 for v in apostas_existentes.values() if v and v != "")
            st.success(f"✓ Apostas encontradas! Você já tem {qtd_apostas} aposta(s) salva(s) com este código.")
            st.info("Você pode revisar e alterar suas apostas abaixo.")
            
            # Mostra resumo das apostas existentes
            with st.expander("📋 Ver minhas apostas salvas"):
                for personagem, nome in apostas_existentes.items():
                    if nome:
                        st.write(f"• **{personagem}** → {nome}")
        else:
            st.info(f"Você está apostando como: *{user_id}*")

        # Vínculo do código ao nome real
        # Verifica se é dia 14/12 a partir das 17h (horário de Brasília UTC-3)
        from datetime import timezone, timedelta
        brasilia_tz = timezone(timedelta(hours=-3))
        agora_brasilia = datetime.now(brasilia_tz)
        
        # Disponível o dia todo no dia 14/12, mas OBRIGATÓRIO a partir das 17h
        dia_14 = (agora_brasilia.day == 14 and agora_brasilia.month == 12)
        apos_17h = (agora_brasilia.hour >= 17)
        
        vinculo_obrigatorio = dia_14 and apos_17h
        vinculo_disponivel = dia_14
        
        # Se for antes do dia 14/12, pede senha para vincular
        acesso_vinculo = vinculo_disponivel
        
        if not vinculo_disponivel:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.9); border-radius: 12px; padding: 16px; margin: 8px 0;'>
                <b style='color:#ff8800'>🔒 Vincular código ao nome real (requer senha de admin)</b>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                senha_vinculo = st.text_input("Senha de admin:", type="password", key="senha_vinculo")
            
            if senha_vinculo == "taylorswift13":
                acesso_vinculo = True
                st.success("Acesso liberado para vincular nome!")
            else:
                if senha_vinculo:
                    st.warning("Senha incorreta.")
        
        if acesso_vinculo:
            mensagem = "⚠️ OBRIGATÓRIO: Vincule seu código ao nome real" if vinculo_obrigatorio else "Vincular código ao seu nome real (disponível hoje)"
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.9); border-radius: 12px; padding: 16px; margin: 8px 0;'>
                <b style='color:#ff8800'>{mensagem}</b>
            </div>
            """, unsafe_allow_html=True)

            opcoes_nomes = ["Selecione seu nome real"] + nomes_reais
            atual = vinculos.get(user_id)
            idx_nome = opcoes_nomes.index(atual) if atual in nomes_reais else 0
            nome_escolhido = st.selectbox(
                "Seu nome real:", opcoes_nomes, index=idx_nome, key=f"vinc_{user_id}")
            
            if vinculo_obrigatorio and nome_escolhido == "Selecione seu nome real":
                st.error("⚠️ Você DEVE vincular seu código ao nome real.")
            
            if st.button("Salvar vínculo", use_container_width=True, key=f"btn_vinc_{user_id}"):
                if nome_escolhido == "Selecione seu nome real":
                    st.warning("Selecione um nome válido para vincular.")
                else:
                    vinculos[user_id] = nome_escolhido
                    save_json("codigos_identidade.json", vinculos)
                    st.success(f"Código vinculado ao nome real: {nome_escolhido}")
        
        # Se for após 17h do dia 14/12, apenas mostra backup e não permite apostas
        if vinculo_obrigatorio:
            st.markdown("---")
            st.info("⏰ Apostas encerradas! Veja abaixo suas apostas já realizadas:")
            
            # Mostra backup das apostas
            saved = apostas.get(user_id, {}) if isinstance(apostas, dict) else {}
            if saved:
                apostas_formatadas = "\n".join([f"{p}: {n}" for p, n in saved.items() if n])
                st.text_area(
                    "Suas apostas (copie para guardar):",
                    value=f"ID: {user_id}\n\n{apostas_formatadas}",
                    height=200
                )
            else:
                st.warning("Você não fez nenhuma aposta.")
            st.stop()

        # Carrega apostas anteriores (se existirem) e pré-preenche os selectboxes
        aposta_temp = {}
        saved = apostas.get(user_id, {}) if isinstance(apostas, dict) else {}

        st.write("Preencha a possível identidade de cada personagem:")
        
        # Primeiro passa: coleta todas as escolhas atuais (combinando saved e session_state)
        escolhas_atuais = {}
        for p in personagens:
            widget_key = f"ap_{user_id}_{p}"
            # Primeiro tenta pegar do session_state (mais recente)
            if widget_key in st.session_state:
                val = st.session_state[widget_key]
                if val != "Faça sua aposta":
                    escolhas_atuais[p] = val
            # Se não tem no session_state, usa o saved
            elif p in saved and saved[p]:
                escolhas_atuais[p] = saved[p]

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

                        # Pega a escolha atual deste personagem
                        escolha_atual = escolhas_atuais.get(p)
                        
                        # Coleta nomes já escolhidos EXCETO o atual
                        nomes_ja_escolhidos = set()
                        for outro_p, nome_escolhido in escolhas_atuais.items():
                            if outro_p != p and nome_escolhido:
                                nomes_ja_escolhidos.add(nome_escolhido)
                        
                        # Monta lista de opções disponíveis (exclui já escolhidos em outros)
                        nomes_disponiveis = [n for n in nomes_reais if n not in nomes_ja_escolhidos]
                        options = ["Faça sua aposta"] + nomes_disponiveis
                        
                        # Verifica se a escolha atual ainda está disponível
                        if escolha_atual and escolha_atual in options:
                            idx = options.index(escolha_atual)
                        else:
                            idx = 0
                            
                        sel = st.selectbox(
                            f"Quem é {p}?",
                            options,
                            index=idx,
                            key=f"ap_{user_id}_{p}",
                            label_visibility="collapsed"
                        )
                        
                        # Salva a escolha em aposta_temp
                        if sel != "Faça sua aposta":
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
                
                # Mostra resumo das apostas para backup
                # st.markdown("---")
                # st.markdown("### 📋 Resumo das suas apostas")
                # st.info("💾 Salve este resumo como backup!")
                
                # resumo_texto = f"**ID:** {user_id}\n\n**Apostas:**\n"
                # for personagem, nome in aposta_temp.items():
                #     if nome:
                #         resumo_texto += f"• {personagem} → {nome}\n"
                
                # st.markdown(resumo_texto)
                
                # Campo copiável
                apostas_formatadas = "\n".join([f"{p}: {n}" for p, n in aposta_temp.items() if n])
                st.text_area(
                    "Copie este texto para guardar como backup:",
                    value=f"ID: {user_id}\n\n{apostas_formatadas}",
                    height=200
                )

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
    
    # Verifica se é dia 14/12
    hoje = datetime.now()
    dia_revelacao = (hoje.day == 14 and hoje.month == 12)
    
    # Solicita senha apenas se NÃO for dia 14/12
    acesso_liberado = dia_revelacao
    
    if not dia_revelacao:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            senha = st.text_input("Senha de admin:", type="password")
        
        if senha == "taylorswift13":  # você pode trocar
            acesso_liberado = True
            st.success("Acesso liberado!")
    else:
        st.info("🎉 Hoje é dia 14/12! Vamos para as revelações.")

    if acesso_liberado:
        st.write("Selecione as revelações oficiais:")
        
        # monta cartela 3x5 para revelações
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

                        current = revelacoes.get(p, "Ainda não revelado")
                        
                        # Coleta nomes já revelados EXCETO o atual
                        nomes_ja_revelados = set()
                        for outro_personagem, nome_revelado in revelacoes.items():
                            if outro_personagem != p and nome_revelado != "Ainda não revelado" and nome_revelado in nomes_reais:
                                nomes_ja_revelados.add(nome_revelado)
                        
                        # Nomes disponíveis = todos exceto os já revelados em outros personagens
                        nomes_disponiveis = [n for n in nomes_reais if n not in nomes_ja_revelados]
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

    elif not dia_revelacao:
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

    # Botão para recarregar dados
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("Ranking")
    with col2:
        if st.button("🔄 Atualizar", use_container_width=True, key="btn_atualizar_ranking"):
            # Limpa todos os caches
            st.cache_data.clear()
            st.cache_resource.clear()
            carregar_todos_dados.clear()
            st.rerun()

    if len(revelacoes) == 0 or all(v == "Ainda não revelado" for v in revelacoes.values()):
        st.info("Nenhuma revelação ainda.")
    else:
        # === SEÇÃO 1: PERSONAGENS REVELADOS ===
        st.markdown("### 🎭 Personagens Revelados")
        
        # Conta quantas pessoas acertaram cada personagem
        acertos_por_personagem = {}
        for personagem, revelado in revelacoes.items():
            if revelado != "Ainda não revelado":
                acertos = 0
                for apostador, palpites in apostas.items():
                    if palpites.get(personagem) == revelado:
                        acertos += 1
                acertos_por_personagem[personagem] = (revelado, acertos)
        
        # Mostra em grid
        if acertos_por_personagem:
            cols_revelados = st.columns(3)
            for idx, (personagem, (revelado, qtd_acertos)) in enumerate(acertos_por_personagem.items()):
                with cols_revelados[idx % 3]:
                    # Pega foto do personagem
                    foto = None
                    if isinstance(identidades, dict):
                        data = identidades.get(personagem, {})
                        foto = data.get("foto") if isinstance(data, dict) else None
                    
                    foto_html = ""
                    if foto:
                        try:
                            foto_html = _rounded_image_html(foto, width=80)
                        except:
                            pass
                    
                    st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.95); border-radius: 12px; padding: 16px; 
                                margin-bottom: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
                        {foto_html}
                        <div style='margin-top: 8px;'>
                            <b style='color: #ff8800; font-size: 1.1em;'>{personagem}</b><br>
                            <span style='color: #1a1a1a; font-size: 1em;'>{revelado}</span><br>
                            <span style='color: #666; font-size: 0.9em;'>✓ {qtd_acertos} acerto{'s' if qtd_acertos != 1 else ''}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # === SEÇÃO 2: RANKING DE PARTICIPANTES ===
        st.markdown("### 🏅 Ranking")
        
        # Calcula resultados
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
        
        # Verifica se hoje é 14/12 para revelar nomes reais
        hoje = datetime.now()
        dia_revelacao = (hoje.day == 14 and hoje.month == 12)
        
        # Renderiza leaderboard estilizado
        for i, (player, score, acertados) in enumerate(resultados, 1):
            nome_real_vinculado = vinculos.get(player)
            
            if dia_revelacao and nome_real_vinculado:
                exibicao = nome_real_vinculado
            else:
                nomes_revelados = set(v for v in revelacoes.values() if v != "Ainda não revelado")
                pode_revelar_nome = nome_real_vinculado in nomes_revelados if nome_real_vinculado else False
                exibicao = nome_real_vinculado if pode_revelar_nome else player
            
            # Define medalha e cor
            if i == 1:
                medalha = "🥇"
                cor_fundo = "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)"
                cor_texto = "#1a1a1a"
            elif i == 2:
                medalha = "🥈"
                cor_fundo = "linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%)"
                cor_texto = "#1a1a1a"
            elif i == 3:
                medalha = "🥉"
                cor_fundo = "linear-gradient(135deg, #CD7F32 0%, #B8860B 100%)"
                cor_texto = "#fff"
            else:
                medalha = f"{i}"
                cor_fundo = "rgba(255,255,255,0.9)"
                cor_texto = "#1a1a1a"
            
            # Calcula estrelas (de 5, baseado na pontuação)
            total_revelacoes = len([v for v in revelacoes.values() if v != "Ainda não revelado"])
            if total_revelacoes > 0:
                estrelas_cheias = int((score / total_revelacoes) * 5)
                estrelas = "⭐" * estrelas_cheias + "☆" * (5 - estrelas_cheias)
            else:
                estrelas = "☆☆☆☆☆"
            
            st.markdown(f"""
            <div style='background: {cor_fundo}; border-radius: 12px; padding: 16px; 
                        margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                        display: flex; align-items: center; justify-content: space-between;'>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='width: 50px; height: 50px; border-radius: 50%; 
                                background: rgba(0,0,0,0.1); display: flex; 
                                align-items: center; justify-content: center;
                                font-size: 1.5em; font-weight: bold; color: {cor_texto};'>
                        {medalha}
                    </div>
                    <div>
                        <div style='font-size: 1.2em; font-weight: bold; color: {cor_texto};'>
                            {exibicao[:20]}
                        </div>
                        <div style='font-size: 0.9em; color: {cor_texto}; opacity: 0.8;'>
                            {estrelas}
                        </div>
                    </div>
                </div>
                <div style='font-size: 1.5em; font-weight: bold; color: {cor_texto};'>
                    {score}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.caption("🎯 Ranking atualizado em tempo real")
