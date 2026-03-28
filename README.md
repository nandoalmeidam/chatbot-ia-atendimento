# Chatbot IA de Atendimento

Sistema de atendimento automático com IA usando FastAPI + interface estilo WhatsApp.

---

## Preview do Sistema

<p align="center">
  <img src="assets/chat.png" width="300"/>
</p>

---

## Tecnologias
- Python
- FastAPI
- HTML, CSS, JavaScript
- Groq API

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
pip install fastapi uvicorn python-dotenv groq
```

### 5. Rodar backend

```bash
uvicorn main:app --reload
```

### 6. Rodar frontend

Abrir index.html com Live Server