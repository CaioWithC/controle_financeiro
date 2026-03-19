from datetime import datetime
from decimal import Decimal
from sqlalchemy import extract, func
from db import SessionLocal
from models import Categoria, Transacao


def criar_categoria(nome: str, tipo: str):
    session = SessionLocal()
    try:
        categoria_existente = session.query(Categoria).filter(Categoria.nome.ilike(nome)).first()
        if categoria_existente:
            print("Categoria já existe.")
            return

        categoria = Categoria(nome=nome, tipo=tipo)
        session.add(categoria)
        session.commit()
        print("Categoria cadastrada com sucesso.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar categoria: {e}")
    finally:
        session.close()

def input_nome_pessoa():
    while True:
        nome = input("Nome da pessoa: ").strip()

        if not nome:
            print("Nome não pode ser vazio.")
            continue

        if len(nome) < 2:
            print("Nome muito curto.")
            continue

        return nome.title()


def listar_categorias(tipo: str | None = None):
    session = SessionLocal()
    try:
        query = session.query(Categoria)
        if tipo:
            query = query.filter(Categoria.tipo == tipo)

        categorias = query.order_by(Categoria.nome).all()

        if not categorias:
            print("Nenhuma categoria encontrada.")
            return []

        for categoria in categorias:
            print(f"{categoria.id} - {categoria.nome} ({categoria.tipo})")
        return categorias
    finally:
        session.close()


def criar_transacao(
    descricao: str,
    valor: float,
    data_str: str,
    tipo: str,
    categoria_id: int,
    forma_pagamento: str,
    status: str,
    nome_pessoa: str,
):
    session = SessionLocal()
    try:
        categoria = session.query(Categoria).filter(Categoria.id == categoria_id).first()
        if not categoria:
            print("Categoria não encontrada.")
            return

        if categoria.tipo != tipo:
            print("A categoria escolhida não combina com o tipo da transação.")
            return

        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()

        transacao = Transacao(
            descricao=descricao,
            valor=Decimal(str(valor)),
            data=data_obj,
            tipo=tipo,
            categoria_id=categoria_id,
            forma_pagamento=forma_pagamento,
            status=status,
            nome_pessoa=nome_pessoa,
        )
        session.add(transacao)
        session.commit()
        print("Transação cadastrada com sucesso.")
    except ValueError:
        print("Data inválida. Use o formato YYYY-MM-DD.")
        session.rollback()
    except Exception as e:
        session.rollback()
        print(f"Erro ao criar transação: {e}")
    finally:
        session.close()


def listar_transacoes():
    session = SessionLocal()
    try:
        transacoes = (
            session.query(Transacao)
            .join(Categoria)
            .order_by(Transacao.data.desc(), Transacao.id.desc())
            .all()
        )

        if not transacoes:
            print("Nenhuma transação cadastrada.")
            return

        for t in transacoes:
            print(
                f"[{t.id}] {t.data} | {t.nome_pessoa} | {t.tipo.upper()} | {t.descricao} | "
                f"R$ {t.valor} | {t.categoria.nome} | {t.forma_pagamento or '-'} | {t.status}"
            )
    finally:
        session.close()


def resumo_mes(ano: int, mes: int):
    session = SessionLocal()
    try:
        total_receitas = (
            session.query(func.coalesce(func.sum(Transacao.valor), 0))
            .filter(Transacao.tipo == "receita")
            .filter(extract("year", Transacao.data) == ano)
            .filter(extract("month", Transacao.data) == mes)
            .scalar()
        )

        total_despesas = (
            session.query(func.coalesce(func.sum(Transacao.valor), 0))
            .filter(Transacao.tipo == "despesa")
            .filter(extract("year", Transacao.data) == ano)
            .filter(extract("month", Transacao.data) == mes)
            .scalar()
        )

        pendentes = (
            session.query(func.coalesce(func.sum(Transacao.valor), 0))
            .filter(Transacao.status == "pendente")
            .filter(extract("year", Transacao.data) == ano)
            .filter(extract("month", Transacao.data) == mes)
            .scalar()
        )

        saldo = total_receitas - total_despesas

        print("\n=== RESUMO DO MÊS ===")
        print(f"Ano/Mês: {ano}-{mes:02d}")
        print(f"Total de receitas: R$ {total_receitas}")
        print(f"Total de despesas: R$ {total_despesas}")
        print(f"Saldo do mês:      R$ {saldo}")
        print(f"Pendentes:         R$ {pendentes}")
    finally:
        session.close()


def deletar_transacao(transacao_id: int):
    session = SessionLocal()
    try:
        transacao = session.query(Transacao).filter(Transacao.id == transacao_id).first()
        if not transacao:
            print("Transação não encontrada.")
            return

        session.delete(transacao)
        session.commit()
        print("Transação removida com sucesso.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao deletar transação: {e}")
    finally:
        session.close()