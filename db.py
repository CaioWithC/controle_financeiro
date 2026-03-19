from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Altere usuário, senha, host, porta e banco conforme o seu PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/bancodedados"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()