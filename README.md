<div align="center">

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                  PYBANK                                      ║
║                 Sistema Bancário Completo v5.0                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)]()
[![Terminal](https://img.shields.io/badge/Terminal-ANSI%20Colors-4D4D4D?style=for-the-badge&logo=windows-terminal&logoColor=white)]()

**Sistema bancário em Python com interface visual rica, persistência em JSON e arquitetura orientada a objetos.**

[🚀 Instalação](#-instalação) • [💻 Uso](#-uso) • [✨ Funcionalidades](#-funcionalidades) • [📸 Screenshots](#-screenshots) • [🏗️ Arquitetura](#️-arquitetura)

</div>

---

## 📋 Sumário

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Arquitetura](#️-arquitetura)
- [Estrutura de Dados](#-estrutura-de-dados)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 📖 Sobre o Projeto

O **PyBank** é um sistema bancário completo desenvolvido em Python puro, projetado para simular operações bancárias reais com uma interface de terminal rica e intuitiva. O sistema utiliza cores ANSI, gradientes RGB, emojis e elementos visuais Unicode para criar uma experiência de usuário agradável diretamente no console.

### 🎯 Objetivos

- Simular um ambiente bancário real com operações CRUD
- Demonstrar padrões de projeto orientados a objetos em Python
- Criar uma interface visual atraente sem dependências externas
- Persistir dados de forma segura utilizando JSON

---

## ✨ Funcionalidades

### 💼 Gestão de Clientes
- [x] Cadastro de clientes pessoa física (PF)
- [x] Validação de CPF (formato e dígitos)
- [x] Cadastro completo de endereço
- [x] Listagem de todos os clientes cadastrados
- [x] Associação automática de contas aos clientes

### 🏦 Gestão de Contas
- [x] Criação de contas correntes vinculadas a clientes
- [x] Número de conta sequencial automático
- [x] Agência padrão `0001`
- [x] Limite de saque configurável (padrão: R$ 500,00)
- [x] Limite de saques diários (padrão: 3)

### 💰 Operações Financeiras
- [x] **Depósitos** com registro no histórico
- [x] **Saques** com verificação de saldo e limites
- [x] **Transferências** entre contas do sistema
- [x] **Extrato** detalhado com todas as movimentações
- [x] Formatação monetária no padrão brasileiro (R$)

### 📊 Dashboard & Relatórios
- [x] Dashboard com estatísticas em tempo real
- [x] Visualização de saldo total e médio
- [x] Gráfico de barras com top 5 contas
- [x] Lista de últimas transações
- [x] Contadores de clientes e contas ativas

### 💾 Persistência
- [x] Salvamento automático em JSON
- [x] Recuperação de dados ao iniciar
- [x] Armazenamento em diretório `data/`
- [x] Estrutura separada para clientes e contas

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.8+ | Linguagem principal |
| ANSI Colors | - | Cores e estilos no terminal |
| RGB Gradient | - | Gradientes de cor personalizados |
| Unicode | - | Caracteres especiais e emojis |
| JSON | - | Persistência de dados |
| OOP | - | Programação orientada a objetos |

### 📦 Bibliotecas Padrão Utilizadas

```python
import json      # Persistência de dados
import os        # Operações de sistema
import re        # Expressões regulares
import textwrap  # Formatação de texto
from abc import ABC, abstractmethod  # Classes abstratas
from dataclasses import dataclass    # Classes de dados
from datetime import datetime        # Manipulação de datas
from pathlib import Path             # Caminhos de arquivo
from typing import List, Optional, Dict  # Type hints
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior instalado
- Terminal com suporte a cores ANSI (recomendado)

### Passo a Passo

1. **Clone o repositório** (ou baixe o arquivo):
```bash
git clone https://github.com/seu-usuario/pybank.git
cd pybank
```

2. **Verifique a instalação do Python**:
```bash
python3 --version
```

3. **Execute o sistema**:
```bash
python3 PyBank.py
```

> ⚠️ **Nota**: Não requer instalação de dependências externas. O sistema utiliza apenas bibliotecas padrão do Python.

---

## 💻 Uso

### Menu Principal

Ao executar, o sistema apresenta um menu interativo:

```
[d] 💰 Depositar        [s] 💸 Sacar
[e] 📄 Extrato          [t] 🔄 Transferir
[c] ➕ Nova Conta       [l] 📋 Listar Contas
[u] 👤 Novo Cliente     [v] 👥 Listar Clientes
[dash] 📊 Dashboard     [q] 🚪 Sair
```

### Fluxo Típico

1. **Cadastrar Cliente** → `u`
   - Informe CPF, nome, data de nascimento e endereço
   - O sistema valida automaticamente

2. **Criar Conta** → `c`
   - Informe o CPF do cliente
   - Conta criada automaticamente com agência 0001

3. **Realizar Depósito** → `d`
   - Selecione a conta
   - Informe o valor

4. **Consultar Extrato** → `e`
   - Visualize todo o histórico de movimentações

### Comandos do Dashboard

- Digite `dash` no menu principal para visualizar estatísticas
- Veja saldo total, médio e gráficos em tempo real

---

## 🏗️ Arquitetura

O PyBank segue os princípios da Programação Orientada a Objetos com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────────┐
│                         PYBANK                              │
├─────────────────────────────────────────────────────────────┤
│  Interface (UI)                                             │
│  ├── Cores         → Paleta ANSI e gradientes RGB          │
│  ├── MenuUI        → Telas e interações                    │
│  └── Dashboard     → Visualização de estatísticas          │
├─────────────────────────────────────────────────────────────┤
│  Serviço (Service)                                          │
│  └── BancoService  → Lógica de negócio e orquestração      │
├─────────────────────────────────────────────────────────────┤
│  Persistência (Repository)                                  │
│  └── BancoDados    → JSON read/write                       │
├─────────────────────────────────────────────────────────────┤
│  Domínio (Domain)                                           │
│  ├── Cliente       → PessoaFisica                          │
│  ├── Conta         → ContaCorrente                         │
│  ├── Endereco      → Value Object                          │
│  ├── Historico     → Registro de transações                │
│  └── Transacao     → Saque, Deposito, Transferencia        │
└─────────────────────────────────────────────────────────────┘
```

### Padrões de Projeto Utilizados

| Padrão | Implementação |
|--------|---------------|
| **Repository** | `BancoDados` - abstração da persistência |
| **Service Layer** | `BancoService` - lógica de negócio |
| **Abstract Base Class** | `Transacao` - contrato para operações |
| **Dataclass** | `Endereco`, `RegistroTransacao` - objetos de valor |
| **Property** | Encapsulamento de atributos nas classes |

---

## 📁 Estrutura de Dados

### Arquivos JSON

O sistema mantém dois arquivos no diretório `data/`:

#### `clientes.json`
```json
{
  "12345678901": {
    "tipo": "pf",
    "nome": "João Silva",
    "data_nascimento": "15-05-1990",
    "cpf": "12345678901",
    "endereco": {
      "logradouro": "Rua das Flores",
      "numero": "123",
      "bairro": "Centro",
      "cidade": "São Paulo",
      "uf": "SP",
      "cep": "01001000"
    }
  }
}
```

#### `contas.json`
```json
[
  {
    "tipo": "corrente",
    "numero": 1,
    "agencia": "0001",
    "cpf_cliente": "12345678901",
    "saldo": 1500.00,
    "historico": [
      {
        "tipo": "Deposito",
        "valor": 1500.00,
        "data": "10/02/2026 14:30:00"
      }
    ],
    "ativa": true,
    "limite": 500.00,
    "limite_saques": 3
  }
]
```

---

## 📸 Screenshots

### Splash Screen
```
╔══════════════════════════════════════════════════════════════════╗
║                    🏦 PYBANK v5.0                                ║
║         Bem-vindo ao Sistema Bancário                            ║
╚══════════════════════════════════════════════════════════════════╝
```

### Dashboard
```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ 👥 CLIENTES          │  │ 💰 PATRIMÔNIO        │  │ 📈 MOVIMENTAÇÕES     │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤
│   5 cadastrados      │  │ Total: R$ 15.000,00  │  │   12 transações      │
│   5 contas           │  │ Média: R$ 3.000,00   │  │   5 contas ativas    │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

### Extrato
```
┌────────────────────────────────────────────────────────────────────┐
│                       EXTRATO BANCÁRIO                             │
├────────────────────────────────────────────────────────────────────┤
│ Cliente: João Silva                                                │
│ Conta: 1 | Agência: 0001                                           │
├────────────────────────────────────────────────────────────────────┤
│ DATA/HORA          │ TIPO        │ VALOR              │
├────────────────────────────────────────────────────────────────────┤
│ 10/02/2026 14:30   │ 💰 DEPOSITO │        R$ 1.500,00 │
│ 10/02/2026 15:45   │ 💸 SAQUE    │          R$ 300,00 │
├────────────────────────────────────────────────────────────────────┤
│ SALDO ATUAL:                                    R$ 1.200,00        │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ Roadmap

### Implementado ✅
- [x] Cadastro de clientes PF
- [x] Gestão de contas correntes
- [x] Depósito, saque e transferência
- [x] Extrato detalhado
- [x] Dashboard com estatísticas
- [x] Persistência em JSON
- [x] Interface colorida com ANSI

### Futuras Implementações 🔮
- [ ] Cadastro de Pessoa Jurídica (PJ)
- [ ] Geração de relatórios em PDF
- [ ] Criptografia de dados sensíveis
- [ ] Múltiplas agências
- [ ] Empréstimos e financiamentos
- [ ] Investimentos (CDB, Tesouro)
- [ ] Interface web com Flask

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**XAKCN** - [@seu-usuario](https://github.com/XAKCN)

---

<div align="center">

Made with ❤️ and Python

⭐ Star este repo se você achou útil!

</div>
