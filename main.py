imoveis = []

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
        'equipamentos':[]
    }

    imoveis.append(imovel)

    print("-" * 20)
    print("IMÓVEL CADASTRADO!")
    print("-" * 20)

    continuar = input("Deseja cadastrar outro imóvel? (S/N): ").upper()

    if continuar != "S":
        break


print("\n" + "=" * 30)
print("IMÓVEIS CADASTRADOS")
print("=" * 30)

for imovel in imoveis:
    print(f"Código do imóvel: {imovel['codigo']}")
    print(f"Nome do proprietário: {imovel['nome']}")
    print(f"CEP do proprietário: {imovel['cep']}")
    print("-" * 30)

while True:
    add=input('Deseja adcionar equipamentos? ').upper()
    if add=='N':
        break
    codigo=input('Digite o codigo do imovel cadastrado: ')
    for i in imoveis:
        if i['codigo']==codigo:
            equipamento=input('qual equipamento quer adicionar? ')
            categoria=input('categoria do produto: ')
            potencia=float(input('potência do equipamento: '))
            quant=int(input('quantidade desse equipamento: '))
            dicionario={
                'nome':equipamento,
                'categoria':categoria,
                'potencia':potencia,
                'quantidade':quant,
                'tempo':0
            }
            i['equipamentos'].append(dicionario)
            break
    else:
        print('nao existe nenhuma residencia com esse codigo')
        continue
while True:
    for imovel in imoveis:
        codigo=input('digite o codigo do imovel: ')
        if imovel['codigo']==codigo:
            for equipamento in imovel['equipamentos']:
                print(f"\nEquipamento: {equipamento['nome']}")
                tempo=float(input('Digite o tempo de uso desse equipamento: '))
                if tempo<0:
                    while True:
                        if tempo>0:
                            break
                        tempo=float(input('digite o tempo: '))
                equipamento['tempo']+=tempo
        break
    else:
        print('nenhuma residencia com esse codigo')
    continuar = input("Deseja cadastrar tempo em outro imóvel? (S/N): ").upper()
    if continuar != "S":
        break
        