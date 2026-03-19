from flask import Flask, render_template, request, redirect, url_for
from db import SessionLocal, engine, Base
from models import Categoria, Transacao
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)

Base.metadata.create_all(bind=engine)


@app.route("/")
def index():
    session = SessionLocal()
    try:
        transacoes = (
            session.query(Transacao)
            .join(Categoria)
            .order_by(Transacao.data.desc(), Transacao.id.desc())
            .all()
        )
        return render_template("index.html", transacoes=transacoes)
    finally:
        session.close()


@app.route("/nova-transacao", methods=["GET", "POST"])
def nova_transacao():
    session = SessionLocal()
    try:
        categorias = session.query(Categoria).order_by(Categoria.nome).all()

        if request.method == "POST":
            nome_pessoa = request.form["nome_pessoa"].strip()
            descricao = request.form["descricao"].strip()
            valor = request.form["valor"].replace(",", ".").strip()
            data = request.form["data"].strip()
            tipo = request.form["tipo"].strip()
            categoria_id = request.form["categoria_id"].strip()
            forma_pagamento = request.form["forma_pagamento"].strip()
            status = request.form["status"].strip()

            if not nome_pessoa or not descricao:
                return "Nome da pessoa e descrição são obrigatórios."

            transacao = Transacao(
                nome_pessoa=nome_pessoa.title(),
                descricao=descricao.title(),
                valor=Decimal(valor),
                data=datetime.strptime(data, "%Y-%m-%d").date(),
                tipo=tipo,
                categoria_id=int(categoria_id),
                forma_pagamento=forma_pagamento,
                status=status,
            )

            session.add(transacao)
            session.commit()
            return redirect(url_for("index"))

        return render_template("nova_transacao.html", categorias=categorias)
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)