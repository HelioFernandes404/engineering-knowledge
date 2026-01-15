# Conceito base do OOP
# Classes e Objetos


## Exemple Class e Objetos
class Carro:
    def __init__(self, cor, modelo):
        self.modelo = modelo
        self.cor = cor

    def ligar(self):
        print("Carro ligado")


meu_carro = Carro("azul", "Fusca")

meu_carro.ligar()  # Carro ligado


# Encapsulamento
class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.__saldo = saldo_inicial  # Atributo privado (encapsulado)

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor

    def sacar(self, valor):
        if 0 < valor <= self.__saldo:
            self.__saldo -= valor

    def mostrar_saldo(self):
        print(f"Saldo: {self.__saldo}")


conta = ContaBancaria(1000)
conta.depositar(500)
conta.sacar(200)
conta.mostrar_saldo()  # Saldo: 1300


# Herança
class Veiculo:
    def __init__(self, cor, modelo):
        self.cor = cor
        self.modelo = modelo

    def ligar(self):
        print("Veículo ligado")


class Moto(Veiculo):
    def __init__(self, cor, modelo, estilo):
        super().__init__(cor, modelo)
        self.estilo = estilo

    def acelear(self):
        print("Moto acelerando")


moto = Moto("preta", "Biz", "Urbana")
moto.ligar()  # Veículo ligado
moto.acelear()  # Moto acelerando


# Polimorfismo
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def emitir_som(self):
        pass


class Cachorro(Animal):
    def emitir_som(self):
        print("Au au")


class Gato(Animal):
    def emitir_som(self):
        print("Miau")


cachorro = Cachorro("Rex")
gato = Gato("Felix")

cachorro.emitir_som()  # Au au
gato.emitir_som()  # Miau
