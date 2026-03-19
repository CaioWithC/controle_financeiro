from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    tipo = Column(String(20), nullable=False)  # receita ou despesa

    transacoes = relationship("Transacao", back_populates="categoria")


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(Date, nullable=False)
    tipo = Column(String(20), nullable=False)  # receita ou despesa
    nome_pessoa = Column(String(100), nullable=False)
    forma_pagamento = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="pago")  # pago ou pendente

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("Categoria", back_populates="transacoes")