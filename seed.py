from db import Base, engine
from crud import criar_categoria

Base.metadata.create_all(bind=engine)

categorias_iniciais = [
    ("Salário", "receita"),
    ("Renda Extra", "receita"),
    ("Mercado", "despesa"),
    ("Água", "despesa"),
    ("Luz", "despesa"),
    ("Internet", "despesa"),
    ("Aluguel", "despesa"),
    ("Remédios", "despesa"),
    ("Transporte", "despesa"),
]

for nome, tipo in categorias_iniciais:
    criar_categoria(nome, tipo)

print("Banco e categorias iniciais criados com sucesso.")