"""Testes da AST.

Resultado esperado: todos passam. As árvores são montadas à mão (sem o parser)
para mostrar a forma que a AST deve ter. Os testes de que o parser gera essas
mesmas árvores ficam em test_parser_valido.py.
"""

from src.ast_nodes import (
    Atribuicao,
    BinOp,
    Bloco,
    Bool,
    For,
    If,
    Num,
    Print,
    Var,
    While,
    formatar,
)


# 1 + 2 * 3  ->  + no topo, * abaixo à direita (precedência de * sobre +)
AST_1_MAIS_2_VEZES_3 = BinOp("+", Num(1), BinOp("*", Num(2), Num(3)))

# for (i = 0; i < 3; i = i + 1) { print(i); }
AST_FOR = For(
    inicializacao=Atribuicao("i", Num(0)),
    condicao=BinOp("<", Var("i"), Num(3)),
    atualizacao=Atribuicao("i", BinOp("+", Var("i"), Num(1))),
    corpo=Bloco([Print(Var("i"))]),
)


def test_ast_1_mais_2_vezes_3_estrutura():
    raiz = AST_1_MAIS_2_VEZES_3
    assert raiz.op == "+"
    assert raiz.esq == Num(1)
    assert isinstance(raiz.dir, BinOp)
    assert raiz.dir.op == "*"
    assert (raiz.dir.esq, raiz.dir.dir) == (Num(2), Num(3))


def test_ast_for_tem_as_tres_clausulas():
    assert isinstance(AST_FOR.inicializacao, Atribuicao)
    assert AST_FOR.inicializacao.nome == "i"
    assert isinstance(AST_FOR.condicao, BinOp)
    assert AST_FOR.condicao.op == "<"
    assert isinstance(AST_FOR.atualizacao, Atribuicao)
    assert AST_FOR.atualizacao.expressao == BinOp("+", Var("i"), Num(1))
    assert AST_FOR.corpo.comandos == [Print(Var("i"))]


def test_if_sem_else_tem_senao_none():
    no = If(Bool(True), Bloco([]))
    assert no.senao is None


def test_while_guarda_condicao_e_corpo():
    no = While(BinOp(">", Var("x"), Num(0)), Bloco([Atribuicao("x", Num(0))]))
    assert no.condicao.op == ">"
    assert len(no.corpo.comandos) == 1


def test_posicao_nao_afeta_igualdade():
    # linha/coluna servem às mensagens de erro, não à estrutura
    assert Num(1, linha=3, coluna=7) == Num(1)
    assert Num(1, linha=3, coluna=7).linha == 3


def test_formatar_1_mais_2_vezes_3():
    assert formatar(AST_1_MAIS_2_VEZES_3) == (
        "BinOp +\n"
        "  Num 1\n"
        "  BinOp *\n"
        "    Num 2\n"
        "    Num 3"
    )
