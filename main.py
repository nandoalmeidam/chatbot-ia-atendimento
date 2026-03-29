from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal
from models import MensagemDB

# controle
estado_usuario = {}

# Carregar variáveis do .env
load_dotenv()

# Inicializar app
app = FastAPI()

# Liberar acesso do frontend (HTML/JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # em produção, restringir domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa cliente de IA (Groq)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Memória simples (armazena histórico por usuário)
historico_conversas = {}

# Modelo de entrada
class Mensagem(BaseModel):
    texto: str
    usuario: str = "default"


def texto_menu():
    return """Olá! 👋

Digite o número da opção:

1️⃣ Atendimento
2️⃣ Horários
3️⃣ Serviços
4️⃣ Falar com atendente
5️⃣ Sair

A qualquer momento, digite *menu* para voltar ao menu."""


# Função principal
def gerar_resposta(pergunta, usuario):
    pergunta_lower = pergunta.lower().strip()

    # Salvar no banco
    db = SessionLocal()
    try:
        db.add(MensagemDB(usuario=usuario, texto=pergunta))
        db.commit()
    finally:
        db.close()

    # Inicializa histórico e estado se não existir
    if usuario not in historico_conversas:
        historico_conversas[usuario] = []

    if usuario not in estado_usuario:
        estado_usuario[usuario] = "inicio"

    historico = historico_conversas[usuario]

    # Menu Inicial
    if pergunta_lower in ["menu", "oi", "olá", "ola"]:
        estado_usuario[usuario] = "menu"
        return texto_menu()

    # Confirmação de localização
    if estado_usuario[usuario] == "confirmar_localizacao":
        if pergunta_lower in ["sim", "s", "claro", "manda", "mande"]:
            estado_usuario[usuario] = "atendimento"
            return """Aqui está nossa localização:
https://maps.google.com/?q=avenida+paulista+sao+paulo

Se quiser, digite *menu* para voltar ao menu."""

        elif pergunta_lower in ["não", "nao"]:
            estado_usuario[usuario] = "atendimento"
            return "Tudo bem! Posso te ajudar com outra coisa 😊\n\n(Digite *menu* para voltar ao menu.)"

    # Opções do Menu
    if estado_usuario[usuario] == "menu":

        if pergunta_lower == "1":
            estado_usuario[usuario] = "atendimento"
            return "Claro! Me diga qual é sua dúvida 😊\n\n(Digite *menu* para voltar ao menu.)"

        elif pergunta_lower == "2":
            return "Nosso horário é de segunda a sexta, das 8h às 18h.\n\n(Digite *menu* para voltar ao menu.)"

        elif pergunta_lower == "3":
            return "Oferecemos desenvolvimento de software, consultoria e suporte técnico.\n\n(Digite *menu* para voltar ao menu.)"

        elif pergunta_lower == "4":
            return "Um atendente humano irá assumir. Aguarde...\n\n(Digite *menu* para voltar ao menu.)"

        elif pergunta_lower == "5":
            estado_usuario[usuario] = "inicio"
            return "Certo! Encerramos por aqui. Quando quiser voltar, é só digitar *oi* ou *menu*."

        else:
            return "Opção inválida. Digite 1, 2, 3, 4 ou 5.\n\n(Digite *menu* para voltar ao menu.)"

    # Atendimento
    if estado_usuario[usuario] == "atendimento":

        # permitir opções úteis mesmo fora do menu
        if pergunta_lower == "2":
            return "Nosso horário é de segunda a sexta, das 8h às 18h.\n\n(Digite *menu* para voltar ao menu.)"

        if pergunta_lower == "3":
            return "Oferecemos desenvolvimento de software, consultoria e suporte técnico.\n\n(Digite *menu* para voltar ao menu.)"

        if pergunta_lower == "4":
            return "Um atendente humano irá assumir. Aguarde...\n\n(Digite *menu* para voltar ao menu.)"

        if pergunta_lower == "5":
            estado_usuario[usuario] = "inicio"
            return "Certo! Encerramos por aqui. Quando quiser voltar, é só digitar *oi* ou *menu*."

        # perguntar localização
        if "localização" in pergunta_lower or "onde fica" in pergunta_lower:
            estado_usuario[usuario] = "confirmar_localizacao"
            return "Estamos na região da Avenida Paulista. Quer que eu te envie o link do Google Maps?\n\n(Digite *menu* para voltar ao menu.)"

        # endereço
        if "endereço" in pergunta_lower:
            return "Estamos localizados em São Paulo. Posso te enviar a localização exata se quiser!\n\n(Digite *menu* para voltar ao menu.)"

        # atendimento humano
        if "atendente" in pergunta_lower or "humano" in pergunta_lower:
            return "Perfeito! Vou te encaminhar para um atendente humano. Aguarde um momento, por favor.\n\n(Digite *menu* para voltar ao menu.)"

        # horário
        if "horário" in pergunta_lower or "funcionamento" in pergunta_lower:
            return "Nosso horário de funcionamento é de segunda a sexta, das 8h às 18h, e aos sábados, das 9h às 13h.\n\n(Digite *menu* para voltar ao menu.)"

        # serviços
        if "serviço" in pergunta_lower or "oferecem" in pergunta_lower:
            return "Oferecemos desenvolvimento de software, consultoria em tecnologia e suporte técnico. Quer saber mais sobre algum?\n\n(Digite *menu* para voltar ao menu.)"

    # IA - Fallback inteligente
    historico.append({"role": "user", "content": pergunta})

    try:
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um atendente profissional de WhatsApp. Responda de forma curta, direta e natural, como uma empresa real. Ao final, lembre de forma breve que o usuário pode digitar menu para voltar."
                },
                *historico[-6:]
            ],
            max_tokens=120
        )

        resposta_texto = resposta.choices[0].message.content
        historico.append({"role": "assistant", "content": resposta_texto})

        return resposta_texto

    except Exception as e:
        print("ERRO REAL:", e)
        return "Desculpe, tivemos um problema ao processar sua mensagem. Pode tentar novamente?\n\n(Digite *menu* para voltar ao menu.)"


# Endpoint whatsapp (Twilio)
@app.post("/whatsapp")
async def whatsapp(Body: str = Form(...), From: str | None = Form(None)):
    """
    Endpoint que recebe mensagens do Twilio (WhatsApp)
    e retorna resposta no formato XML.
    """
    usuario = From if From else "whatsapp_user"
    resposta_texto = gerar_resposta(Body, usuario)

    # Cria resposta Twilio
    resp = MessagingResponse()
    resp.message(resposta_texto)

    # Retorna XML (Obrigatório para o Twilio)
    return Response(
        content=str(resp),
        media_type="application/xml"
    )

# Endpoint chat web
@app.post("/chat")
async def chat(msg: Mensagem):
    resposta = gerar_resposta(msg.texto, msg.usuario)
    return {"resposta": resposta}