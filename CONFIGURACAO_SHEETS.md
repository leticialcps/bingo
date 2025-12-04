# 📊 Guia de Configuração: Google Sheets

## ✅ Passo 1: Cole as Secrets no Streamlit Cloud

Depois do deploy, vá em **Settings > Secrets** e cole:

```toml
[gcp_service_account]
type = "service_account"
project_id = "projetoswifitiesidosos"
private_key_id = "7356cf7fca71e95ab4f5576c76b07ff7db4e4dab"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDYnB510tVDVm7A\nDKZPKbCQpyevQpYQhiDHMZSkY2WoffA5AhIpOSQiFJKnTZ30a7+peZ/JfEOAhouQ\nMoxIYp3CmX4tykdHFI2o72PnVrH/A/OS8hqNkuFjl3nw2/1At47QqcbwKeqJS4vU\nZooDx7LEBbfal4mfp3ZeeA5otKG+ffkacMO/qaC4WtUunfuk9ne8r0zE277UrjgY\nxPGGTTt+bJSkw2aacYC4qhWbDDDxRQpFTvgZA4RiEaimD0Jv1rIP0RcIIIempDpo\nd/h1pShfUMN47Rf6uduwz/P7CDYAX/gM1CVau4pXCynvyAZWqIE3r6zphdf9Cgvd\nX6VDstFAgMBAAECggEAD+ZBvB9KJSOyhGlJSdVDDxMd8Bjgn/zgag6jHP/oxdnc\nqKqUv67gjpnY++vQFNFV47A4QNdcsxHtK5vyPRvz/YU7xEutOLPzA/vyZtgvv4rA\nNcCMn2ixH5jOTBYxvC7dDkbwAc/p1cMUU/Zk2gst/YJ38NUftnbZ0uxYDmp31t4Q\npzBDsyC1fDvZv3zkzgjZVWOU4cLbPAOB/6oCLWwvCs+cgB/bXvBSsOwlYOhXxUaw\n1p1jamcs2ngG4+y0BAIMCeCf0ejF79WE2vb1OLPN6vyOxCG1R4P0RjDHB2cI69W2\nTeGLa+VjuaePe+61XS3Fsc9KNE0eq1+QExTfjDY7HwKBgQD7FylFHLLJQc9saEx6\n/cbfLs9aO+xLtx2CAdfLHI1sPOliylJ4ztixsvJ7KDoI/CIjrhj3jm/2XYqtCBTK\n+xTUewC+2xBj3MTFtqFeSQ8p9Y9iLpmJoMvWfHwLPUwzzXIZJ1liuNi/fO6YHpJA\nQPid2nnWX5IkJ5efbHOk98+vSwKBgQDc2F09Xyu05tdMLd720zb5NcdYxeH1nDw6\nkF3zpdarCsVM2SvoI3luLltjlDq3xRwwd1JrF7q8QWnvFkv/hUBOdVqeO/xFfutQ\nKYGoeyH5eZ2GZikDjLZ/6jhwAk0PiWZLDgnzb3kSDcvwRxNF/2HFvpkdC+Pzqveu\negARYYyFrwKBgDt4Ftw5mda08Y25fjO7G3kMuyuh+atNKX37NcLzdkNmgdhWFwZp\n50TfHzMwKd6q6OMOfvdTEw2Exi2JNnOE2EAjCeAqPk2Ioko5oSqVnzPO5zDX3KGO\nJfkc7rwyvnOeeyGeAjuxkBR6YIBC7VyuhrPMZQLzC8foYK7vnsw5rUTVAoGAD4Oz\nqSgSbfb5kQR38WcNKZy5kGb2ZMbBBGw37XHtDr8G9UscZoZ3dWIUUX6MUXSrckwv\nog5cs/T0eDNcy2qVBe4Am7UjF86+wTbpQOjFjj0Y7+QlZXZxK7NMm7HNsBW69fLa\niBuAqeAGP67+j6BNQhMNtpirPub3124CqzXrJUkCgYEAplehvRJ2t7rZG97JpnTF\nZvdEip3MnQ0FRrYXnPkFUiE5nfu+YjO6J9S4FtqZyAefI5U3I1W9DwYjMxS+HOIC\niUz+tKAgfebbkPKmiUwszc2qqytSmwTA0+buo6sOW34jZUd7WJRBMhBPy08RQd1Z\nL+mHQ6rz7VRy8VGjE6rFXco=\n-----END PRIVATE KEY-----\n"
client_email = "bingo-idosos@projetoswifitiesidosos.iam.gserviceaccount.com"
client_id = "108829760319174017046"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/bingo-idosos%40projetoswifitiesidosos.iam.gserviceaccount.com"
universe_domain = "googleapis.com"

sheet_name = "dados_amigosecreto_idosos"
```

