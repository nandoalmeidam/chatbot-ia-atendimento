# Chatbot IA de Atendimento via Whatsapp

Projeto de chatbot inteligente para automação de atendimento, integrando IA com interface web e comunicação via WhatsApp.

---

## Preview do Sistema

<p align="center">
  <img src="assets/chat.png" width="300"/>
</p>

---

## Funcionalidades

- Atendimento automático com IA
- Respostas baseadas em regras (horário, serviços, localização)
- Integração com WhatsApp (Twilio Sandbox)
- Interface web estilo chat
- Memória de conversa por usuário
- Fallback inteligente com IA (Groq)

---

## Fluxo do Sistema

Usuário → WhatsApp → Twilio → FastAPI → IA → resposta → WhatsApp

---

## Tecnologias
- Python
- FastAPI
- HTML, CSS, JavaScript
- Groq API
- Twilio API
- ngrok

---

## Como rodar

### 1. Clonar o projeto

```bash
git clone https://github.com/nandoalmeidam/chatbot-ia-atendimento
cd chatbot-ia-atendimento
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar ambiente

## Windows:
```bash
.venv\Scripts\activate
```

## Mac/Linux:
```bash
source .venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Criar um arquivo .env
GROQ_API_KEY=sua_chave_aqui

### 6. Rodar backend

```bash
uvicorn main:app --reload
```

### 7. Expor servidor (ngrok)

ngrok http 8000

### 8. Configurar Twilio

- Acesse o painel do Twilio
- Vá em "Send a WhatsApp message"
- Configure o seu webhook:
https://SEU_NGROK/whatsapp
