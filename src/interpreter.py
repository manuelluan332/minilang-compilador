"""Interpretador da MiniLang: tabela de símbolos e execução sobre a AST.

Uso (a partir do código-fonte, depois que o parser estiver integrado):
    python -m src.interpreter exemplos/programa_valido.ml
"""

import sys
from dataclasses import dataclass

from src.ast_nodes import (
    Atribuicao,
    BinOp,
    Bloco,
    Bool,
    For,
    If,
    Num,
    Print,
    Programa,
    Var,
    While,
)

# Nomes dos tipos da MiniLang (usados nas mensagens de erro e nas verificações).
TIPO_INT = "int"
TIPO_BOOL = "bool"

# Limite de iterações de um único laço (while ou for). Acima dele, o laço é
# considerado infinito e a execução é interrompida com erro (item g).
LIMITE_ITERACOES = 100_000

OPS_ARITMETICOS = {"+", "-", "*", "/"}
OPS_ORDEM = {"<", ">", "<=", ">="}
OPS_IGUALDADE = {"==", "!="}


class ErroSemantico(Exception):
    """Erro detectado durante a execução (restrições S1–S5 da gramática).

    O formato da mensagem é o mesmo das outras fases:
        Erro semântico na linha X, coluna Y: <mensagem>
    """

    def __init__(self, mensagem, linha=None, coluna=None):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        posicao = f" na linha {linha}, coluna {coluna}" if linha is not None else ""
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


# ---- Execução sobre a AST ----------------------------------------------------


def _posicao(no):
    """(linha, coluna) do nó; nós montados à mão (sem parser) têm posição 0."""
    return (no.linha, no.coluna) if no.linha else (None, None)


class Interpretador:
    """Executa a AST percorrendo-a recursivamente (semântica operacional).

    - Comandos (Programa, Bloco, Atribuicao, Print, If, While, For) são
      executados por _executar e alteram a tabela de símbolos ou a saída.
    - Expressões (Num, Bool, Var, BinOp) são avaliadas por _avaliar e
      devolvem um valor Python: int para inteiro, bool para booleano.

    A verificação de tipos (S2, S4, S5) é feita no momento da execução, porque
    a tipagem é dinâmica: o tipo de uma variável é o do último valor atribuído.
    """

    def __init__(self, escrever=print, limite_iteracoes=LIMITE_ITERACOES):
        self.tabela = TabelaSimbolos()
        self.escrever = escrever
        self.limite_iteracoes = limite_iteracoes

    def executar(self, programa):
        self._executar(programa)

    # ---- comandos -----------------------------------------------------------

    def _executar(self, no):
        if isinstance(no, (Programa, Bloco)):
            for comando in no.comandos:
                self._executar(comando)
        elif isinstance(no, Atribuicao):
            self.tabela.definir(no.nome, self._avaliar(no.expressao))
        elif isinstance(no, Print):
            self.escrever(formatar_valor(self._avaliar(no.expressao)))
        elif isinstance(no, If):
            if self._condicao(no.condicao, "if"):
                self._executar(no.entao)
            elif no.senao is not None:
                self._executar(no.senao)
        elif isinstance(no, While):
            iteracoes = 0
            while self._condicao(no.condicao, "while"):
                iteracoes = self._contar_iteracao(iteracoes, no, "while")
                self._executar(no.corpo)
        elif isinstance(no, For):
            # for (ini; cond; atu) { corpo }  ≡  ini; while (cond) { corpo; atu; }
            self._executar(no.inicializacao)
            iteracoes = 0
            while self._condicao(no.condicao, "for"):
                iteracoes = self._contar_iteracao(iteracoes, no, "for")
                self._executar(no.corpo)
                self._executar(no.atualizacao)
        else:
            raise TypeError(f"comando desconhecido: {no!r}")

    def _condicao(self, expressao, comando):
        """Avalia a condição de if/while/for e exige que seja booleana (S4)."""
        valor = self._avaliar(expressao)
        if tipo_de(valor) != TIPO_BOOL:
            raise ErroSemantico(
                f"a condição do {comando} deve ser booleana, mas é {tipo_de(valor)}",
                *_posicao(expressao),
            )
        return valor

    def _contar_iteracao(self, iteracoes, no, comando):
        iteracoes += 1
        if iteracoes > self.limite_iteracoes:
            raise ErroSemantico(
                f"o {comando} excedeu o limite de {self.limite_iteracoes} iterações "
                "(provável laço infinito)",
                *_posicao(no),
            )
        return iteracoes

    # ---- expressões ---------------------------------------------------------

    def _avaliar(self, no):
        if isinstance(no, (Num, Bool)):
            return no.valor
        if isinstance(no, Var):
            return self.tabela.buscar(no.nome, *_posicao(no)).valor  # S1
        if isinstance(no, BinOp):
            return self._binop(no)
        raise TypeError(f"expressão desconhecida: {no!r}")

    def _binop(self, no):
        esq = self._avaliar(no.esq)
        dir = self._avaliar(no.dir)
        t_esq, t_dir = tipo_de(esq), tipo_de(dir)
        op = no.op
        linha, coluna = _posicao(no)

        if op in OPS_ARITMETICOS or op in OPS_ORDEM:
            # S2 (+ - * /) e S5 (< > <= >=): os dois operandos devem ser inteiros
            if t_esq != TIPO_INT or t_dir != TIPO_INT:
                raise ErroSemantico(
                    f"operador '{op}' exige operandos inteiros, mas recebeu "
                    f"{t_esq} e {t_dir}",
                    linha,
                    coluna,
                )
            if op == "+":
                return esq + dir
            if op == "-":
                return esq - dir
            if op == "*":
                return esq * dir
            if op == "/":
                return dividir(esq, dir, linha, coluna)  # S3
            if op == "<":
                return esq < dir
            if op == ">":
                return esq > dir
            if op == "<=":
                return esq <= dir
            return esq >= dir

        if op in OPS_IGUALDADE:
            # S5 (== !=): operandos do mesmo tipo. Sem esta verificação, o Python
            # diria que 1 == true é verdadeiro (True é subclasse de int).
            if t_esq != t_dir:
                raise ErroSemantico(
                    f"operador '{op}' exige operandos do mesmo tipo, mas recebeu "
                    f"{t_esq} e {t_dir}",
                    linha,
                    coluna,
                )
            return esq == dir if op == "==" else esq != dir

        raise TypeError(f"operador desconhecido: {op!r}")


def executar(programa, escrever=print, limite_iteracoes=LIMITE_ITERACOES):
    """Executa uma AST (nó Programa) e devolve a tabela de símbolos final."""
    interpretador = Interpretador(escrever, limite_iteracoes)
    interpretador.executar(programa)
    return interpretador.tabela


if __name__ == "__main__":
    # Pipeline completo: lexer -> parser -> interpretador. Depende do
    # src/parser.py expor parse(tokens) devolvendo um nó Programa.
    from src.lexer import LexerError, tokenizar
    from src import parser

    if len(sys.argv) != 2:
        print("uso: python -m src.interpreter <arquivo.ml>")
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8-sig") as arquivo:
        texto = arquivo.read()
    try:
        executar(parser.parse(tokenizar(texto)))
    except (LexerError, ErroSemantico, getattr(parser, "ParserError", LexerError)) as erro:
        print(erro)
        sys.exit(1)