---

## ✅ Passo 2: Criar e Configurar a Planilha

### Opção A: Criar Nova Planilha

1. Vá em [Google Sheets](https://sheets.google.com)
2. Crie uma nova planilha
3. **Renomeie para:** `dados_amigosecreto_idosos`
4. Clique em **"Compartilhar"** (botão azul no canto superior direito)
5. Adicione o email: `bingo-idosos@projetoswifitiesidosos.iam.gserviceaccount.com`
6. Dê permissão de **"Editor"**
7. Clique em **"Enviar"**

### Opção B: Usar Planilha Existente

Se você já tem uma planilha chamada `dados_amigosecreto_idosos`:

1. Abra a planilha
2. Clique em **"Compartilhar"**
3. Adicione: `bingo-idosos@projetoswifitiesidosos.iam.gserviceaccount.com`
4. Permissão: **"Editor"**

---

## 📋 Estrutura das Abas (serão criadas automaticamente)

A planilha terá estas abas:

### 1. **participantes**
Armazena a lista de personagens e nomes reais.

| key | value |
|-----|-------|
| personagens | ["Personagem1", "Personagem2", ...] |
| nomes_reais | ["Nome1", "Nome2", ...] |

### 2. **apostas**
Armazena as apostas de cada código.

| key | value |
|-----|-------|
| codigo123 | {"Personagem1": "Nome1", "Personagem2": "Nome2"} |
| codigo456 | {"Personagem1": "Nome3", "Personagem2": "Nome4"} |

### 3. **revelacoes**
Armazena as revelações oficiais.

| key | value |
|-----|-------|
| Personagem1 | Nome1 |
| Personagem2 | Ainda não revelado |

### 4. **identidades**
Armazena fotos dos personagens.

| key | value |
|-----|-------|
| Personagem1 | {"foto": "url_da_foto"} |

### 5. **codigos_identidade**
Armazena vínculo código → nome real.

| key | value |
|-----|-------|
| codigo123 | Nome Real 1 |
| codigo456 | Nome Real 2 |

---

## 🔄 Como Funciona a Conversão JSON → Google Sheets

O sistema converte automaticamente:

### De JSON para Sheets:
```json
{
  "codigo123": {
    "Personagem1": "Nome1",
    "Personagem2": "Nome2"
  }
}
```

Vira na planilha:

| key | value |
|-----|-------|
| codigo123 | {"Personagem1": "Nome1", "Personagem2": "Nome2"} |

### De Sheets para JSON:
A leitura faz o caminho inverso, reconstruindo o objeto JSON original.

---

## ✅ Testando a Integração

Após configurar:

1. **Acesse o app** no Streamlit Cloud
2. **Faça uma aposta** ou **cadastre dados**
3. **Abra a planilha** no Google Sheets
4. Você verá as abas sendo criadas automaticamente
5. Os dados aparecerão em tempo real!

---

## 🆘 Solução de Problemas

### ❌ "Planilha não encontrada"
- Verifique se o nome é exatamente: `dados_amigosecreto_idosos`
- Certifique-se de compartilhar com o email correto
- Dê permissão de "Editor", não apenas "Visualizador"

### ❌ "Permission denied"
- Verifique se compartilhou a planilha com: `bingo-idosos@projetoswifitiesidosos.iam.gserviceaccount.com`
- Certifique-se de que a permissão é "Editor"

### ⚠️ "Usando arquivos locais"
- As secrets ainda não foram configuradas no Streamlit Cloud
- Vá em Settings > Secrets e cole as credenciais

---

## 🎉 Pronto!

Agora seu app está 100% integrado com Google Sheets e todos os dados ficarão salvos permanentemente!

**Dúvidas?** Consulte `GOOGLE_SHEETS_SETUP.md` para mais detalhes.
