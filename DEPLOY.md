# 🚀 Guia Rápido de Deploy

## Opção 1: Deploy Rápido (5 minutos)

Se você quer testar o app rapidamente sem se preocupar com persistência de dados:

### Passo 1: Fazer push do código

```bash
git add .
git commit -m "App Bingo pronto para deploy"
git push origin AlteracoesPrincipais1
```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione:
   - Repository: `leticialcps/bingo`
   - Branch: `AlteracoesPrincipais1`
   - Main file path: `streamlit_app.py`
5. Clique em "Deploy!"

### Passo 3: Compartilhe o link

Após o deploy, você receberá um link como:
```
https://seu-app.streamlit.app
```

Compartilhe esse link com seus amigos!

⚠️ **Limitação**: Os dados serão armazenados em arquivos JSON temporários e podem ser perdidos se o app reiniciar.

---

## Opção 2: Deploy com Google Sheets (15 minutos)

Para ter persistência garantida dos dados e permitir que vários amigos usem simultaneamente:

### Siga o tutorial completo:
👉 [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)

### Vantagens:
✅ Dados nunca se perdem  
✅ Você pode ver/editar os dados na planilha  
✅ Múltiplos usuários simultâneos  
✅ Backup automático  
✅ Completamente gratuito!  

---

## Testando Localmente Antes do Deploy

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o app
streamlit run streamlit_app.py
```

O app abrirá em `http://localhost:8501`

---

## Configurações Importantes

### Alterar a senha de admin

Edite `streamlit_app.py` e procure por:
```python
if senha == "admin123":  # você pode trocar
```

Mude `"admin123"` para sua senha preferida.

### Customizar data de revelação

Para alterar a data especial (atualmente 14/12), procure por:
```python
pode_vincular = (hoje.day == 14 and hoje.month == 12)
```

E altere para sua data desejada.

---

## Solução de Problemas

### App não está carregando
- Verifique se todas as dependências foram instaladas
- Veja os logs no Streamlit Cloud para mensagens de erro

### Dados não estão sendo salvos
- Se não configurou Google Sheets, os dados são salvos em arquivos JSON temporários
- Configure Google Sheets seguindo [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)

### Erro de módulo não encontrado
```bash
pip install -r requirements.txt --upgrade
```

---

## Próximos Passos

Após o deploy:

1. **Teste o app** você mesmo primeiro
2. **Configure a senha de admin** para algo seguro
3. **Compartilhe o link** com seus amigos
4. **Acompanhe o ranking** conforme as revelações acontecem!

🎉 Divirta-se!
