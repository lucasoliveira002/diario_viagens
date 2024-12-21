class Viagem:
    #classe para viagem
    def __init__(self, destino, data, descricao, nota):
        self.destino = destino
        self.data = data
        self.descricao = descricao
        self.nota = nota

    #retorna um dicionário com os dados da viagem
    def to_dict(self):
        return {
            'destino': self.destino,
            'data': self.data,
            'descricao': self.descricao,
            'nota': self.nota
        }

    #retorna uma instância de viagem a partir de um dicionário
    @classmethod
    def from_dict(cls, data):
        return cls(
            destino=data['destino'],
            data=data['data'],
            descricao=data['descricao'],
            nota=data['nota']
        )