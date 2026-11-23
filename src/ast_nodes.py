"""Árvore sintática abstrata (AST) da MiniLang.

Cada classe corresponde a uma construção da gramática (docs/gramatica.md, seção 3).
A AST guarda apenas o que é necessário para executar o programa:

- não há nós para parênteses, ';', '{' '}' ou para os níveis intermediários da
  gramática (expressao -> comparacao -> soma -> termo -> fator);
- a precedência e a associatividade ficam registradas na FORMA da árvore:
  em 1 + 2 * 3 o nó '*' fica abaixo do nó '+'.

Todo nó guarda linha e coluna do token que o originou, para que o interpretador
possa reportar erros semânticos com posição (catálogo de erros, item f).
"""

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class No:
    """Base de todos os nós. linha/coluna são nomeados e ficam no fim do construtor:
    Num(1) nos testes, Num(1, linha=2, coluna=5) no parser.

    compare=False: duas árvores com a mesma estrutura são iguais (==) mesmo que
    venham de posições diferentes do código, o que simplifica os testes.
    """

    linha: int = field(default=0, compare=False)
    coluna: int = field(default=0, compare=False)


# ---- Expressões -------------------------------------------------------------


@dataclass
class Num(No):
    """Literal inteiro (token NUM)."""

    valor: int


@dataclass
class Bool(No):
    """Literal booleano (tokens TRUE / FALSE)."""

    valor: bool


@dataclass
class Var(No):
    """Uso de variável dentro de uma expressão (token ID)."""

    nome: str


@dataclass
class BinOp(No):
    """Operação binária: + - * / < > <= >= == !=.

    Um único nó representa os níveis soma, termo e comparacao da gramática;
    o operador é guardado pelo lexema ("+", "<=", ...).
    """

    op: str
    esq: No
    dir: No


# ---- Comandos ---------------------------------------------------------------


@dataclass
class Bloco(No):
    """bloco = "{" { comando } "}" ."""

    comandos: list[No]


@dataclass
class Atribuicao(No):
    """atribuicao = ID "=" expressao ."""

    nome: str
    expressao: No


@dataclass
class Print(No):
    """impressao = "print" "(" expressao ")" ."""

    expressao: No


@dataclass
class If(No):
    """condicional = "if" "(" expressao ")" bloco [ "else" bloco ] .

    senao é None quando não há else.
    """

    condicao: No
    entao: Bloco
    senao: Bloco | None = None


@dataclass
class While(No):
    """enquanto = "while" "(" expressao ")" bloco ."""

    condicao: No
    corpo: Bloco


@dataclass
class For(No):
    """para = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco .

    As três cláusulas são obrigatórias.
    """

    inicializacao: Atribuicao
    condicao: No
    atualizacao: Atribuicao
    corpo: Bloco


@dataclass
class Programa(No):
    """programa = { comando } ."""

    comandos: list[No]


# ---- Visualização -----------------------------------------------------------


def formatar(no, nivel=0):
    """Devolve a AST como texto indentado (útil para o relatório e o vídeo).

    Exemplo para 1 + 2 * 3:
        BinOp +
          Num 1
          BinOp *
            Num 2
            Num 3
    """
    pad = "  " * nivel
    if isinstance(no, (Num, Bool)):
        texto = "true" if no.valor is True else "false" if no.valor is False else no.valor
        return f"{pad}{type(no).__name__} {texto}"
    if isinstance(no, Var):
        return f"{pad}Var {no.nome}"
    if isinstance(no, BinOp):
        return "\n".join(
            [f"{pad}BinOp {no.op}", formatar(no.esq, nivel + 1), formatar(no.dir, nivel + 1)]
        )
    if isinstance(no, Atribuicao):
        return f"{pad}Atribuicao {no.nome}\n{formatar(no.expressao, nivel + 1)}"
    if isinstance(no, Print):
        return f"{pad}Print\n{formatar(no.expressao, nivel + 1)}"
    if isinstance(no, (Programa, Bloco)):
        filhos = [formatar(c, nivel + 1) for c in no.comandos]
        return "\n".join([f"{pad}{type(no).__name__}", *filhos])
    if isinstance(no, If):
        partes = [f"{pad}If", formatar(no.condicao, nivel + 1), formatar(no.entao, nivel + 1)]
        if no.senao is not None:
            partes.append(formatar(no.senao, nivel + 1))
        return "\n".join(partes)
    if isinstance(no, While):
        return "\n".join(
            [f"{pad}While", formatar(no.condicao, nivel + 1), formatar(no.corpo, nivel + 1)]
        )
    if isinstance(no, For):
        return "\n".join(
            [
                f"{pad}For",
                formatar(no.inicializacao, nivel + 1),
                formatar(no.condicao, nivel + 1),
                formatar(no.atualizacao, nivel + 1),
                formatar(no.corpo, nivel + 1),
            ]
        )
    raise TypeError(f"nó desconhecido: {no!r}")
