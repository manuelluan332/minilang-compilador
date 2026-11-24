"""Interpretador da MiniLang: tabela de símbolos e execução sobre a AST."""

from dataclasses import dataclass

# Nomes dos tipos da MiniLang (usados nas mensagens de erro e nas verificações).
TIPO_INT = "int"
TIPO_BOOL = "bool"


class ErroSemantico(Exception):
    """Erro detectado durante a execução (restrições S1–S5 da gramática)."""

    def __init__(self, mensagem, linha=None, coluna=None):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        posicao = f" (linha {linha}, coluna {coluna})" if linha is not None else ""
        super().__init__(f"Erro semântico{posicao}: {mensagem}")


def tipo_de(valor):
    """Devolve o tipo MiniLang de um valor Python.

    O teste de bool vem ANTES do de int: em Python, bool é subclasse de int
    (isinstance(True, int) == True), então a ordem inversa classificaria
    true como inteiro e deixaria passar operações como 1 + true.
    """
    if type(valor) is bool:
        return TIPO_BOOL
    if type(valor) is int:
        return TIPO_INT
    raise TypeError(f"valor sem tipo MiniLang: {valor!r}")


def dividir(a, b, linha=None, coluna=None):
    """Divisão inteira da MiniLang: trunca em direção a zero (S3).

    O operador // do Python arredonda para baixo: (-7) // 2 == -4. A MiniLang
    segue C e Java e trunca: -7 / 2 == -3. Por isso o quociente é calculado
    sobre os valores absolutos e o sinal é aplicado depois.
    """
    if b == 0:
        raise ErroSemantico("divisão por zero", linha, coluna)
    quociente = abs(a) // abs(b)
    return quociente if (a < 0) == (b < 0) else -quociente


def formatar_valor(valor):
    """Texto que o print mostra: booleanos como 'true'/'false', como no código."""
    if tipo_de(valor) == TIPO_BOOL:
        return "true" if valor else "false"
    return str(valor)


@dataclass
class Simbolo:
    """Entrada da tabela de símbolos."""

    nome: str
    tipo: str  # TIPO_INT ou TIPO_BOOL
    valor: int | bool


class TabelaSimbolos:
    """Tabela de símbolos com escopo único (global).

    Estrutura: dicionário nome -> Simbolo. Um escopo basta porque a MiniLang
    não tem funções nem escopo aninhado (fora de escopo no enunciado):
    variáveis criadas dentro de um bloco continuam visíveis depois dele.
    """

    def __init__(self):
        self._simbolos = {}

    def definir(self, nome, valor):
        """Inserção (ou atualização) de uma variável.

        A tipagem é dinâmica: uma nova atribuição substitui valor e tipo.
        """
        self._simbolos[nome] = Simbolo(nome, tipo_de(valor), valor)

    def buscar(self, nome, linha=None, coluna=None):
        """Busca de uma variável. Lança ErroSemantico se ela não existir (S1)."""
        simbolo = self._simbolos.get(nome)
        if simbolo is None:
            raise ErroSemantico(f"variável '{nome}' não definida", linha, coluna)
        return simbolo

    def existe(self, nome):
        return nome in self._simbolos

    def __len__(self):
        return len(self._simbolos)
