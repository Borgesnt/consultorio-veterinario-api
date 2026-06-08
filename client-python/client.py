import requests

URL = "http://localhost:5000"

while True:

    print("\n1 - Cadastrar Animal")
    print("2 - Listar Animais")
    print("3 - Registrar Consulta")
    print("4 - Listar Consultas")
    print("0 - Sair")

    op = input("Escolha: ")

    if op == "1":

        nome = input("Nome: ")
        idade = int(input("Idade: "))
        tipo = input("Tipo: ")

        r = requests.post(
            f"{URL}/animais",
            json={
                "nome": nome,
                "idade": idade,
                "tipo": tipo
            }
        )

        print(r.json())

    elif op == "2":

        r = requests.get(f"{URL}/animais")

        print(r.json())

    elif op == "3":

        animal = input("Animal: ")
        data = input("Data: ")
        motivo = input("Motivo: ")

        r = requests.post(
            f"{URL}/consultas",
            json={
                "animal": animal,
                "data": data,
                "motivo": motivo
            }
        )

        print(r.json())

    elif op == "4":

        r = requests.get(f"{URL}/consultas")

        print(r.json())

    elif op == "0":
        break
