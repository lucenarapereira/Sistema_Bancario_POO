import textwrap
from datetime import datetime

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self.transacoes.append({"tipo": tipo, "valor": valor})

    def exibir_historico(self):
        if not self.transacoes:
            return "Não foram realizadas transações."
        historico_str = "\n".join([f"{trans['tipo']}:\tR$ {trans['valor']:.2f}" for trans in self.transacoes])
        return historico_str

class Cliente:
    def __init__(self, nome, data_nascimento, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, endereco)
        self.cpf = cpf

class Conta(Historico):
    def __init__(self, agencia, numero_conta, cliente):
        super().__init__()
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.numero_saques = 0
        self.limite_saques = 3  

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.adicionar_transacao("Depósito", valor)
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.adicionar_transacao("Saque", valor)
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print(self.exibir_historico())
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

class ContaCorrente(Conta):
    def __init__(self, agencia, numero_conta, cliente, limite_cheque_especial=0.0, limite=500.0):
        super().__init__(agencia, numero_conta, cliente)
        self.limite_cheque_especial = limite_cheque_especial
        self.limite = limite 

    def sacar(self, valor):
     
        if valor > self.saldo + self.limite_cheque_especial:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente, nem no cheque especial. @@@")
            return
        if self.numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return
        super().sacar(valor)

class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []
        self.agencia = "0001"

    def criar_cliente(self):
        nome = input("Informe o nome completo: ")
        data_nascimento_str = input("Informe a data de nascimento (dd-mm-aaaa): ")
        data_nascimento = datetime.strptime(data_nascimento_str, "%d-%m-%Y").date()
        cpf = input("Informe o CPF (somente números): ")

        if any(c.cpf == cpf for c in self.clientes):
            print("\n@@@ Já existe cliente com esse CPF! @@@")
            return

        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
        self.clientes.append(cliente)
        print("=== Cliente criado com sucesso! ===")

    def criar_conta(self):
        cpf = input("Informe o CPF do cliente: ")
        cliente = next((c for c in self.clientes if c.cpf == cpf), None)

        if cliente:
            numero_conta = len(self.contas) + 1
            tipo_conta = input("Informe o tipo de conta (corrente ou simples): ").strip().lower()
            if tipo_conta == "corrente":
                limite_cheque_especial = float(input("Informe o limite do cheque especial: "))
                limite = float(input("Informe o limite da conta: "))
                conta = ContaCorrente(self.agencia, numero_conta, cliente, limite_cheque_especial, limite)
            else:
                conta = Conta(self.agencia, numero_conta, cliente)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")

    def listar_contas(self):
        for conta in self.contas:
            print("=" * 100)
            print(f"Agência:\t{conta.agencia}")
            print(f"C/C:\t\t{conta.numero_conta}")
            print(f"Titular:\t{conta.cliente.nome}")
            print(f"CPF:\t{conta.cliente.cpf}")
            print("=" * 100)

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo cliente
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            conta_numero = int(input("Informe o número da conta: ")) - 1
            valor = float(input("Informe o valor do depósito: "))
            banco.contas[conta_numero].depositar(valor)

        elif opcao == "s":
            conta_numero = int(input("Informe o número da conta: ")) - 1
            valor = float(input("Informe o valor do saque: "))
            banco.contas[conta_numero].sacar(valor)

        elif opcao == "e":
            conta_numero = int(input("Informe o número da conta: ")) - 1
            banco.contas[conta_numero].exibir_extrato()

        elif opcao == "nu":
            banco.criar_cliente()

        elif opcao == "nc":
            banco.criar_conta()

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
