from typing import Self
import crcmod
import qrcode

class Payload():
    def __init__(self, nome, chavepix, valor, cidade, txtId):

        self.nome = nome
        self.chavepix = chavepix
        self.valor = valor
        self.cidade = cidade
        self.txtId = txtId

        self.payloadFormat = '000201'
        self.merchanAccount = '26'
        self.merchanCategCode = '52040000'