imoveis = []

equipamentos = [
    {"nome": "Televisão", "categoria": "Eletrônico", "potencia": 100},
    {"nome": "Geladeira", "categoria": "Eletrodoméstico", "potencia": 200},
    {"nome": "Ventilador", "categoria": "Climatização", "potencia": 80},
    {"nome": "Micro-ondas", "categoria": "Eletrodoméstico", "potencia": 1200},
    {"nome": "Chuveiro", "categoria": "Aquecimento", "potencia": 5500}
]

while True:
    codigo_imovel = input("Informe o código do imóvel para cadastro: ")

    while len(codigo_imovel) != 6 or not codigo_imovel.isdigit():
        print("CÓDIGO INVÁLIDO! Digite um código de imóvel com exatamente 6 dígitos.")
        codigo_imovel = input("Informe o código do imóvel para cadastro: ")

    nome = input("Digite seu nome completo para cadastro: ")

    endereco = input("Digite seu CEP para cadastro de endereço: ")

    while len(endereco) != 8 or not endereco.isdigit():
        print("CEP INVÁLIDO! O CEP tem que ter exatamente 8 caracteres.")
        endereco = input("Digite seu CEP para cadastro de endereço: ")

    imovel = {
        "codigo": codigo_imovel,
        "nome": nome,
        "cep": endereco,
        "equipamentos": []
    }

    print("\nEQUIPAMENTOS DISPONÍVEIS")
    print("-" * 30)

    for i in range(len(equipamentos)):
        print(
            i + 1,
            "-",
            equipamentos[i]["nome"],
            "-",
            equipamentos[i]["potencia"],
            "W"
        )

    while True:
        escolha = int(input("\nDigite o número do equipamento: "))

        if escolha < 1 or escolha > len(equipamentos):
            print("Equipamento inválido!")
            continue

        equipamento = equipamentos[escolha - 1]

        quantidade = int(input("Quantidade: "))
        horas = float(input("Horas de uso por dia: "))

        consumo = (
            equipamento["potencia"]
            * quantidade
            * horas
            * 30
        ) / 1000

        equipamento_imovel = {
            "nome": equipamento["nome"],
            "categoria": equipamento["categoria"],
            "potencia": equipamento["potencia"],
            "quantidade": quantidade,
            "horas": horas,
            "consumo": consumo
        }

        imovel["equipamentos"].append(equipamento_imovel)

        continuar_equipamento = input(
            "Deseja adicionar outro equipamento? (S/N): "
        ).upper()

        if continuar_equipamento != "S":
            break

    imoveis.append(imovel)

    print("-" * 30)
    print("IMÓVEL CADASTRADO!")
    print("-" * 30)

    continuar = input("Deseja cadastrar outro imóvel? (S/N): ").upper()

    if continuar != "S":
        break

print("\n" + "=" * 40)
print("IMÓVEIS CADASTRADOS")
print("=" * 40)

for imovel in imoveis:
    print(f"\nCódigo do imóvel: {imovel['codigo']}")
    print(f"Nome do proprietário: {imovel['nome']}")
    print(f"CEP do proprietário: {imovel['cep']}")

    print("\nEQUIPAMENTOS")

    consumo_total = 0

    for equipamento in imovel["equipamentos"]:
        print("-" * 30)
        print("Nome:", equipamento["nome"])
        print("Categoria:", equipamento["categoria"])
        print("Potência:", equipamento["potencia"], "W")
        print("Quantidade:", equipamento["quantidade"])
        print("Uso diário:", equipamento["horas"], "horas")
        print(f"Consumo mensal: {equipamento['consumo']:.2f} kWh/mês")

        consumo_total += equipamento["consumo"]

    print("-" * 30)
    print(f"CONSUMO TOTAL DO IMÓVEL: {consumo_total:.2f} kWh/mês")
    print("=" * 40)
