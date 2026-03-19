from db import Base, engine
from crud import (
    criar_categoria,
    listar_categorias,
    criar_transacao,
    listar_transacoes,
    resumo_mes,
    deletar_transacao,
)

Base.metadata.create_all(bind=engine)


def menu():
    while True:
        print("\n=== CONTROLE FINANCEIRO DOMÉSTICO ===")
        print("1 - Criar categoria")
        print("2 - Listar categorias")
        print("3 - Adicionar transação")
        print("4 - Listar transações")
        print("5 - Ver resumo do mês")
        print("6 - Deletar transação")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome da categoria: ").strip()
            tipo = input("Tipo (receita/despesa): ").strip().lower()

            if tipo not in ["receita", "despesa"]:
                print("Tipo inválido.")
                continue

            criar_categoria(nome, tipo)

        elif opcao == "2":
            filtro = input("Filtrar por tipo? (receita/despesa ou Enter para todos): ").strip().lower()
            if filtro == "":
                filtro = None
            listar_categorias(filtro)

        elif opcao == "3":
            nome_pessoa = input(str("Nome da Pessoa: "))
            descricao = input("Descrição: ").strip()
            valor = float(input("Valor: ").replace(",", "."))
            data = input("Data (YYYY-MM-DD): ").strip()
            tipo = input("Tipo (receita/despesa): ").strip().lower()

            if tipo not in ["receita", "despesa"]:
                print("Tipo inválido.")
                continue

            print("\nCategorias disponíveis:")
            listar_categorias(tipo)

            categoria_id = int(input("ID da categoria: "))
            forma_pagamento = input("Forma de pagamento (dinheiro, pix, cartão...): ").strip()
            status = input("Status (pago/pendente): ").strip().lower()

            if status not in ["pago", "pendente"]:
                print("Status inválido.")
                continue

            criar_transacao(
                descricao=descricao,
                valor=valor,
                data_str=data,
                tipo=tipo,
                categoria_id=categoria_id,
                forma_pagamento=forma_pagamento,
                status=status,
                nome_pessoa=nome_pessoa,
            )

        elif opcao == "4":
            listar_transacoes()

        elif opcao == "5":
            ano = int(input("Ano: "))
            mes = int(input("Mês (1-12): "))
            resumo_mes(ano, mes)

        elif opcao == "6":
            transacao_id = int(input("ID da transação para deletar: "))
            deletar_transacao(transacao_id)

        elif opcao == "0":
            print("Encerrando o sistema.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()