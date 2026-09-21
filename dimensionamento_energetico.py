from datetime import datetime

# ============================================================
# DIMENSIONAMENTO ENERGÉTICO
# Sistema em memória baseado nas User Stories US01 até US13
# ============================================================

clientes = []
imoveis = []

equipamentos = [
    {"id": 1, "nome": "Televisão", "categoria": "Eletrônico", "potencia": 100},
    {"id": 2, "nome": "Geladeira", "categoria": "Eletrodoméstico", "potencia": 200},
    {"id": 3, "nome": "Ventilador", "categoria": "Climatização", "potencia": 80},
    {"id": 4, "nome": "Micro-ondas", "categoria": "Eletrodoméstico", "potencia": 1200},
    {"id": 5, "nome": "Chuveiro", "categoria": "Aquecimento", "potencia": 5500},
]

# Perfis previstos no documento:
# 1 = Usuário/Morador
# 2 = Gerente
# 3 = Administrador


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def linha():
    print("-" * 55)


def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            return valor
        except ValueError:
            print("Valor inválido! Digite um número inteiro.")


def ler_float(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))

            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Digite um valor menor ou igual a {maximo}.")
                continue

            return valor
        except ValueError:
            print("Valor inválido! Digite um número.")


def ler_texto_obrigatorio(mensagem):
    while True:
        texto = input(mensagem).strip()

        if texto:
            return texto

        print("Este campo é obrigatório.")


def confirmar(mensagem="Confirma a operação? (S/N): "):
    return input(mensagem).strip().upper() == "S"


def buscar_cliente(codigo):
    for cliente in clientes:
        if cliente["codigo"] == codigo:
            return cliente

    return None


def buscar_imovel(codigo):
    for imovel in imoveis:
        if imovel["codigo"] == codigo:
            return imovel

    return None


def buscar_equipamento(equipamento_id):
    for equipamento in equipamentos:
        if equipamento["id"] == equipamento_id:
            return equipamento

    return None


def gerar_id_equipamento():
    if not equipamentos:
        return 1

    maior_id = 0

    for equipamento in equipamentos:
        if equipamento["id"] > maior_id:
            maior_id = equipamento["id"]

    return maior_id + 1


def calcular_consumo(potencia, quantidade, horas):
    # C = (P x Q x H x 30) / 1000
    return (potencia * quantidade * horas * 30) / 1000


def calcular_consumo_total(imovel):
    total = 0

    for equipamento in imovel["equipamentos"]:
        total += equipamento["consumo"]

    return total


def registrar_historico(imovel):
    consumo_total = calcular_consumo_total(imovel)

    registro = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "consumo": consumo_total
    }

    imovel["historico"].append(registro)


# ============================================================
# US01 — CADASTRAR CLIENTE
# ============================================================

def cadastrar_cliente():
    print("\nCADASTRAR CLIENTE")
    linha()

    codigo = input("Código do cliente (6 dígitos): ").strip()

    while len(codigo) != 6 or not codigo.isdigit() or buscar_cliente(codigo) is not None:
        if buscar_cliente(codigo) is not None:
            print("Já existe um cliente com esse código.")
        else:
            print("Código inválido! Digite exatamente 6 números.")

        codigo = input("Código do cliente (6 dígitos): ").strip()

    nome = ler_texto_obrigatorio("Nome completo: ")

    cep = input("CEP (8 dígitos): ").strip()

    while len(cep) != 8 or not cep.isdigit():
        print("CEP inválido! Digite exatamente 8 números.")
        cep = input("CEP (8 dígitos): ").strip()

    cliente = {
        "codigo": codigo,
        "nome": nome,
        "cep": cep
    }

    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")


# ============================================================
# US02 — CONSULTAR CLIENTE
# ============================================================

