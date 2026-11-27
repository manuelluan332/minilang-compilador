"""Testes do parser com entradas VÁLIDAS.

Resultado esperado: analisar() não lança erro e devolve a AST indicada.
"""

from pathlib import Path

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
from src.parser import analisar

RAIZ = Path(__file__).resolve().parents[2]


def expr(codigo):
    """AST da expressão em 'x = <codigo>;'."""
    return analisar(f"x = {codigo};").comandos[0].expressao


# --- Precedência e associatividade ---------------------------------------------


def test_multiplicacao_antes_da_soma():
    assert expr("1+2*3") == BinOp("+", Num(1), BinOp("*", Num(2), Num(3)))


def test_parenteses_mudam_o_agrupamento():
    assert expr("(1+2)*3") == BinOp("*", BinOp("+", Num(1), Num(2)), Num(3))


def test_subtracao_associativa_a_esquerda():
    # a - b - c == (a - b) - c
    assert expr("a - b - c") == BinOp("-", BinOp("-", Var("a"), Var("b")), Var("c"))


def test_divisao_associativa_a_esquerda():
    assert expr("8 / 4 / 2") == BinOp("/", BinOp("/", Num(8), Num(4)), Num(2))


def test_comparacao_tem_menor_precedencia():
    assert expr("x + 1 <= 2 * y") == BinOp(
        "<=", BinOp("+", Var("x"), Num(1)), BinOp("*", Num(2), Var("y"))
    )


def test_todos_os_operadores_de_comparacao():
    for op in ["<", ">", "<=", ">=", "==", "!="]:
        assert expr(f"a {op} b") == BinOp(op, Var("a"), Var("b"))


def test_literais_booleanos():
    assert expr("true") == Bool(True)
    assert expr("false") == Bool(False)


# --- Comandos --------------------------------------------------------------------


def test_programa_vazio():
    assert analisar("") == Programa([])


def test_print():
    assert analisar("print(1);") == Programa([Print(Num(1))])


def test_if_sem_else():
    assert analisar("if (x > 0) { print(x); }") == Programa(
        [If(BinOp(">", Var("x"), Num(0)), Bloco([Print(Var("x"))]))]
    )


def test_if_com_else():
    assert analisar("if (true) { x = 1; } else { x = 2; }") == Programa(
        [
            If(
                Bool(True),
                Bloco([Atribuicao("x", Num(1))]),
                Bloco([Atribuicao("x", Num(2))]),
            )
        ]
    )


def test_while():
    assert analisar("while (x > 0) { x = x - 1; }") == Programa(
        [
            While(
                BinOp(">", Var("x"), Num(0)),
                Bloco([Atribuicao("x", BinOp("-", Var("x"), Num(1)))]),
            )
        ]
    )


def test_for():
    assert analisar("for (i = 0; i < 3; i = i + 1) { print(i); }") == Programa(
        [
            For(
                Atribuicao("i", Num(0)),
                BinOp("<", Var("i"), Num(3)),
                Atribuicao("i", BinOp("+", Var("i"), Num(1))),
                Bloco([Print(Var("i"))]),
            )
        ]
    )


def test_for_com_corpo_vazio():
    no = analisar("for (i = 0; i < 3; i = i + 1) { }").comandos[0]
    assert no.corpo == Bloco([])


def test_lacos_aninhados():
    no = analisar("while (a < 2) { for (i = 0; i < 2; i = i + 1) { print(i); } }").comandos[0]
    assert isinstance(no, While)
    assert isinstance(no.corpo.comandos[0], For)


def test_parser_guarda_linha_e_coluna():
    programa = analisar("x = 1;\nprint(y);")
    var_y = programa.comandos[1].expressao
    assert (var_y.nome, var_y.linha, var_y.coluna) == ("y", 2, 7)


def test_bloco_solto_como_comando():
    assert analisar("{ x = 1; }") == Programa([Bloco([Atribuicao("x", Num(1))])])


def test_comentarios_sao_ignorados():
    assert analisar("// nota\nx = 1; /* bloco */") == Programa([Atribuicao("x", Num(1))])


# --- Arquivos de exemplo ---------------------------------------------------------


def test_programa_valido_ml():
    codigo = (RAIZ / "exemplos" / "programa_valido.ml").read_text(encoding="utf-8")
    programa = analisar(codigo)
    tipos = [type(c).__name__ for c in programa.comandos]
    assert tipos == ["Atribuicao", "Atribuicao", "Print", "While", "Atribuicao", "For", "If"]


def test_exemplo_1_da_gramatica():
    codigo = """
    // soma decrescente e contagem
    x = 10;
    soma = 0;
    while (x > 0) {
        soma = soma + x;
        x = x - 1;
    }
    for (i = 0; i < 3; i = i + 1) {
        print(i);
    }
    if (soma > 20) { print(soma); } else { print(0); }
    """
    tipos = [type(c).__name__ for c in analisar(codigo).comandos]
    assert tipos == ["Atribuicao", "Atribuicao", "While", "For", "If"]
