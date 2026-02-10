#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                  PYBANK                                      ║
║                 Sistema Bancário Completo v.5_final                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import os
import re
import textwrap
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict


# ═══════════════════════════════════════════════════════════════════════════════
# CORES E ESTILOS ANSI
# ═══════════════════════════════════════════════════════════════════════════════

class Cores:
    """Paleta de cores ANSI para terminal."""
    # Cores básicas
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKE = "\033[9m"
    
    # Cores de texto
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Cores claras
    LIGHT_BLACK = "\033[90m"
    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_MAGENTA = "\033[95m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_WHITE = "\033[97m"
    
    # Cores de fundo
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Gradientes e estilos especiais
    @staticmethod
    def gradient(text: str, start_color: tuple, end_color: tuple) -> str:
        """Aplica gradiente de cor no texto."""
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue
            ratio = i / max(length - 1, 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            result += f"\033[38;2;{r};{g};{b}m{char}"
        return result + Cores.RESET
    
    @staticmethod
    def rgb(r: int, g: int, b: int, text: str) -> str:
        """Aplica cor RGB específica."""
        return f"\033[38;2;{r};{g};{b}m{text}{Cores.RESET}"
    
    @staticmethod
    def bg_rgb(r: int, g: int, b: int, text: str) -> str:
        """Aplica cor de fundo RGB."""
        return f"\033[48;2;{r};{g};{b}m{text}{Cores.RESET}"


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

UI_LARGURA = 70
PROJETO_NOME = "PyBank"
PROJETO_VERSAO = "v.5_final"
DATA_DIR = Path(__file__).parent / "data"
CLIENTES_FILE = DATA_DIR / "clientes.json"
CONTAS_FILE = DATA_DIR / "contas.json"

# Cores tema
C_PRIMARIA = Cores.CYAN
C_SECUNDARIA = Cores.MAGENTA
C_SUCESSO = Cores.GREEN
C_ERRO = Cores.RED
C_AVISO = Cores.YELLOW
C_INFO = Cores.BLUE
C_DESTAQUE = Cores.LIGHT_CYAN
C_TEXTO = Cores.WHITE
C_SUBTITULO = Cores.LIGHT_BLACK

ANSI_ESCAPE_RE = re.compile(r"\033\[[0-9;]*m")
VARIATION_SELECTOR = "\ufe0f"


# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE INTERFACE VISUAL
# ═══════════════════════════════════════════════════════════════════════════════

def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def normalizar_unicode(texto: str) -> str:
    """Remove caracteres problemáticos para cálculo de largura visual."""
    return str(texto).replace(VARIATION_SELECTOR, "")


def limpar_ansi(texto: str) -> str:
    """Remove sequências ANSI de formatação."""
    return ANSI_ESCAPE_RE.sub("", normalizar_unicode(texto))


def largura_visual(texto: str) -> int:
    """Calcula largura visual real (Unicode + ANSI)."""
    largura = 0
    for char in limpar_ansi(texto):
        if unicodedata.combining(char):
            continue
        largura += 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
    return largura


def truncar_visual(texto: str, limite: int) -> str:
    """Trunca texto considerando largura visual e sequências ANSI."""
    if limite <= 0:
        return ""

    texto = normalizar_unicode(texto)
    resultado = []
    largura = 0
    i = 0
    possui_ansi = False
    truncado = False

    while i < len(texto):
        if texto[i] == "\033":
            match = ANSI_ESCAPE_RE.match(texto, i)
            if match:
                resultado.append(match.group(0))
                i = match.end()
                possui_ansi = True
                continue

        char = texto[i]
        if unicodedata.combining(char):
            i += 1
            continue

        largura_char = 2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
        if largura + largura_char > limite:
            truncado = True
            break

        resultado.append(char)
        largura += largura_char
        i += 1

    texto_final = "".join(resultado)
    if truncado and possui_ansi and not texto_final.endswith(Cores.RESET):
        texto_final += Cores.RESET
    return texto_final


def ajustar_visual(texto: str, largura: int, alinhamento: str = "esquerda") -> str:
    """Ajusta texto para largura fixa usando largura visual real."""
    texto_ajustado = truncar_visual(texto, largura)
    faltante = max(0, largura - largura_visual(texto_ajustado))

    if alinhamento == "direita":
        return " " * faltante + texto_ajustado
    if alinhamento == "centro":
        esquerda = faltante // 2
        direita = faltante - esquerda
        return " " * esquerda + texto_ajustado + " " * direita
    return texto_ajustado + " " * faltante


def formatar_moeda(valor: float) -> str:
    """Formata valores monetários brasileiros com cor."""
    valor_formatado = f"{abs(valor):,.2f}"
    valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    cor = C_SUCESSO if valor >= 0 else C_ERRO
    return f"{cor}R$ {valor_formatado}{Cores.RESET}"


def limitar_texto(texto: str, limite: int) -> str:
    """Limita texto com reticências."""
    if largura_visual(texto) <= limite:
        return normalizar_unicode(str(texto))
    if limite <= 3:
        return truncar_visual(texto, limite)
    return truncar_visual(texto, limite - 3) + f"{Cores.DIM}...{Cores.RESET}"


def centralizar(texto: str, largura: int = UI_LARGURA) -> str:
    """Centraliza texto considerando códigos ANSI."""
    return ajustar_visual(texto, largura, "centro")


def criar_linha(cor: str = C_PRIMARIA, char: str = "═", largura: int = UI_LARGURA) -> str:
    """Cria uma linha decorativa."""
    return f"{cor}{char * largura}{Cores.RESET}"


def criar_caixa(titulo: str, *linhas: str, cor_titulo: str = C_PRIMARIA, 
                cor_borda: str = C_PRIMARIA, icone: str = "🏦") -> str:
    """Cria uma caixa decorativa."""
    interna = UI_LARGURA - 2
    titulo_linha = f" {cor_titulo}{Cores.BOLD}{normalizar_unicode(icone)} {titulo.upper()}{Cores.RESET} "

    resultado = [
        f"{cor_borda}╔{'═' * interna}╗{Cores.RESET}",
        f"{cor_borda}║{Cores.RESET}{ajustar_visual(titulo_linha, interna, 'centro')}{cor_borda}║{Cores.RESET}",
        f"{cor_borda}╠{'═' * interna}╣{Cores.RESET}",
    ]
    
    for linha in linhas:
        if linha:
            conteudo = ajustar_visual(f" {normalizar_unicode(linha)} ", interna)
            resultado.append(f"{cor_borda}║{Cores.RESET}{conteudo}{cor_borda}║{Cores.RESET}")
    
    resultado.append(f"{cor_borda}╚{'═' * interna}╝{Cores.RESET}")
    return "\n".join(resultado)


def criar_painel(titulo: str, conteudo: List[str], icone: str = "📊", 
                 cor: str = C_PRIMARIA) -> str:
    """Cria um painel informativo."""
    largura = 32  # largura interna
    titulo_linha = f" {Cores.BOLD}{normalizar_unicode(icone)} {titulo}{Cores.RESET} "

    linhas = [
        f"{cor}┌{'─' * largura}┐{Cores.RESET}",
        f"{cor}│{Cores.RESET}{ajustar_visual(titulo_linha, largura)}{cor}│{Cores.RESET}",
        f"{cor}├{'─' * largura}┤{Cores.RESET}",
    ]
    
    for item in conteudo:
        conteudo_linha = ajustar_visual(f" {normalizar_unicode(item)}", largura)
        linhas.append(f"{cor}│{Cores.RESET}{conteudo_linha}{cor}│{Cores.RESET}")
    
    linhas.append(f"{cor}└{'─' * largura}┘{Cores.RESET}")
    return "\n".join(linhas)


def barra_progresso(valor: float, maximo: float, largura: int = 20, 
                    cor_preenchida: str = C_SUCESSO, cor_vazia: str = Cores.DIM) -> str:
    """Cria uma barra de progresso visual."""
    if maximo <= 0:
        preenchido = 0
    else:
        preenchido = int((valor / maximo) * largura)
    preenchido = max(0, min(largura, preenchido))
    
    barra = "█" * preenchido + "░" * (largura - preenchido)
    return f"{cor_preenchida}{barra[:largura]}{Cores.RESET}"


def animacao_carregamento(texto: str = "Carregando", duracao: float = 0.5):
    """Mostra animação de carregamento."""
    import time
    simbolos = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    inicio = time.time()
    i = 0
    while time.time() - inicio < duracao:
        print(f"\r{C_PRIMARIA}{simbolos[i % len(simbolos)]}{Cores.RESET} {texto}...", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{' ' * (len(texto) + 10)}\r", end="")


def titulo_gradiente(texto: str) -> str:
    """Cria título com gradiente dourado."""
    return Cores.gradient(texto, (255, 215, 0), (255, 140, 0))


# ═══════════════════════════════════════════════════════════════════════════════
# MENSAGENS ESTILIZADAS
# ═══════════════════════════════════════════════════════════════════════════════

def msg_sucesso(mensagem: str, icone: str = "✅"):
    """Exibe mensagem de sucesso."""
    print(f"{C_SUCESSO}{normalizar_unicode(icone)} {mensagem}{Cores.RESET}")


def msg_erro(mensagem: str, icone: str = "❌"):
    """Exibe mensagem de erro."""
    print(f"{C_ERRO}{normalizar_unicode(icone)} {mensagem}{Cores.RESET}")


def msg_aviso(mensagem: str, icone: str = "⚠"):
    """Exibe mensagem de aviso."""
    print(f"{C_AVISO}{normalizar_unicode(icone)} {mensagem}{Cores.RESET}")


def msg_info(mensagem: str, icone: str = "ℹ"):
    """Exibe mensagem informativa."""
    print(f"{C_INFO}{normalizar_unicode(icone)} {mensagem}{Cores.RESET}")


def msg_destaque(mensagem: str, icone: str = "👉"):
    """Exibe mensagem em destaque."""
    print(f"{C_DESTAQUE}{Cores.BOLD}{normalizar_unicode(icone)} {mensagem}{Cores.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRADA DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

def input_colorido(mensagem: str, cor: str = C_PRIMARIA, icone: str = "→") -> str:
    """Input com cor."""
    return input(f"{cor}{icone}{Cores.RESET} {mensagem} ").strip()


def input_valor(mensagem: str) -> Optional[float]:
    """Input monetário com validação."""
    entrada = input_colorido(mensagem, C_SUCESSO, "💵")
    entrada = entrada.replace(",", ".")
    try:
        valor = float(entrada)
        if valor <= 0:
            msg_erro("O valor deve ser maior que zero!")
            return None
        return valor
    except ValueError:
        msg_erro("Valor inválido! Use apenas números.")
        return None


def input_cpf() -> str:
    """Input de CPF com validação visual."""
    cpf = input_colorido("CPF (somente números):", C_INFO, "📝")
    return re.sub(r'[^0-9]', '', cpf)


def confirmar(mensagem: str) -> bool:
    """Confirmação com estilo."""
    resposta = input(f"{C_AVISO}❓ {mensagem} (s/n):{Cores.RESET} ").strip().lower()
    return resposta in ('s', 'sim', 'yes', 'y')


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

def validar_cpf(cpf: str) -> bool:
    """Valida CPF (11 dígitos)."""
    cpf = re.sub(r'[^0-9]', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()


def formatar_cpf(cpf: str) -> str:
    """Formata CPF XXX.XXX.XXX-XX."""
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11:
        return cpf
    return f"{C_PRIMARIA}{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}{Cores.RESET}"


def validar_data(data: str) -> bool:
    """Valida data dd-mm-aaaa."""
    try:
        datetime.strptime(data, "%d-%m-%Y")
        return True
    except ValueError:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# ENTIDADES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Endereco:
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    uf: str
    cep: str = ""
    
    def __str__(self) -> str:
        end = f"{self.logradouro}, {self.numero} - {self.bairro}"
        end += f"\n{' ' * 15} {self.cidade}/{self.uf}"
        if self.cep:
            end += f" - CEP: {self.cep}"
        return end
    
    def to_dict(self) -> dict:
        return {
            "logradouro": self.logradouro,
            "numero": self.numero,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "cep": self.cep
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Endereco":
        return cls(**data)


class Cliente:
    def __init__(self, endereco: Endereco):
        self._endereco = endereco
        self._contas: List["Conta"] = []
    
    @property
    def endereco(self) -> Endereco:
        return self._endereco
    
    @property
    def contas(self) -> List["Conta"]:
        return self._contas
    
    def adicionar_conta(self, conta: "Conta"):
        self._contas.append(conta)
    
    def realizar_transacao(self, conta: "Conta", transacao: "Transacao") -> bool:
        if conta not in self._contas:
            msg_erro("Esta conta não pertence a este cliente!")
            return False
        return transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: Endereco):
        super().__init__(endereco)
        self._nome = nome.strip().title()
        self._data_nascimento = data_nascimento
        self._cpf = re.sub(r'[^0-9]', '', cpf)
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento
    
    @property
    def cpf(self) -> str:
        return self._cpf
    
    def to_dict(self) -> dict:
        return {
            "tipo": "pf",
            "nome": self._nome,
            "data_nascimento": self._data_nascimento,
            "cpf": self._cpf,
            "endereco": self._endereco.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PessoaFisica":
        return cls(
            nome=data["nome"],
            data_nascimento=data["data_nascimento"],
            cpf=data["cpf"],
            endereco=Endereco.from_dict(data["endereco"])
        )


@dataclass
class RegistroTransacao:
    tipo: str
    valor: float
    data: str
    
    def to_dict(self) -> dict:
        return {"tipo": self.tipo, "valor": self.valor, "data": self.data}
    
    @classmethod
    def from_dict(cls, data: dict) -> "RegistroTransacao":
        return cls(**data)


class Historico:
    def __init__(self):
        self._transacoes: List[RegistroTransacao] = []
    
    @property
    def transacoes(self) -> List[RegistroTransacao]:
        return self._transacoes.copy()
    
    def adicionar(self, transacao: "Transacao"):
        registro = RegistroTransacao(
            tipo=transacao.__class__.__name__,
            valor=transacao.valor,
            data=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        self._transacoes.append(registro)
    
    def to_dict(self) -> List[dict]:
        return [t.to_dict() for t in self._transacoes]
    
    @classmethod
    def from_dict(cls, data: List[dict]) -> "Historico":
        h = cls()
        h._transacoes = [RegistroTransacao.from_dict(t) for t in data]
        return h


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass
    
    @abstractmethod
    def registrar(self, conta: "Conta") -> bool:
        pass


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: "Conta") -> bool:
        if conta.sacar(self._valor):
            conta.historico.adicionar(self)
            return True
        return False


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: "Conta") -> bool:
        if conta.depositar(self._valor):
            conta.historico.adicionar(self)
            return True
        return False


class Transferencia(Transacao):
    def __init__(self, valor: float, conta_destino: "Conta"):
        self._valor = valor
        self._conta_destino = conta_destino
    
    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta_origem: "Conta") -> bool:
        if conta_origem.sacar(self._valor):
            if self._conta_destino.depositar(self._valor):
                conta_origem.historico.adicionar(self)
                self._conta_destino.historico.adicionar(Deposito(self._valor))
                return True
            conta_origem.depositar(self._valor)
        return False


class Conta:
    _contador = 0
    AGENCIA = "0001"
    
    def __init__(self, cliente: Cliente, numero: Optional[int] = None):
        Conta._contador += 1
        self._numero = numero or Conta._contador
        self._agencia = self.AGENCIA
        self._cliente = cliente
        self._saldo = 0.0
        self._historico = Historico()
        self._ativa = True
    
    @classmethod
    def set_contador(cls, valor: int):
        cls._contador = valor
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def historico(self) -> Historico:
        return self._historico
    
    @property
    def ativa(self) -> bool:
        return self._ativa
    
    def sacar(self, valor: float) -> bool:
        if not self._ativa:
            msg_erro("Conta inativa!")
            return False
        if valor <= 0:
            msg_erro("Valor deve ser positivo!")
            return False
        if valor > self._saldo:
            msg_erro(f"Saldo insuficiente! Disponível: {formatar_moeda(self._saldo)}")
            return False
        self._saldo -= valor
        return True
    
    def depositar(self, valor: float) -> bool:
        if not self._ativa:
            msg_erro("Conta inativa!")
            return False
        if valor <= 0:
            msg_erro("Valor deve ser positivo!")
            return False
        self._saldo += valor
        return True
    
    def to_dict(self) -> dict:
        return {
            "tipo": "corrente",
            "numero": self._numero,
            "agencia": self._agencia,
            "cpf_cliente": self._cliente.cpf if isinstance(self._cliente, PessoaFisica) else "",
            "saldo": self._saldo,
            "historico": self._historico.to_dict(),
            "ativa": self._ativa
        }
    
    @classmethod
    def from_dict(cls, data: dict, clientes: dict) -> "Conta":
        cpf = data.get("cpf_cliente", "")
        cliente = clientes.get(cpf)
        if not cliente:
            raise ValueError(f"Cliente {cpf} não encontrado")
        
        c = cls(cliente=cliente, numero=data["numero"])
        c._saldo = data.get("saldo", 0)
        c._historico = Historico.from_dict(data.get("historico", []))
        c._ativa = data.get("ativa", True)
        return c


class ContaCorrente(Conta):
    LIMITE_PADRAO = 500.0
    LIMITE_SAQUES = 3
    
    def __init__(self, cliente: Cliente, numero: Optional[int] = None,
                 limite: float = LIMITE_PADRAO, limite_saques: int = LIMITE_SAQUES):
        super().__init__(cliente, numero)
        self._limite = limite
        self._limite_saques = limite_saques
    
    @property
    def limite(self) -> float:
        return self._limite
    
    def saques_hoje(self) -> int:
        hoje = datetime.now().strftime("%d/%m/%Y")
        return len([t for t in self._historico.transacoes 
                    if t.tipo == "Saque" and t.data.startswith(hoje)])
    
    def sacar(self, valor: float) -> bool:
        if valor > self._limite:
            msg_erro(f"Excede limite de {formatar_moeda(self._limite)} por operação")
            return False
        if self.saques_hoje() >= self._limite_saques:
            msg_erro(f"Limite de {self._limite_saques} saques diários atingido")
            return False
        return super().sacar(valor)
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "tipo": "corrente",
            "limite": self._limite,
            "limite_saques": self._limite_saques
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict, clientes: dict) -> "ContaCorrente":
        cpf = data.get("cpf_cliente", "")
        cliente = clientes.get(cpf)
        if not cliente:
            raise ValueError(f"Cliente {cpf} não encontrado")
        
        c = cls(cliente=cliente, numero=data["numero"],
                limite=data.get("limite", cls.LIMITE_PADRAO),
                limite_saques=data.get("limite_saques", cls.LIMITE_SAQUES))
        c._saldo = data.get("saldo", 0)
        c._historico = Historico.from_dict(data.get("historico", []))
        c._ativa = data.get("ativa", True)
        return c


# ═══════════════════════════════════════════════════════════════════════════════
# PERSISTÊNCIA
# ═══════════════════════════════════════════════════════════════════════════════

class BancoDados:
    @staticmethod
    def inicializar():
        DATA_DIR.mkdir(exist_ok=True)
    
    @staticmethod
    def salvar_clientes(clientes: dict):
        with open(CLIENTES_FILE, 'w', encoding='utf-8') as f:
            json.dump({cpf: c.to_dict() for cpf, c in clientes.items()}, 
                     f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def carregar_clientes() -> dict:
        if not CLIENTES_FILE.exists():
            return {}
        with open(CLIENTES_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        clientes = {}
        for cpf, data in dados.items():
            try:
                clientes[cpf] = PessoaFisica.from_dict(data)
            except Exception as e:
                msg_erro(f"Erro ao carregar cliente {cpf}: {e}")
        return clientes
    
    @staticmethod
    def salvar_contas(contas: List[Conta]):
        with open(CONTAS_FILE, 'w', encoding='utf-8') as f:
            json.dump([c.to_dict() for c in contas], f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def carregar_contas(clientes: dict) -> List[Conta]:
        if not CONTAS_FILE.exists():
            return []
        with open(CONTAS_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        contas = []
        max_num = 0
        for data in dados:
            try:
                conta = ContaCorrente.from_dict(data, clientes)
                contas.append(conta)
                if conta.numero > max_num:
                    max_num = conta.numero
                if conta not in conta.cliente.contas:
                    conta.cliente.adicionar_conta(conta)
            except Exception as e:
                msg_erro(f"Erro ao carregar conta: {e}")
        
        Conta.set_contador(max_num)
        return contas


# ═══════════════════════════════════════════════════════════════════════════════
# SERVIÇO BANCÁRIO
# ═══════════════════════════════════════════════════════════════════════════════

class BancoService:
    def __init__(self):
        BancoDados.inicializar()
        self._clientes: dict = BancoDados.carregar_clientes()
        self._contas: List[Conta] = BancoDados.carregar_contas(self._clientes)
    
    @property
    def clientes(self) -> dict:
        return self._clientes
    
    @property
    def contas(self) -> List[Conta]:
        return self._contas
    
    def salvar(self):
        BancoDados.salvar_clientes(self._clientes)
        BancoDados.salvar_contas(self._contas)
    
    def buscar_cliente(self, cpf: str) -> Optional[Cliente]:
        return self._clientes.get(re.sub(r'[^0-9]', '', cpf))
    
    def criar_cliente(self, nome: str, data_nasc: str, cpf: str, 
                      endereco: Endereco) -> Optional[PessoaFisica]:
        if not validar_cpf(cpf):
            msg_erro("CPF inválido! 11 dígitos necessários.")
            return None
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)
        if cpf_limpo in self._clientes:
            msg_erro("CPF já cadastrado!")
            return None
        if not validar_data(data_nasc):
            msg_erro("Data inválida! Use dd-mm-aaaa")
            return None
        
        cliente = PessoaFisica(nome, data_nasc, cpf, endereco)
        self._clientes[cpf_limpo] = cliente
        self.salvar()
        return cliente
    
    def criar_conta(self, cpf: str) -> Optional[Conta]:
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            msg_erro("Cliente não encontrado!")
            return None
        conta = ContaCorrente(cliente)
        self._contas.append(conta)
        cliente.adicionar_conta(conta)
        self.salvar()
        return conta
    
    def buscar_conta(self, numero: int) -> Optional[Conta]:
        for c in self._contas:
            if c.numero == numero:
                return c
        return None
    
    def depositar(self, conta: Conta, valor: float) -> bool:
        t = Deposito(valor)
        if conta.cliente.realizar_transacao(conta, t):
            self.salvar()
            return True
        return False
    
    def sacar(self, conta: Conta, valor: float) -> bool:
        t = Saque(valor)
        if conta.cliente.realizar_transacao(conta, t):
            self.salvar()
            return True
        return False
    
    def transferir(self, origem: Conta, destino: Conta, valor: float) -> bool:
        if origem == destino:
            msg_erro("Contas devem ser diferentes!")
            return False
        t = Transferencia(valor, destino)
        if origem.cliente.realizar_transacao(origem, t):
            self.salvar()
            return True
        return False
    
    # Estatísticas para dashboard
    def total_saldo(self) -> float:
        return sum(c.saldo for c in self._contas)
    
    def total_transacoes(self) -> int:
        return sum(len(c.historico.transacoes) for c in self._contas)
    
    def contas_ativas(self) -> int:
        return sum(1 for c in self._contas if c.ativa)
    
    def media_saldo(self) -> float:
        if not self._contas:
            return 0
        return self.total_saldo() / len(self._contas)


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD E INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

class Dashboard:
    def __init__(self, banco: BancoService):
        self._banco = banco
    
    def exibir(self):
        """Exibe dashboard com estatísticas."""
        limpar_tela()

        interna = UI_LARGURA - 2
        titulo = titulo_gradiente(f" 📊 {PROJETO_NOME.upper()} DASHBOARD ")
        print(f"\n{C_PRIMARIA}╔{'═' * interna}╗{Cores.RESET}")
        print(f"{C_PRIMARIA}║{Cores.RESET}{ajustar_visual(titulo, interna, 'centro')}{C_PRIMARIA}║{Cores.RESET}")
        print(f"{C_PRIMARIA}╠{'═' * interna}╣{Cores.RESET}")
        
        # Painéis de estatísticas
        painel_clientes = criar_painel("CLIENTES", [
            f"{Cores.BOLD}{len(self._banco.clientes):>3}{Cores.RESET} cadastrados",
            f"{Cores.BOLD}{len(self._banco.contas):>3}{Cores.RESET} contas"
        ], "👥", C_INFO)
        
        painel_saldo = criar_painel("PATRIMÔNIO", [
            f"Total: {formatar_moeda(self._banco.total_saldo())}",
            f"Média: {formatar_moeda(self._banco.media_saldo())}"
        ], "💰", C_SUCESSO)
        
        painel_trans = criar_painel("MOVIMENTAÇÕES", [
            f"{Cores.BOLD}{self._banco.total_transacoes():>3}{Cores.RESET} transações",
            f"{Cores.BOLD}{self._banco.contas_ativas():>3}{Cores.RESET} contas ativas"
        ], "📈", C_SECUNDARIA)
        
        # Layout lado a lado
        linhas_clientes = painel_clientes.split("\n")
        linhas_saldo = painel_saldo.split("\n")
        linhas_trans = painel_trans.split("\n")
        
        max_linhas = max(len(linhas_clientes), len(linhas_saldo), len(linhas_trans))
        
        print()
        for i in range(max_linhas):
            c = linhas_clientes[i] if i < len(linhas_clientes) else " " * 34
            s = linhas_saldo[i] if i < len(linhas_saldo) else " " * 34
            t = linhas_trans[i] if i < len(linhas_trans) else " " * 34
            print(f"  {c}  {s}  {t}")
        
        # Gráfico de barras - saldos
        print(f"\n{C_PRIMARIA}  📊 TOP 5 CONTAS POR SALDO:{Cores.RESET}")
        print(f"  {Cores.DIM}{'─' * 66}{Cores.RESET}")
        
        contas_ordenadas = sorted(self._banco.contas, key=lambda x: x.saldo, reverse=True)[:5]
        max_saldo = max((c.saldo for c in contas_ordenadas), default=1)
        
        for conta in contas_ordenadas:
            nome = conta.cliente.nome[:15] if isinstance(conta.cliente, PessoaFisica) else "Cliente"
            barra = barra_progresso(conta.saldo, max_saldo, 25, C_SUCESSO)
            print(f"  {C_PRIMARIA}#{conta.numero:>2}{Cores.RESET} {nome:<15} {barra} {formatar_moeda(conta.saldo)}")
        
        print(f"  {Cores.DIM}{'─' * 66}{Cores.RESET}")
        
        # Últimas transações
        print(f"\n{C_PRIMARIA}  🕐 ÚLTIMAS TRANSAÇÕES:{Cores.RESET}")
        print(f"  {Cores.DIM}{'─' * 66}{Cores.RESET}")
        
        todas_trans = []
        for conta in self._banco.contas:
            for t in conta.historico.transacoes:
                todas_trans.append((t, conta))
        
        todas_trans.sort(key=lambda x: datetime.strptime(x[0].data, "%d/%m/%Y %H:%M:%S"), reverse=True)
        
        for t, conta in todas_trans[:5]:
            icone = "💰" if t.tipo == "Deposito" else ("💸" if t.tipo == "Saque" else "🔄")
            cor = C_SUCESSO if t.tipo == "Deposito" else (C_ERRO if t.tipo == "Saque" else C_INFO)
            nome = conta.cliente.nome[:12] if isinstance(conta.cliente, PessoaFisica) else "Cliente"
            print(f"  {icone} {Cores.DIM}{t.data}{Cores.RESET} | {cor}{t.tipo:<12}{Cores.RESET} | {nome:<12} | {formatar_moeda(t.valor)}")
        
        if not todas_trans:
            print(f"  {Cores.DIM}Nenhuma transação registrada{Cores.RESET}")
        
        print(f"  {Cores.DIM}{'─' * 66}{Cores.RESET}")
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class MenuUI:
    def __init__(self):
        self._banco = BancoService()
        self._dashboard = Dashboard(self._banco)
    
    def mostrar_menu(self) -> str:
        """Exibe menu estilizado."""
        opcoes = [
            ("d", "💰", "Depositar", C_SUCESSO),
            ("s", "💸", "Sacar", C_ERRO),
            ("e", "📄", "Extrato", C_INFO),
            ("t", "🔄", "Transferir", C_SECUNDARIA),
            ("c", "➕", "Nova Conta", C_PRIMARIA),
            ("l", "📋", "Listar Contas", C_PRIMARIA),
            ("u", "👤", "Novo Cliente", C_DESTAQUE),
            ("v", "👥", "Listar Clientes", C_DESTAQUE),
            ("dash", "📊", "Dashboard", C_AVISO),
            ("q", "🚪", "Sair", Cores.LIGHT_RED),
        ]
        
        interna = UI_LARGURA - 2
        print(f"\n{C_PRIMARIA}╔{'═' * interna}╗{Cores.RESET}")
        print(f"{C_PRIMARIA}║{Cores.RESET}{ajustar_visual(titulo_gradiente(f'🏦 {PROJETO_NOME.upper()} MENU'), interna, 'centro')}{C_PRIMARIA}║{Cores.RESET}")
        print(f"{C_PRIMARIA}╠{'═' * interna}╣{Cores.RESET}")
        
        for i in range(0, len(opcoes), 2):
            op1 = opcoes[i]
            linha = f"  {op1[3]}{Cores.BOLD}[{op1[0]}]{Cores.RESET} {op1[1]} {op1[2]:<15}{Cores.RESET}"
            
            if i + 1 < len(opcoes):
                op2 = opcoes[i + 1]
                linha += f"    {op2[3]}{Cores.BOLD}[{op2[0]}]{Cores.RESET} {op2[1]} {op2[2]:<15}{Cores.RESET}"
            
            print(f"{C_PRIMARIA}║{Cores.RESET}{ajustar_visual(linha, interna)}{C_PRIMARIA}║{Cores.RESET}")

        print(f"{C_PRIMARIA}╚{'═' * interna}╝{Cores.RESET}")
        return input_colorido("Selecione uma opção:", C_DESTAQUE, "👉").lower()
    
    def selecionar_conta(self, msg: str = "Selecione a conta") -> Optional[Conta]:
        """Interface de seleção de conta."""
        if not self._banco.contas:
            msg_erro("Nenhuma conta cadastrada!")
            return None
        
        print(f"\n{C_INFO}📋 {msg}:{Cores.RESET}")
        print(f"{Cores.DIM}{'─' * 50}{Cores.RESET}")
        
        for conta in self._banco.contas:
            if isinstance(conta.cliente, PessoaFisica):
                nome = conta.cliente.nome[:25]
                status = f"{C_SUCESSO}●{Cores.RESET}" if conta.ativa else f"{C_ERRO}●{Cores.RESET}"
                print(f"  {status} [{C_PRIMARIA}{conta.numero}{Cores.RESET}] {nome:<25} {formatar_moeda(conta.saldo)}")
        
        print(f"{Cores.DIM}{'─' * 50}{Cores.RESET}")
        
        try:
            num = int(input_colorido("Número da conta:", C_PRIMARIA, "→"))
            conta = self._banco.buscar_conta(num)
            if not conta:
                msg_erro("Conta não encontrada!")
            return conta
        except ValueError:
            msg_erro("Número inválido!")
            return None
    
    def tela_depositar(self):
        limpar_tela()
        print(criar_caixa("DEPÓSITO", cor_titulo=C_SUCESSO, icone="💰"))
        
        conta = self.selecionar_conta()
        if not conta:
            return
        
        valor = input_valor("Informe o valor:")
        if valor and self._banco.depositar(conta, valor):
            msg_sucesso(f"Depósito de {formatar_moeda(valor)} realizado!")
            msg_info(f"Novo saldo: {formatar_moeda(conta.saldo)}")
    
    def tela_sacar(self):
        limpar_tela()
        print(criar_caixa("SAQUE", cor_titulo=C_ERRO, icone="💸"))
        
        conta = self.selecionar_conta()
        if not conta:
            return
        
        if isinstance(conta, ContaCorrente):
            restantes = conta.limite_saques - conta.saques_hoje()
            print(f"\n{C_INFO}  ℹ  Limite: {formatar_moeda(conta.limite)} | Saques hoje: {conta.saques_hoje()}/{conta.limite_saques}{Cores.RESET}")
            print(f"  {barra_progresso(conta.saques_hoje(), conta.limite_saques, 20, C_AVISO if restantes <= 1 else C_SUCESSO)}")
        
        valor = input_valor("Informe o valor:")
        if valor and self._banco.sacar(conta, valor):
            msg_sucesso(f"Saque de {formatar_moeda(valor)} realizado!")
            msg_info(f"Novo saldo: {formatar_moeda(conta.saldo)}")
    
    def tela_extrato(self):
        limpar_tela()
        conta = self.selecionar_conta()
        if not conta:
            return
        
        cliente = conta.cliente
        nome = cliente.nome if isinstance(cliente, PessoaFisica) else "Cliente"

        largura = 68
        col_data = 19
        col_tipo = 18
        col_valor = largura - (col_data + col_tipo + 8)

        def linha_colunas(data: str, tipo: str, valor: str) -> str:
            conteudo = (
                " "
                + ajustar_visual(data, col_data)
                + " │ "
                + ajustar_visual(tipo, col_tipo)
                + " │ "
                + ajustar_visual(valor, col_valor, "direita")
                + " "
            )
            return f"{C_PRIMARIA}│{Cores.RESET}{conteudo}{C_PRIMARIA}│{Cores.RESET}"

        print(f"\n{C_PRIMARIA}┌{'─' * largura}┐{Cores.RESET}")
        print(f"{C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f'{Cores.BOLD} EXTRATO BANCÁRIO {Cores.RESET}', largura, 'centro')}{C_PRIMARIA}│{Cores.RESET}")
        print(f"{C_PRIMARIA}├{'─' * largura}┤{Cores.RESET}")
        print(f"{C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' {C_DESTAQUE}Cliente:{Cores.RESET} {limitar_texto(nome, 45)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
        print(f"{C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' {C_DESTAQUE}Conta:{Cores.RESET} {conta.numero} | {C_DESTAQUE}Agência:{Cores.RESET} {conta.agencia}', largura)}{C_PRIMARIA}│{Cores.RESET}")
        print(f"{C_PRIMARIA}├{'─' * largura}┤{Cores.RESET}")
        print(linha_colunas(f"{Cores.DIM}DATA/HORA{Cores.RESET}", f"{Cores.DIM}TIPO{Cores.RESET}", f"{Cores.DIM}VALOR{Cores.RESET}"))
        print(f"{C_PRIMARIA}├{'─' * largura}┤{Cores.RESET}")

        trans = conta.historico.transacoes
        if not trans:
            vazio = f"{Cores.DIM}Nenhuma movimentação registrada{Cores.RESET}"
            print(f"{C_PRIMARIA}│{Cores.RESET}{ajustar_visual(vazio, largura, 'centro')}{C_PRIMARIA}│{Cores.RESET}")
        else:
            mapa_tipos = {
                "DEPOSITO": "DEPOSITO",
                "SAQUE": "SAQUE",
                "TRANSFERENCIA": "TRANSF.SAIDA",
                "DEPOSITOTRANSFERENCIA": "TRANSF.ENTRADA",
            }
            for t in trans:
                tipo_fmt = mapa_tipos.get(t.tipo.upper(), t.tipo.upper())
                valor_fmt = formatar_moeda(t.valor)
                print(linha_colunas(f"{Cores.DIM}{t.data}{Cores.RESET}", tipo_fmt, valor_fmt))

        print(f"{C_PRIMARIA}├{'─' * largura}┤{Cores.RESET}")
        saldo_valor = formatar_moeda(conta.saldo)
        rotulo = f" {C_SUCESSO}{Cores.BOLD}SALDO ATUAL:{Cores.RESET}"
        espacos = max(1, largura - largura_visual(rotulo) - largura_visual(saldo_valor) - 1)
        print(f"{C_PRIMARIA}│{Cores.RESET}{rotulo}{' ' * espacos}{saldo_valor} {C_PRIMARIA}│{Cores.RESET}")
        print(f"{C_PRIMARIA}└{'─' * largura}┘{Cores.RESET}")
    
    def tela_transferir(self):
        limpar_tela()
        print(criar_caixa("TRANSFERÊNCIA", cor_titulo=C_SECUNDARIA, icone="🔄"))
        
        msg_info("Conta de ORIGEM:")
        origem = self.selecionar_conta()
        if not origem:
            return
        
        print(f"\n{C_SECUNDARIA}{'─' * 50}{Cores.RESET}")
        msg_info("Conta de DESTINO:")
        destino = self.selecionar_conta()
        if not destino:
            return
        
        if origem == destino:
            msg_erro("Contas devem ser diferentes!")
            return
        
        print(f"\n  {C_DESTAQUE}De:{Cores.RESET}    Conta #{origem.numero} ({origem.cliente.nome[:20]})")
        print(f"  {C_DESTAQUE}Para:{Cores.RESET}  Conta #{destino.numero} ({destino.cliente.nome[:20]})")
        
        valor = input_valor("Valor a transferir:")
        if valor and self._banco.transferir(origem, destino, valor):
            msg_sucesso(f"Transferência de {formatar_moeda(valor)} realizada!")
    
    def tela_nova_conta(self):
        limpar_tela()
        print(criar_caixa("NOVA CONTA", cor_titulo=C_PRIMARIA, icone="➕"))
        
        cpf = input_cpf()
        cliente = self._banco.buscar_cliente(cpf)
        
        if not cliente:
            msg_erro("Cliente não encontrado!")
            if confirmar("Cadastrar novo cliente?"):
                self.tela_novo_cliente()
            return
        
        msg_info(f"Cliente: {cliente.nome}")
        conta = self._banco.criar_conta(cliente.cpf)
        if conta:
            msg_sucesso(f"Conta #{conta.numero} criada!")
            print(f"\n  {C_DESTAQUE}Dados da conta:{Cores.RESET}")
            largura = 40
            print(f"  ┌{'─' * largura}┐")
            print(f"  │{ajustar_visual(f' Agência: {conta.agencia}', largura)}│")
            print(f"  │{ajustar_visual(f' Conta:   {conta.numero}', largura)}│")
            print(f"  │{ajustar_visual(f' Titular: {limitar_texto(cliente.nome, 30)}', largura)}│")
            print(f"  └{'─' * largura}┘")
    
    def tela_listar_contas(self):
        limpar_tela()
        print(criar_caixa("CONTAS CADASTRADAS", cor_titulo=C_PRIMARIA, icone="📋"))
        
        if not self._banco.contas:
            msg_aviso("Nenhuma conta cadastrada.")
            return
        
        print(f"\n  {C_DESTAQUE}Total: {len(self._banco.contas)} contas{Cores.RESET}\n")
        
        for conta in self._banco.contas:
            if isinstance(conta.cliente, PessoaFisica):
                status = f"{C_SUCESSO}ATIVA{Cores.RESET}" if conta.ativa else f"{C_ERRO}INATIVA{Cores.RESET}"
                largura = 60
                cabecalho = f"{Cores.BOLD}Conta #{conta.numero}{Cores.RESET}"
                prefixo = f" {cabecalho}"
                espacos = max(1, largura - largura_visual(prefixo) - largura_visual(status) - 1)

                print(f"  {C_PRIMARIA}┌{'─' * largura}┐{Cores.RESET}")
                print(f"  {C_PRIMARIA}│{Cores.RESET}{prefixo}{' ' * espacos}{status} {C_PRIMARIA}│{Cores.RESET}")
                print(f"  {C_PRIMARIA}├{'─' * largura}┤{Cores.RESET}")
                print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' Titular: {limitar_texto(conta.cliente.nome, 45)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
                print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' CPF:     {formatar_cpf(conta.cliente.cpf)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
                print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' Saldo:   {formatar_moeda(conta.saldo)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
                if isinstance(conta, ContaCorrente):
                    print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' Limite:  {formatar_moeda(conta.limite)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
                print(f"  {C_PRIMARIA}└{'─' * largura}┘{Cores.RESET}")
                print()
    
    def tela_novo_cliente(self):
        limpar_tela()
        print(criar_caixa("NOVO CLIENTE", cor_titulo=C_DESTAQUE, icone="👤"))
        
        cpf = input_cpf()
        if not validar_cpf(cpf):
            msg_erro("CPF inválido! 11 dígitos.")
            return
        if self._banco.buscar_cliente(cpf):
            msg_erro("CPF já cadastrado!")
            return
        
        nome = input_colorido("Nome completo:", C_TEXTO, "📝").strip()
        if not nome:
            msg_erro("Nome obrigatório!")
            return
        
        data_nasc = input_colorido("Data nascimento (dd-mm-aaaa):", C_TEXTO, "🎂").strip()
        if not validar_data(data_nasc):
            msg_erro("Data inválida!")
            return
        
        print(f"\n{C_INFO}  📍 Endereço:{Cores.RESET}")
        logradouro = input_colorido("Logradouro:", C_TEXTO, "  →").strip()
        numero = input_colorido("Número:", C_TEXTO, "  →").strip()
        bairro = input_colorido("Bairro:", C_TEXTO, "  →").strip()
        cidade = input_colorido("Cidade:", C_TEXTO, "  →").strip()
        uf = input_colorido("UF (ex: SP):", C_TEXTO, "  →").strip().upper()
        cep = input_colorido("CEP (opcional):", C_TEXTO, "  →").strip()
        
        if not all([logradouro, numero, bairro, cidade, uf]):
            msg_erro("Endereço incompleto!")
            return
        
        endereco = Endereco(logradouro, numero, bairro, cidade, uf, cep)
        cliente = self._banco.criar_cliente(nome, data_nasc, cpf, endereco)
        
        if cliente:
            msg_sucesso(f"Cliente {cliente.nome} cadastrado!")
            if confirmar("Criar conta para este cliente?"):
                conta = self._banco.criar_conta(cliente.cpf)
                if conta:
                    msg_sucesso(f"Conta #{conta.numero} criada!")
    
    def tela_listar_clientes(self):
        limpar_tela()
        print(criar_caixa("CLIENTES CADASTRADOS", cor_titulo=C_DESTAQUE, icone="👥"))
        
        if not self._banco.clientes:
            msg_aviso("Nenhum cliente cadastrado.")
            return
        
        print(f"\n  {C_DESTAQUE}Total: {len(self._banco.clientes)} clientes{Cores.RESET}\n")
        
        for cliente in self._banco.clientes.values():
            largura = 60
            endereco_linha = str(cliente.endereco).replace("\n", " ")
            print(f"  {C_PRIMARIA}┌{'─' * largura}┐{Cores.RESET}")
            print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f' 👤 {Cores.BOLD}{limitar_texto(cliente.nome, 50)}{Cores.RESET}', largura)}{C_PRIMARIA}│{Cores.RESET}")
            print(f"  {C_PRIMARIA}├{'─' * largura}┤{Cores.RESET}")
            print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f'    CPF: {formatar_cpf(cliente.cpf)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
            print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f'    Nasc: {cliente.data_nascimento}', largura)}{C_PRIMARIA}│{Cores.RESET}")
            print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f'    End: {limitar_texto(endereco_linha, 48)}', largura)}{C_PRIMARIA}│{Cores.RESET}")
            print(f"  {C_PRIMARIA}│{Cores.RESET}{ajustar_visual(f'    Contas: {C_SUCESSO}{len(cliente.contas)}{Cores.RESET}', largura)}{C_PRIMARIA}│{Cores.RESET}")
            print(f"  {C_PRIMARIA}└{'─' * largura}┘{Cores.RESET}")
            print()
    
    def executar(self):
        limpar_tela()
        
        # Splash screen
        print("\n" * 5)
        splash = """
         ____                   __        __    
        / __ )____  ____  _____/ /_____ _/ /____
       / __  / __ \\/ __ \\/ ___/ __/ __ `/ / ___/
      / /_/ / /_/ / /_/ / /__/ /_/ /_/ / (__  )
     /_____/\\____/\\____/\\___/\\__/\\__,_/_/____/
        """
        print(Cores.gradient(splash, (0, 255, 255), (255, 0, 255)))
        largura = 68
        print(f"\n{C_PRIMARIA}╔{'═' * largura}╗{Cores.RESET}")
        print(f"{C_PRIMARIA}║{Cores.RESET}{ajustar_visual(titulo_gradiente(f'Bem-vindo ao {PROJETO_NOME} {PROJETO_VERSAO}'), largura, 'centro')}{C_PRIMARIA}║{Cores.RESET}")
        print(f"{C_PRIMARIA}╚{'═' * largura}╝{Cores.RESET}")
        
        animacao_carregamento("Inicializando sistema", 0.8)
        
        while True:
            self._dashboard.exibir()
            opcao = self.mostrar_menu()
            
            if opcao == "q":
                limpar_tela()
                interna = UI_LARGURA - 2
                print(f"\n{C_SUCESSO}╔{'═' * interna}╗{Cores.RESET}")
                print(f"{C_SUCESSO}║{Cores.RESET}{ajustar_visual(titulo_gradiente(f'Obrigado por usar o {PROJETO_NOME}!'), interna, 'centro')}{C_SUCESSO}║{Cores.RESET}")
                print(f"{C_SUCESSO}╚{'═' * interna}╝{Cores.RESET}\n")
                break
            
            elif opcao == "d":
                self.tela_depositar()
            elif opcao == "s":
                self.tela_sacar()
            elif opcao == "e":
                self.tela_extrato()
            elif opcao == "t":
                self.tela_transferir()
            elif opcao == "c":
                self.tela_nova_conta()
            elif opcao == "l":
                self.tela_listar_contas()
            elif opcao == "u":
                self.tela_novo_cliente()
            elif opcao == "v":
                self.tela_listar_clientes()
            elif opcao in ("dash", "dashboard", "dd"):
                pass  # Dashboard já mostra no início do loop
            else:
                msg_erro("Opção inválida!")
            
            input(f"\n{C_PRIMARIA}Pressione ENTER para continuar...{Cores.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    try:
        app = MenuUI()
        app.executar()
    except KeyboardInterrupt:
        print(f"\n\n{C_AVISO}⚠ Operação cancelada.{Cores.RESET}")
    except Exception as e:
        msg_erro(f"Erro: {e}")
        raise


if __name__ == "__main__":
    main()
