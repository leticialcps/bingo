# 🎵 Bingo Amigo Secreto Swifties Idosos

Um app interativo de bingo para revelar identidades secretas entre amigos Swifties! Com integração ao Google Sheets para persistência de dados.

## ✨ Funcionalidades

- 🎲 **Fazer Apostas**: Cada participante pode apostar na identidade real de cada personagem
- 🔓 **Revelar Identidades**: Admin pode revelar as identidades verdadeiras
- 🏆 **Ranking**: Pontuação automática e ranking dos participantes
- 📅 **Sistema de Vínculos**: No dia 14/12, participantes podem vincular seu código a um nome real
- 💾 **Persistência via Google Sheets**: Todos os dados são salvos automaticamente no Google Sheets

## 🚀 Deploy no Streamlit Cloud

### Opção Rápida (sem Google Sheets)

1. Faça push do código:
```bash
git add .
git commit -m "Deploy do Bingo"
git push origin AlteracoesPrincipais1
```

2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça o deploy

⚠️ **Atenção**: Sem Google Sheets, os dados podem ser perdidos quando o app reiniciar.

### Opção Recomendada (com Google Sheets)

Para ter persistência garantida dos dados, siga o guia completo:

👉 **[GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)** - Tutorial completo passo a passo

## 🏃 Como rodar localmente

1. Clone o repositório:
```bash
git clone https://github.com/leticialcps/bingo.git
cd bingo
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. (Opcional) Configure Google Sheets:
   - Siga as instruções em [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)
   - Ou rode sem configurar e use os arquivos JSON locais

4. Execute o app:
```bash
streamlit run streamlit_app.py
```

## 📁 Estrutura do Projeto

```
bingo/
├── streamlit_app.py          # App principal
├── sheets_db.py              # Integração com Google Sheets
├── requirements.txt          # Dependências Python
├── apostas.json             # Apostas dos participantes (fallback)
├── revelacoes.json          # Revelações oficiais (fallback)
├── identidades.json         # Identidades dos personagens (fallback)
├── participantes.json       # Lista de participantes e personagens
├── codigos_identidade.json  # Vínculos código → nome real (fallback)
└── .streamlit/
    └── secrets.toml.example # Template para configuração do Google Sheets
```

## 🎮 Como usar

### Para Participantes

1. Acesse o app e vá em **"Fazer Aposta"**
2. Digite seu código (ou gere um novo)
3. **Salve seu código!** Você precisará dele para ver seu ranking
4. No dia **14/12**, você pode vincular seu código ao seu nome real
5. Preencha suas apostas sobre quem é cada personagem
6. Clique em "Salvar minhas apostas"
7. Acompanhe o ranking em **"Ranking"**

### Para Admin

1. Vá em **"Revelar Identidades"**
2. Digite a senha de admin (padrão: `admin123`)
3. Selecione as identidades reais de cada personagem
4. Clique em "Confirmar Revelações"
5. O ranking será atualizado automaticamente!

## 🔐 Segurança

- Senha de admin configurável no código
- Credenciais do Google Sheets protegidas via Streamlit Secrets
- Arquivo `secrets.toml` excluído do Git via `.gitignore`

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/) - Framework web
- [Google Sheets API](https://developers.google.com/sheets/api) - Banco de dados
- [gspread](https://docs.gspread.org/) - Cliente Python para Google Sheets

## 📝 Licença

MIT License - veja [LICENSE](LICENSE) para mais detalhes.

## 🎨 Customização

O app possui um tema visual customizado com:
- Background temático para cada seção
- Título com efeito glitter laranja
- Botões brancos com hover laranja
- Containers com glassmorphism

---

Feito com 💜 para os Swifties Idosos
