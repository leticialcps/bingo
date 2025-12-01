# Configuração do Google Sheets para o Bingo

Este app agora usa Google Sheets como banco de dados! Isso garante que os dados persistam mesmo quando o app reiniciar.

## Passo 1: Criar uma conta de serviço no Google Cloud

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto (ou use um existente)
3. Ative a **Google Sheets API** e **Google Drive API**:
   - Vá em "APIs & Services" > "Enable APIs and Services"
   - Pesquise por "Google Sheets API" e clique em "Enable"
   - Pesquise por "Google Drive API" e clique em "Enable"

## Passo 2: Criar credenciais de conta de serviço

1. Vá em "APIs & Services" > "Credentials"
2. Clique em "Create Credentials" > "Service Account"
3. Preencha:
   - **Nome**: Bingo App (ou qualquer nome)
   - **Role**: Editor
4. Clique em "Done"
5. Clique na conta de serviço criada
6. Vá na aba "Keys"
7. Clique em "Add Key" > "Create New Key"
8. Escolha formato **JSON**
9. Baixe o arquivo JSON (você vai usar ele no próximo passo)

## Passo 3: Configurar no Streamlit Cloud

### Opção A: Deploy no Streamlit Cloud (Recomendado)

1. Faça push do código para o GitHub:
```bash
git add .
git commit -m "Adiciona integração com Google Sheets"
git push origin AlteracoesPrincipais1
```

2. Acesse [share.streamlit.io](https://share.streamlit.io)

3. Faça o deploy do app

4. Depois do deploy, clique em "⚙️ Settings" > "Secrets"

5. Cole o conteúdo do arquivo JSON baixado no passo 2 neste formato:

```toml
[gcp_service_account]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "sua-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nsua-private-key-aqui\n-----END PRIVATE KEY-----\n"
client_email = "seu-email@projeto.iam.gserviceaccount.com"
client_id = "seu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/seu-email%40projeto.iam.gserviceaccount.com"

sheet_name = "Bingo Amigo Secreto"
```

**IMPORTANTE:** Copie TODOS os campos do arquivo JSON baixado. A `private_key` deve manter as quebras de linha `\n`.

### Opção B: Testar localmente

1. Crie uma pasta `.streamlit` na raiz do projeto:
```bash
mkdir .streamlit
```

2. Crie o arquivo `.streamlit/secrets.toml` e cole o mesmo conteúdo acima

3. **NUNCA faça commit do arquivo `secrets.toml`!** Ele já está no `.gitignore`

4. Execute o app:
```bash
streamlit run streamlit_app.py
```

## Passo 4: Criar a planilha do Google Sheets

O app criará automaticamente a planilha "Bingo Amigo Secreto" na primeira execução.

Você pode também:
1. Criar manualmente uma planilha no Google Sheets com o nome "Bingo Amigo Secreto"
2. Compartilhar essa planilha com o email da conta de serviço (o `client_email` do JSON)
3. Dar permissão de "Editor" para essa conta

## Como funciona

- O app tentará primeiro usar Google Sheets para armazenar os dados
- Se não conseguir conectar (credenciais inválidas ou ausentes), usará os arquivos JSON locais como fallback
- Cada aba da planilha representa um arquivo JSON:
  - `participantes` → participantes.json
  - `apostas` → apostas.json
  - `revelacoes` → revelacoes.json
  - `identidades` → identidades.json
  - `codigos_identidade` → codigos_identidade.json

## Solução de problemas

### Erro: "Spreadsheet not found"
- Verifique se o nome da planilha no `secrets.toml` está correto
- Ou deixe o app criar automaticamente a planilha

### Erro: "Permission denied"
- Certifique-se de que as APIs (Google Sheets e Drive) estão ativadas no Google Cloud
- Verifique se a planilha foi compartilhada com o `client_email` da conta de serviço

### App está usando JSON ao invés do Google Sheets
- Verifique se o arquivo `secrets.toml` está configurado corretamente
- No Streamlit Cloud, verifique se os secrets foram adicionados nas configurações
- Veja os logs do app para mensagens de erro específicas

## Vantagens do Google Sheets

✅ Dados persistentes (nunca se perdem)  
✅ Você pode ver e editar os dados diretamente na planilha  
✅ Backup automático do Google  
✅ Múltiplos usuários simultâneos  
✅ Gratuito!  
