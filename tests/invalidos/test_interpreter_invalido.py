"""Testes inválidos do interpretador (erros semânticos).

Resultado esperado: cada caso lança ErroSemantico com a mensagem indicada,
no formato "Erro semântico na linha X, coluna Y: <mensagem>".

  - buscar variável nunca definida -> "variável 'z' não definida"                    (S1)
  - print(z + 1) sem z definida    -> "variável 'z' não definida"                    (S1)
  - y = 1 + true;                  -> "operador '+' exige operandos inteiros, mas recebeu int e bool"  (S2)
  - print(true * 2);               -> "operador '*' exige operandos inteiros, ..."   (S2)
  - x = 5 / 0;                     -> "divisão por zero"                             (S3)
  - if (1) { }                     -> "a condição do if deve ser booleana, mas é int"     (S4)
  - while (1 + 2) { ... }          -> "a condição do while deve ser booleana, mas é int"  (S4)
  - for (i = 0; 5; i = 1) { }      -> "a condição do for deve ser booleana, mas é int"    (S4)
  - 1 < true  /  true < false      -> "operador '<' exige operandos inteiros, ..."   (S5)
  - 1 == true  /  1 != false       -> "operador '==' exige operandos do mesmo tipo, mas recebeu int e bool"  (S5)
"""

import pytest

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
from src.interpreter import ErroSemantico, TabelaSimbolos, dividir, executar


def erro_ao_rodar(*comandos):
    with pytest.raises(ErroSemantico) as info:
        executar(Programa(list(comandos)), escrever=lambda _: None)
    return info.value


# --- Tabela de símbolos e divisão ----------------------------------------------

def test_buscar_variavel_nao_definida():
    tabela = TabelaSimbolos()
    with pytest.raises(ErroSemantico, match="variável 'z' não definida"):
        tabela.buscar("z")


def test_erro_informa_posicao():
    tabela = TabelaSimbolos()
    with pytest.raises(ErroSemantico) as erro:
        tabela.buscar("z", linha=3, coluna=7)
    assert erro.value.linha == 3
    assert "linha 3, coluna 7" in str(erro.value)


def test_divisao_por_zero():
    with pytest.raises(ErroSemantico, match="divisão por zero") as erro:
        dividir(5, 0, linha=1, coluna=7)
    assert "linha 1, coluna 7" in str(erro.value)


# --- S1: variável não definida ---------------------------------------------------

def test_variavel_nao_definida_dentro_de_expressao():
    e = erro_ao_rodar(Print(BinOp("+", Var("z", linha=2, coluna=7), Num(1))))
    assert e.mensagem == "variável 'z' não definida"
    assert (e.linha, e.coluna) == (2, 7)


# --- S2: aritmética só com inteiros ----------------------------------------------

def test_soma_de_inteiro_com_booleano():
    e = erro_ao_rodar(Atribuicao("y", BinOp("+", Num(1), Bool(True))))
    assert e.mensagem == "operador '+' exige operandos inteiros, mas recebeu int e bool"


def test_multiplicacao_de_booleano():
    e = erro_ao_rodar(Print(BinOp("*", Bool(True), Num(2))))
    assert "operador '*' exige operandos inteiros" in e.mensagem


# --- S3: divisão por zero ----------------------------------------------------------

def test_divisao_por_zero_na_ast():
    e = erro_ao_rodar(Atribuicao("x", BinOp("/", Num(5), Num(0), linha=1, coluna=7)))
    assert str(e) == "Erro semântico na linha 1, coluna 7: divisão por zero"


# --- S4: condição booleana -----------------------------------------------------------

def test_condicao_do_if_nao_booleana():
    e = erro_ao_rodar(If(Num(1), Bloco([])))
    assert e.mensagem == "a condição do if deve ser booleana, mas é int"


def test_condicao_do_while_nao_booleana():
    # Exemplo 5 da gramática
    e = erro_ao_rodar(While(BinOp("+", Num(1), Num(2)), Bloco([Print(Num(1))])))
    assert e.mensagem == "a condição do while deve ser booleana, mas é int"


def test_condicao_do_for_nao_booleana():
    e = erro_ao_rodar(
        For(Atribuicao("i", Num(0)), Num(5), Atribuicao("i", Num(1)), Bloco([]))
    )
    assert e.mensagem == "a condição do for deve ser booleana, mas é int"


# --- S5: comparações -------------------------------------------------------------------

def test_comparacao_de_ordem_com_booleano():
    for esq, dir in [(Num(1), Bool(True)), (Bool(True), Bool(False))]:
        e = erro_ao_rodar(Print(BinOp("<", esq, dir)))
        assert "operador '<' exige operandos inteiros" in e.mensagem


def test_igualdade_entre_tipos_diferentes():
    # Em Python, 1 == True é True; na MiniLang é erro (S5)
    for op, dir in [("==", Bool(True)), ("!=", Bool(False))]:
        e = erro_ao_rodar(Print(BinOp(op, Num(1), dir)))
        assert e.mensagem == (
            f"operador '{op}' exige operandos do mesmo tipo, mas recebeu int e bool"
        )


# --- Diagnóstico -------------------------------------------------------------------------

def test_erro_aponta_posicao_do_no():
    e = erro_ao_rodar(If(Num(1, linha=4, coluna=5), Bloco([])))
    assert str(e) == (
        "Erro semântico na linha 4, coluna 5: a condição do if deve ser booleana, mas é int"
    )


def test_erro_interrompe_a_execucao():
    # o print depois do erro não chega a executar
    saida = []
    with pytest.raises(ErroSemantico):
        executar(
            Programa([Print(Num(1)), Print(Var("z")), Print(Num(2))]),
            escrever=saida.append,
        )
    assert saida == ["1"]
