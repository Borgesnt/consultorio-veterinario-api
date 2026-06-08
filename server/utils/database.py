import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

ARQUIVO = os.path.join(
    BASE_DIR,
    "data.json"
)


def carregar():

    if not os.path.exists(ARQUIVO):

        dados = {
            "animais": [],
            "consultas": [],
            "mensagens_processadas": 0,
            "eventos": []
        }

        salvar(dados)

        return dados

    with open(ARQUIVO, "r") as f:

        return json.load(f)


def salvar(dados):

    with open(ARQUIVO, "w") as f:

        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )