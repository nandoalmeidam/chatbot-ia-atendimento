from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

# 🔧 Carregar variáveis do .env
load_dotenv()

# Inicializar app
app = FastAPI()

# Liberar acesso do frontend (HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Memória simples (por usuário)
historico_conversas = {}

# Modelo de entrada
class Mensagem(BaseModel):
    texto: str
    usuario: str = "default"

# Função principal
def gerar_resposta(pergunta, usuario):
    pergunta_lower = pergunta.lower()

    # Inicializa histórico do usuário
    if usuario not in historico_conversas:
        historico_conversas[usuario] = []

    historico = historico_conversas[usuario]

    # =========================
    # REGRAS (ORDEM IMPORTA)
    # =========================

    # localização EXATA
    if "mande" in pergunta_lower and "localização" in pergunta_lower:
        return "Claro! Aqui está nossa localização no Google Maps: https://maps.google.com/?q=avenida+paulista+sao+paulo"

    # perguntar localização
    if "localização" in pergunta_lower or "onde fica" in pergunta_lower:
        return "Estamos na região da Avenida Paulista. Quer que eu te envie o link do Google Maps?"

    # endereço
    if "endereço" in pergunta_lower:
        return "Estamos localizados em São Paulo. Posso te enviar a localização exata se quiser!"

    # atendimento humano
    if "atendente" in pergunta_lower or "humano" in pergunta_lower:
        return "Perfeito! Vou te encaminhar para um atendente humano. Aguarde um momento, por favor."

    # horário
    if "horário" in pergunta_lower or "funcionamento" in pergunta_lower:
        return "Nosso horário de funcionamento é de segunda a sexta, das 8h às 18h, e aos sábados, das 9h às 13h."

    # serviços
    if "serviço" in pergunta_lower or "oferecem" in pergunta_lower:
        return "Oferecemos desenvolvimento de software, consultoria em tecnologia e suporte técnico. Quer saber mais sobre algum?"

    # =========================
    # IA COM CONTEXTO
    # =========================

    # adiciona pergunta ao histórico
    historico.append({"role": "user", "content": pergunta})

    try:
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um atendente profissional de WhatsApp. Responda de forma curta, direta e natural, como uma empresa real."
                },
                *historico[-6:]  # últimas mensagens (memória curta)
            ],
            max_tokens=120
        )

        resposta_texto = resposta.choices[0].message.content

        # salva resposta no histórico
        historico.append({"role": "assistant", "content": resposta_texto})

        return resposta_texto

    except Exception as e:
        print("ERRO REAL:", e)
        return "Desculpe, tivemos um problema ao processar sua mensagem. Pode tentar novamente?"

# Endpoint
@app.post("/chat")
def chat(msg: Mensagem):
    resposta = gerar_resposta(msg.texto, msg.usuario)
    return {"resposta": resposta}