import csv
import random
from pathlib import Path

random.seed(42)

DESTINO = Path("01_data/clientes_teste_10000.csv")
TOTAL = 10_000

nomes = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo",
    "Fernanda", "Gabriel", "Helena", "Igor", "Juliana",
    "Lucas", "Mariana", "Nicolas", "Olivia", "Paulo",
]

sobrenomes = [
    "Silva", "Santos", "Oliveira", "Souza", "Lima",
    "Costa", "Pereira", "Ferreira", "Almeida", "Ribeiro",
]

clientes = []

for i in range(1, TOTAL + 1):
    nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    idade = random.randint(18, 80)
    email = f"cliente{i}@email.com"

    clientes.append({
        "id_cliente": i,
        "nome": nome,
        "idade": idade,
        "email": email,
    })

# Problemas controlados para testar o agente
for i in random.sample(range(TOTAL), 100):
    clientes[i]["email"] = ""

for i in random.sample(range(TOTAL), 80):
    clientes[i]["email"] = f"email_invalido_{i}"

for i in random.sample(range(TOTAL), 50):
    clientes[i]["idade"] = ""

for i in random.sample(range(TOTAL), 40):
    clientes[i]["idade"] = random.choice([10, 15, 110, 150])

# 30 IDs duplicados intencionais
for i in range(30):
    clientes[TOTAL - 30 + i]["id_cliente"] = clientes[i]["id_cliente"]

DESTINO.parent.mkdir(parents=True, exist_ok=True)

with DESTINO.open("w", newline="", encoding="utf-8") as arquivo:
    writer = csv.DictWriter(
        arquivo,
        fieldnames=["id_cliente", "nome", "idade", "email"]
    )
    writer.writeheader()
    writer.writerows(clientes)

print(f"Dataset criado: {DESTINO}")
print(f"Registros: {TOTAL}")
print("Problemas inseridos: emails ausentes/inválidos, idades ausentes/fora do intervalo e IDs duplicados.")