def consultar_cliente():
    print("\nCONSULTAR CLIENTE")
    linha()

    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
        return

    termo = input("Digite o código ou nome do cliente: ").strip().lower()

    encontrados = []

    for cliente in clientes:
        if termo == cliente["codigo"] or termo in cliente["nome"].lower():
            encontrados.append(cliente)

    if len(encontrados) == 0:
        print("Cliente não encontrado.")
        return

    for cliente in encontrados:
        linha()
        print("Código:", cliente["codigo"])
        print("Nome:", cliente["nome"])
        print("CEP:", cliente["cep"])

        print("Imóveis associados:")

        encontrou_imovel = False

        for imovel in imoveis:
            if imovel["cliente_codigo"] == cliente["codigo"]:
                encontrou_imovel = True
                print(
                    f"  - Código: {imovel['codigo']} | "
                    f"Identificação: {imovel['identificacao']} | "
                    f"CEP: {imovel['cep']}"
                )

        if not encontrou_imovel:
            print("  Nenhum imóvel associado.")


# ============================================================
# US03 — EDITAR CLIENTE
# ============================================================

def editar_cliente():
    print("\nEDITAR CLIENTE")
    linha()

    codigo = input("Código do cliente: ").strip()
    cliente = buscar_cliente(codigo)

    if cliente is None:
        print("Cliente não encontrado.")
        return

    print("Pressione ENTER para manter o valor atual.")

    novo_nome = input(f"Nome [{cliente['nome']}]: ").strip()
    novo_cep = input(f"CEP [{cliente['cep']}]: ").strip()

    if novo_nome:
        cliente["nome"] = novo_nome

    if novo_cep:
        while len(novo_cep) != 8 or not novo_cep.isdigit():
            print("CEP inválido! Digite exatamente 8 números.")
            novo_cep = input("Novo CEP: ").strip()

        cliente["cep"] = novo_cep

    print("Cliente atualizado com sucesso!")


# ============================================================
# US04 — EXCLUIR CLIENTE
# ============================================================

