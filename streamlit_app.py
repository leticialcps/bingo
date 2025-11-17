import streamlit as st
import json
import uuid
import os
import base64
import mimetypes

# -----------------------------------------------
# Funções utilitárias
# -----------------------------------------------
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


def _rounded_image_html(path, width=120):
    """Retorna um HTML <img> com border-radius aplicado e imagem embutida em base64.
    Usa o caminho do arquivo local `path` e dimensiona para `width` (px).
    """
    try:
        if not path:
            return ""
        with open(path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = "image/png"
        html = f'<img src="data:{mime};base64,{b64}" style="border-radius:50%; width:{width}px; height:{width}px; object-fit:cover;"/>'
        return html
    except Exception:
        return ""

participantes = load_json("participantes.json")
personagens = participantes["personagens"]
nomes_reais = participantes["nomes_reais"]

apostas = load_json("apostas.json")
revelacoes = load_json("revelacoes.json")
identidades = load_json("identidades.json")

st.set_page_config(page_title="Amigo Secreto - Bingo", layout="centered")
st.title("🎁 Bingo Amigo Secreto - Descubra Quem é Quem!")

menu = st.sidebar.radio("Menu", ["Fazer Aposta", "Revelar Identidades", "Ranking"])

# -----------------------------------------------
# Página - Apostas
# -----------------------------------------------
if menu == "Fazer Aposta":

    st.header("🕵️ Faça suas apostas")
    st.write("Você receberá um código anônimo para usar depois no ranking.")

    user_id = st.text_input("Digite seu código (ou deixe em branco para gerar)")

    if not user_id:
        if st.button("Gerar novo código"):
            user_id = uuid.uuid4().hex
            st.success(f"Seu código anônimo é:\n\n*{user_id}*\n\n⚠️ Salve esse código, é sua identidade no jogo!")
            st.stop()

    if user_id:
        st.info(f"Você está apostando como: *{user_id}*")

        # Carrega apostas anteriores (se existirem) e pré-preenche os selectboxes
        aposta_temp = {}
        saved = apostas.get(user_id, {}) if isinstance(apostas, dict) else {}

        st.write("Preencha a possível identidade de cada personagem:")

        for p in personagens:
            default = saved.get(p) if p in saved else None
            if default in nomes_reais:
                idx = nomes_reais.index(default)
            else:
                idx = 0
            sel = st.selectbox(
                f"Quem você acha que é *{p}*?",
                nomes_reais,
                index=idx,
                key=f"ap_{user_id}_{p}"
            )
            aposta_temp[p] = sel

        if st.button("Salvar minhas apostas"):
            apostas[user_id] = aposta_temp
            save_json("apostas.json", apostas)
            st.success("Apostas registradas com sucesso!")

# -----------------------------------------------
# Página - Revelação (Admin)
# -----------------------------------------------
elif menu == "Revelar Identidades":

    st.header("🔓 Revelação Oficial")
    senha = st.text_input("Senha de admin:", type="password")

    if senha == "admin123":  # você pode trocar
        st.success("Acesso liberado!")

        for p in personagens:
            revelacoes[p] = st.selectbox(f"{p} é na verdade:", ["Ainda não revelado"] + nomes_reais)

        if st.button("Confirmar Revelações"):
            save_json("revelacoes.json", revelacoes)
            st.balloons()
            st.success("Revelações registradas!")

    else:
        st.warning("Senha incorreta ou não informada.")

# -----------------------------------------------
# Página - Ranking
# -----------------------------------------------
elif menu == "Ranking":
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
        for i, (player, score, acertados) in enumerate(resultados, 1):
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
            st.write(f"{medalha} *{player}* — {score} pontos")

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
