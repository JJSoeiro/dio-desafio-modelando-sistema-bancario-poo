<h1>
    <a href="https://www.dio.me/">
     <img align="center" width="40px" src="https://hermes.dio.me/tracks/648ef080-6c4b-4e54-bf72-34f62030f350.png"></a>
    <span> Bootcamp Python AI Backend Developer - VIVO</span>
</h1>

##   Desafio de Projeto Modelando o Sistema Bancário em POO com Python

### Objetivo Geral

Iniciar a modelagem do sistema bancário em POO (Programação Orientada a Objetos). Adicionar classes para cliente a as operações bancárias: depósito e saque.


### Desafio

Atualizar a implementação do Sistema bancário, para armazenar os dados de clientes e contas bancárias em objetos ao invés de dicionários. O Código deve seguir o modelo de classe UML a seguir:

## Modelo de classe UML

```mermaid
classDiagram
  class Deposito {
    - valor : float
  }

  class Saque {
    - valor : float
  }

  class interface_Transacao {
    + registrar(conta : Conta)
  }

  class Historico {
    + adicinar_transacao(transacao : Transacao)
  }

  class Cliente {
    - endereco : str
    - contas : list
    + realizar_transacao(conta : Conta, transacao : Transacao)
    + adicionar_conta(conta : Conta)
  }

  class Conta {
    - saldo : float
    - numero : int
    - agencia : str
    - cliente : Cliente
    - historico : Historico
    + saldo()  float
    + nova_conta(cliente : Cliente, numero : int)  Conta
    + sacar(valor : float)  bool
    + depositar(valor : float)  bool
  }

  class ContaCorrente {
    - limite : float
    - limites_saques : int
  }

  class PessoaFisica {
    - cpf : str
    - nome : str
    - data_nascimento : date
  }

  Deposito -- > interface_Transacao
  Saque -- > interface_Transacao
  interface_Transacao "*" --* "-transacoes" Historico
  Cliente "realiza" -- "*" interface_Transacao
  Historico "-historico 1" --* Conta
  Conta "" <-- ContaCorrente
  Conta "* -contas" *-- "1 -cliente" Cliente
  Cliente <-- PessoaFisica
```

### Desafio extra

Após concluir a modelagem das classes e a criação dos métodos. Atualizar os métodos que tratam as opções do menu para funcionarem com as classes modeladas.

### Ferramentas

![Python](https://img.shields.io/badge/Python-000?style=for-the-badge&logo=python)
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=30A3DC)](https://docs.github.com/)

### Utilitários

[![Badges](https://img.shields.io/badge/Badges-30A3DC?style=for-the-badge)](https://github.com/digitalinnovationone/dio-lab-open-source/blob/main/utils/badges/badges.md)
