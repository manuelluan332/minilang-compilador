"""Testes de laço infinito com limite de iterações.

O interpretador conta as voltas de cada laço. Se um único while ou for passar
do limite (LIMITE_ITERACOES, 100 000 por padrão), a execução é interrompida.

Resultado esperado: ErroSemantico com a mensagem
  "o while excedeu o limite de N iterações (provável laço infinito)"
  "o for excedeu o limite de N iterações (provável laço infinito)"
"""

import pytest

from src.ast_nodes import Atribuicao, BinOp, Bloco, Bool, For, Num, Print, Programa, Var, While
from src.interpreter import LIMITE_ITERACOES, ErroSemantico, executar


def rodar(*comandos, limite=10):
    saida = []
    executar(Programa(list(comandos)), escrever=saida.append, limite_iteracoes=limite)
    return saida


def test_while_true_e_interrompido():
    # while (true) { x = 1; }
    with pytest.raises(ErroSemantico) as info:
        rodar(While(Bool(True), Bloco([Atribuicao("x", Num(1))])))
    assert info.value.mensagem == (
        "o while excedeu o limite de 10 iterações (provável laço infinito)"
    )


def test_while_que_esquece_o_incremento():
    # i = 0; while (i < 3) { print(i); }  -> i nunca muda
    saida = []
    with pytest.raises(ErroSemantico, match="provável laço infinito"):
        executar(
            Programa([
                Atribuicao("i", Num(0)),
                While(BinOp("<", Var("i"), Num(3)), Bloco([Print(Var("i"))])),
            ]),
            escrever=saida.append,
            limite_iteracoes=10,
        )
    # o corpo executou exatamente o limite de vezes antes do erro
    assert saida == ["0"] * 10


def test_for_com_atualizacao_que_nao_avanca():
    # for (i = 0; i < 3; i = i) { }
    with pytest.raises(ErroSemantico) as info:
        rodar(For(Atribuicao("i", Num(0)), BinOp("<", Var("i"), Num(3)),
                  Atribuicao("i", Var("i")), Bloco([])))
    assert info.value.mensagem == "o for excedeu o limite de 10 iterações (provável laço infinito)"


def test_for_com_atualizacao_no_sentido_errado():
    # for (i = 0; i < 3; i = i - 1) { }  -> i diminui e nunca chega a 3
    with pytest.raises(ErroSemantico, match="o for excedeu o limite"):
        rodar(For(Atribuicao("i", Num(0)), BinOp("<", Var("i"), Num(3)),
                  Atribuicao("i", BinOp("-", Var("i"), Num(1))), Bloco([])))


def test_erro_aponta_posicao_do_laco():
    laco = While(Bool(True), Bloco([]), linha=3, coluna=1)
    with pytest.raises(ErroSemantico) as info:
        rodar(laco)
    assert (info.value.linha, info.value.coluna) == (3, 1)


def test_laco_que_atinge_exatamente_o_limite_nao_e_erro():
    # 10 voltas com limite 10: termina normalmente
    saida = rodar(
        Atribuicao("i", Num(0)),
        While(BinOp("<", Var("i"), Num(10)),
              Bloco([Atribuicao("i", BinOp("+", Var("i"), Num(1)))])),
        Print(Var("i")),
        limite=10,
    )
    assert saida == ["10"]


def test_limite_padrao_permite_laco_grande():
    # o limite padrão não atrapalha laços legítimos longos
    assert LIMITE_ITERACOES >= 10_000
    saida = []
    executar(
        Programa([
            Atribuicao("i", Num(0)),
            While(BinOp("<", Var("i"), Num(10_000)),
                  Bloco([Atribuicao("i", BinOp("+", Var("i"), Num(1)))])),
            Print(Var("i")),
        ]),
        escrever=saida.append,
    )
    assert saida == ["10000"]