def excluir_cliente():
    print("\nEXCLUIR CLIENTE")
    linha()

    codigo = input("Código do cliente: ").strip()
    cliente = buscar_cliente(codigo)

    if cliente is None:
        print("Cliente não encontrado.")
        return

    for imovel in imoveis:
        if imovel["cliente_codigo"] == codigo:
            print("Não é possível excluir: o cliente possui imóvel cadastrado.")
            return

    print("Cliente selecionado:")
    print("Código:", cliente["codigo"])
    print("Nome:", cliente["nome"])
    print("CEP:", cliente["cep"])

    if confirmar("Deseja realmente excluir este cliente? (S/N): "):
        clientes.remove(cliente)
        print("Cliente excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


# ============================================================
# US05 — CADASTRAR IMÓVEL
# ============================================================

def cadastrar_imovel():
    print("\nCADASTRAR IMÓVEL")
    linha()

    if len(clientes) == 0:
        print("Cadastre um cliente antes de cadastrar um imóvel.")
        return

    cliente_codigo = input("Código do cliente responsável: ").strip()
    cliente = buscar_cliente(cliente_codigo)

    if cliente is None:
        print("Cliente não encontrado.")
        return

    codigo = input("Código do imóvel (6 dígitos): ").strip()

    while len(codigo) != 6 or not codigo.isdigit() or buscar_imovel(codigo) is not None:
        if buscar_imovel(codigo) is not None:
            print("Já existe um imóvel com esse código.")
        else:
            print("Código inválido! Digite exatamente 6 números.")

        codigo = input("Código do imóvel (6 dígitos): ").strip()

    identificacao = ler_texto_obrigatorio(
        "Identificação do imóvel (ex.: Casa, Apartamento): "
    )

    cep = input("CEP do imóvel (8 dígitos): ").strip()

    while len(cep) != 8 or not cep.isdigit():
        print("CEP inválido! Digite exatamente 8 números.")
        cep = input("CEP do imóvel (8 dígitos): ").strip()

    imovel = {
        "codigo": codigo,
        "cliente_codigo": cliente_codigo,
        "identificacao": identificacao,
        "cep": cep,
        "equipamentos": [],
        "historico": []
    }

    imoveis.append(imovel)

    print("Imóvel cadastrado com sucesso!")


# ============================================================
# US06 — VISUALIZAR IMÓVEL
# ============================================================

def mostrar_imovel(imovel):
    cliente = buscar_cliente(imovel["cliente_codigo"])

    linha()
    print("Código do imóvel:", imovel["codigo"])
    print("Identificação:", imovel["identificacao"])
    print("CEP:", imovel["cep"])

    if cliente is not None:
        print("Responsável:", cliente["nome"])
        print("Código do cliente:", cliente["codigo"])

    print("\nEQUIPAMENTOS DO IMÓVEL")

    if len(imovel["equipamentos"]) == 0:
        print("Nenhum equipamento adicionado.")
    else:
        for equipamento in imovel["equipamentos"]:
            linha()
            print("Nome:", equipamento["nome"])
            print("Categoria:", equipamento["categoria"])
            print("Potência:", equipamento["potencia"], "W")
            print("Quantidade:", equipamento["quantidade"])
            print("Uso diário:", equipamento["horas"], "hora(s)")
            print(f"Consumo mensal: {equipamento['consumo']:.2f} kWh/mês")

    linha()
    print(
        f"CONSUMO TOTAL ESTIMADO: "
        f"{calcular_consumo_total(imovel):.2f} kWh/mês"
    )


def visualizar_imovel():
    print("\nVISUALIZAR IMÓVEL")
    linha()

    codigo = input("Código do imóvel: ").strip()
    imovel = buscar_imovel(codigo)

    if imovel is None:
        print("Imóvel não encontrado.")
        return

    mostrar_imovel(imovel)


# ============================================================
# US07 — EDITAR IMÓVEL
# ============================================================

def editar_imovel():
    print("\nEDITAR IMÓVEL")
    linha()

    codigo = input("Código do imóvel: ").strip()
    imovel = buscar_imovel(codigo)

    if imovel is None:
        print("Imóvel não encontrado.")
        return

    print("Pressione ENTER para manter o valor atual.")

    nova_identificacao = input(
        f"Identificação [{imovel['identificacao']}]: "
    ).strip()

    novo_cep = input(f"CEP [{imovel['cep']}]: ").strip()

    if nova_identificacao:
        imovel["identificacao"] = nova_identificacao

    if novo_cep:
        while len(novo_cep) != 8 or not novo_cep.isdigit():
            print("CEP inválido! Digite exatamente 8 números.")
            novo_cep = input("Novo CEP: ").strip()

        imovel["cep"] = novo_cep

    print("Imóvel atualizado com sucesso!")


# ============================================================
# US08 — EXCLUIR IMÓVEL
# ============================================================

def excluir_imovel():
    print("\nEXCLUIR IMÓVEL")
    linha()

    codigo = input("Código do imóvel: ").strip()
    imovel = buscar_imovel(codigo)

    if imovel is None:
        print("Imóvel não encontrado.")
        return

    mostrar_imovel(imovel)

    if len(imovel["equipamentos"]) > 0:
        print("\nATENÇÃO: os vínculos com equipamentos também serão removidos.")

    if confirmar("Deseja realmente excluir este imóvel? (S/N): "):
        imoveis.remove(imovel)
        print("Imóvel excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


# ============================================================
# US09 — VISUALIZAR EQUIPAMENTOS
# ============================================================

def visualizar_equipamentos():
    print("\nEQUIPAMENTOS DISPONÍVEIS")
    linha()

    if len(equipamentos) == 0:
        print("Nenhum equipamento cadastrado.")
        return

    for equipamento in equipamentos:
        print(
            f"ID: {equipamento['id']} | "
            f"Nome: {equipamento['nome']} | "
            f"Categoria: {equipamento['categoria']} | "
            f"Potência: {equipamento['potencia']} W"
        )


# ============================================================
# US10 — CADASTRAR EQUIPAMENTO
# ============================================================

def cadastrar_equipamento():
    print("\nCADASTRAR EQUIPAMENTO")
    linha()

    nome = ler_texto_obrigatorio("Nome do equipamento: ")
    categoria = ler_texto_obrigatorio("Categoria: ")
    potencia = ler_float("Potência nominal em watts (W): ", minimo=0.01)

    equipamento = {
        "id": gerar_id_equipamento(),
        "nome": nome,
        "categoria": categoria,
        "potencia": potencia
    }

    equipamentos.append(equipamento)

    print("Equipamento cadastrado com sucesso!")
    print("ID:", equipamento["id"])


# ============================================================
# US11 — EXCLUIR EQUIPAMENTO
# ============================================================

def excluir_equipamento():
    print("\nEXCLUIR EQUIPAMENTO")
    linha()

    visualizar_equipamentos()

    if len(equipamentos) == 0:
        return

    equipamento_id = ler_inteiro("\nID do equipamento que deseja excluir: ", minimo=1)
    equipamento = buscar_equipamento(equipamento_id)

    if equipamento is None:
        print("Equipamento não encontrado.")
        return

    vinculado = False

    for imovel in imoveis:
        for equipamento_imovel in imovel["equipamentos"]:
            if equipamento_imovel["equipamento_id"] == equipamento_id:
                vinculado = True
                break

        if vinculado:
            break

    if vinculado:
        print("Não é possível excluir: o equipamento está vinculado a um imóvel.")
        return

    print(
        f"Selecionado: {equipamento['nome']} - "
        f"{equipamento['potencia']} W"
    )

    if confirmar("Deseja realmente excluir este equipamento? (S/N): "):
        equipamentos.remove(equipamento)
        print("Equipamento excluído com sucesso!")
    else:
        print("Exclusão cancelada.")


# ============================================================
# US12 — ADICIONAR EQUIPAMENTO AO IMÓVEL
# ============================================================

def adicionar_equipamento_imovel():
    print("\nADICIONAR EQUIPAMENTO AO IMÓVEL")
    linha()

    codigo = input("Código do imóvel: ").strip()
    imovel = buscar_imovel(codigo)

    if imovel is None:
        print("Imóvel não encontrado.")
        return

    if len(equipamentos) == 0:
        print("Não há equipamentos disponíveis.")
        return

    while True:
        visualizar_equipamentos()

        equipamento_id = ler_inteiro(
            "\nDigite o ID do equipamento: ",
            minimo=1
        )

        equipamento = buscar_equipamento(equipamento_id)

        if equipamento is None:
            print("Equipamento inválido!")
        else:
            quantidade = ler_inteiro("Quantidade: ", minimo=1)
            horas = ler_float(
                "Horas de uso por dia: ",
                minimo=0,
                maximo=24
            )

            consumo = calcular_consumo(
                equipamento["potencia"],
                quantidade,
                horas
            )

            equipamento_imovel = {
                "equipamento_id": equipamento["id"],
                "nome": equipamento["nome"],
                "categoria": equipamento["categoria"],
                "potencia": equipamento["potencia"],
                "quantidade": quantidade,
                "horas": horas,
                "consumo": consumo
            }

            imovel["equipamentos"].append(equipamento_imovel)

            print(
                f"{equipamento['nome']} adicionado. "
                f"Consumo estimado: {consumo:.2f} kWh/mês"
            )

        if not confirmar("Deseja adicionar outro equipamento? (S/N): "):
            break

    registrar_historico(imovel)

    print(
        f"Consumo total estimado do imóvel: "
        f"{calcular_consumo_total(imovel):.2f} kWh/mês"
    )


# ============================================================
# US13 — VISUALIZAR HISTÓRICO DE CONSUMO
# ============================================================

def visualizar_historico():
    print("\nHISTÓRICO DE CONSUMO")
    linha()

    codigo = input("Código do imóvel: ").strip()
    imovel = buscar_imovel(codigo)

    if imovel is None:
        print("Imóvel não encontrado.")
        return

    if len(imovel["historico"]) == 0:
        print("Este imóvel ainda não possui registros de consumo.")
        return

    historico_ordenado = sorted(
        imovel["historico"],
        key=lambda registro: datetime.strptime(
            registro["data"],
            "%d/%m/%Y %H:%M:%S"
        )
    )

    for i in range(len(historico_ordenado)):
        registro = historico_ordenado[i]

        print(
            f"{i + 1}. {registro['data']} - "
            f"{registro['consumo']:.2f} kWh/mês"
        )


# ============================================================
# MENUS E HIERARQUIA DE ACESSO
# ============================================================

def menu_usuario():
    while True:
        print("\n" + "=" * 55)
        print("MENU — USUÁRIO/MORADOR")
        print("=" * 55)
        print("1 - Cadastrar imóvel")
        print("2 - Visualizar imóvel")
        print("3 - Editar imóvel")
        print("4 - Visualizar equipamentos")
        print("5 - Adicionar equipamento ao imóvel")
        print("6 - Visualizar histórico de consumo")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_imovel()
        elif opcao == "2":
            visualizar_imovel()
        elif opcao == "3":
            editar_imovel()
        elif opcao == "4":
            visualizar_equipamentos()
        elif opcao == "5":
            adicionar_equipamento_imovel()
        elif opcao == "6":
            visualizar_historico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_gerente():
    while True:
        print("\n" + "=" * 55)
        print("MENU — GERENTE")
        print("=" * 55)
        print("1 - Cadastrar cliente")
        print("2 - Consultar cliente")
        print("3 - Editar cliente")
        print("4 - Excluir cliente")
        print("5 - Cadastrar imóvel")
        print("6 - Visualizar imóvel")
        print("7 - Editar imóvel")
        print("8 - Excluir imóvel")
        print("9 - Visualizar equipamentos")
        print("10 - Adicionar equipamento ao imóvel")
        print("11 - Visualizar histórico de consumo")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            consultar_cliente()
        elif opcao == "3":
            editar_cliente()
        elif opcao == "4":
            excluir_cliente()
        elif opcao == "5":
            cadastrar_imovel()
        elif opcao == "6":
            visualizar_imovel()
        elif opcao == "7":
            editar_imovel()
        elif opcao == "8":
            excluir_imovel()
        elif opcao == "9":
            visualizar_equipamentos()
        elif opcao == "10":
            adicionar_equipamento_imovel()
        elif opcao == "11":
            visualizar_historico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_administrador():
    while True:
        print("\n" + "=" * 55)
        print("MENU — ADMINISTRADOR")
        print("=" * 55)
        print("1 - Cadastrar cliente")
        print("2 - Consultar cliente")
        print("3 - Editar cliente")
        print("4 - Excluir cliente")
        print("5 - Cadastrar imóvel")
        print("6 - Visualizar imóvel")
        print("7 - Editar imóvel")
        print("8 - Excluir imóvel")
        print("9 - Visualizar equipamentos")
        print("10 - Cadastrar equipamento")
        print("11 - Excluir equipamento")
        print("12 - Adicionar equipamento ao imóvel")
        print("13 - Visualizar histórico de consumo")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            consultar_cliente()
        elif opcao == "3":
            editar_cliente()
        elif opcao == "4":
            excluir_cliente()
        elif opcao == "5":
            cadastrar_imovel()
        elif opcao == "6":
            visualizar_imovel()
        elif opcao == "7":
            editar_imovel()
        elif opcao == "8":
            excluir_imovel()
        elif opcao == "9":
            visualizar_equipamentos()
        elif opcao == "10":
            cadastrar_equipamento()
        elif opcao == "11":
            excluir_equipamento()
        elif opcao == "12":
            adicionar_equipamento_imovel()
        elif opcao == "13":
            visualizar_historico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def main():
    while True:
        print("\n" + "=" * 55)
        print("SISTEMA DE DIMENSIONAMENTO ENERGÉTICO")
        print("=" * 55)
        print("Selecione o perfil para testar o sistema:")
        print("1 - Usuário/Morador")
        print("2 - Gerente")
        print("3 - Administrador")
        print("0 - Encerrar")

        perfil = input("Escolha: ").strip()

        if perfil == "1":
            menu_usuario()
        elif perfil == "2":
            menu_gerente()
        elif perfil == "3":
            menu_administrador()
        elif perfil == "0":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
