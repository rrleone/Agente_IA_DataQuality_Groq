
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API Key não encontrada no arquivo .env")

client = Groq(api_key=api_key)

MODELO = "openai/gpt-oss-20b"

print(f"Conectando ao Groq com o modelo {MODELO}...")

response = client.chat.completions.create(
    model=MODELO,
    messages=[
        {
            "role": "user",
            "content": "Responda apenas: Agente de IA conectado com sucesso!"
        }
    ],
    max_tokens=100
)

print("\nResposta do Groq:")
print(response.choices[0].message.content)
