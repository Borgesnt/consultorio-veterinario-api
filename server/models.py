class Animal:
    def __init__(self, nome, idade, tipo):
        self.nome = nome
        self.idade = idade
        self.tipo = tipo

    def to_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "tipo": self.tipo
        }


class Consulta:
    def __init__(self, animal, data, motivo):
        self.animal = animal
        self.data = data
        self.motivo = motivo

    def to_dict(self):
        return {
            "animal": self.animal,
            "data": self.data,
            "motivo": self.motivo
        }
