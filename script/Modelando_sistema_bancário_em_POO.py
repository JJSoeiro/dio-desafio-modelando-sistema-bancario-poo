import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento



class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\n=== Operação falhou! Saldo insuficiente para saque. ===')

        elif valor > 0:
            self._saldo -= valor
            print(f'\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===')
            return True

        else:
            print('\n=== Operação falhou! O valor informado é inválido. ===')

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'\n=== Deposito de R$ {valor:.2f} realizado com sucesso! ===')
        else:
            print('\n=== Operação falhou! O valor informado é inválido. ===')
            return False

        return True
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f'\n=== Operação falhou! Ultrapassado o limite de {self.limite_saques} saques diários. ===')

        elif excedeu_saques:
            print('\n=== Operação falhou! Valor solicitado acima do limite de saque de R$ 500,00. ===')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f'''\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        '''

    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)        


def entrar_no_sistema():
    menu = '''

      Bem Vindo, selecione à opção desajada.
    ==========================================
    [1]\tJá sou cliente. Entrar no sistema.
    [2]\tNão sou cliente. Abrir conta.
    [0]\tSair

    => '''
    return input(textwrap.dedent(menu))


def consultar_contas():
    menu = """

                     MENU
    ======================================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tAbrir nova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def cadastrar_clientes():
    menu = """

                     MENU
    ======================================
    [cc]\tCadastrar cliente
    [ac]\tAbrir conta
    [lc]\tListar conta
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\n=== Cliente não possui conta! ===')
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n=== Cliente não encontrado! ===')
        return

    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n=== Cliente não encontrado! ===')
        return

    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n=== Cliente não encontrado! ===')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n            Extrato Bancário')
    print('=' * 40)
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\t\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f'\nSaldo:\t\tR$ {conta.saldo:.2f}')
    print('=' * 40)


def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n=== Cliente não encontrado, fluxo de criação de conta encerrado! ===')
        return

    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n=== Conta criada com sucesso! ===')


def listar_contas(contas):
    for conta in contas:
        print('=' * 100)
        print(textwrap.dedent(str(conta)))


def selecionar_funcoes_conta(clientes, contas):
    while True:
        consulta_conta = consultar_contas()

        if consulta_conta == 'd':
            depositar(clientes)

        elif consulta_conta == 's':
            sacar(clientes)

        elif consulta_conta == 'e':
            exibir_extrato(contas)

        elif consulta_conta == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif consulta_conta == 'lc':
            listar_contas(contas)

        elif consulta_conta == 'q':
            print('\n=== Obrigado por utilizar os nossos serviços! ===')
            break

        else:
            print('\n=== Opção selecionada incorreta, selecione a opção correta. ===')


def cadastrar_novo_cliente(clientes):
    cpf = input('Informe o CPF (somente número): ')
    cliente_filtrado = filtrar_cliente(cpf, clientes)

    if cliente_filtrado:
        print('\n=== Já existe cliente com esse CPF! ===')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n=== Cliente criado com sucesso! ===')


def selecionar_funcoes_cadastro(clientes, contas):
    while True:
        cadastro_cliente = cadastrar_clientes()

        if cadastro_cliente == 'cc':
            cadastrar_novo_cliente(clientes)

        elif cadastro_cliente == 'ac':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif cadastro_cliente == 'lc':
            listar_contas(contas)
                
        elif cadastro_cliente == 'q':
            print('\n=== Obrigado por utilizar os nossos serviços! ===')
            break

        else:
            print('\n=== Opção selecionada incorreta, selecione a opção correta. ===')



def main():
    clientes = []
    contas = []


    while True:

        entra_sistema = entrar_no_sistema()

        if entra_sistema == '1':
            selecionar_funcoes_conta(clientes, contas) 

        elif entra_sistema == '2':
            selecionar_funcoes_cadastro(clientes, contas)

        elif entra_sistema == '0':
            print('\n=== Aguardamos o seu retorno! ===')
            break

        else:
            print('\n=== Opção selecionada incorreta, selecione a opção correta. ===')

main()
