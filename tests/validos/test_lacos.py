"""Testes de laço (while e for).

Resultado esperado: todos passam sem erro. Cada laço é testado executando
0, 1 e N vezes, e o for também com o corpo alterando a variável de controle.
As árvores são montadas à mão, na forma que o parser gera.
"""

from src.ast_nodes import Atribuicao, BinOp, Bloco, For, Num, Print, Programa, Var, While
from src.interpreter import executar


def rodar(*comandos):
    saida = []
    tabela = executar(Programa(list(comandos)), escrever=saida.append)
    return saida, tabela


def incremento(nome, passo=1):
    """nome = nome + passo"""
    return Atribuicao(nome, BinOp("+", Var(nome), Num(passo)))


def contagem_while(n):
    """i = 0; while (i < n) { print(i); i = i + 1; }"""
    return [
        Atribuicao("i", Num(0)),
        While(BinOp("<", Var("i"), Num(n)), Bloco([Print(Var("i")), incremento("i")])),
    ]


def contagem_for(n, corpo_extra=()):
    """for (i = 0; i < n; i = i + 1) { print(i); <corpo_extra> }"""
    return For(
        Atribuicao("i", Num(0)),
        BinOp("<", Var("i"), Num(n)),
        incremento("i"),
        Bloco([Print(Var("i")), *corpo_extra]),
    )


# --- while ---------------------------------------------------------------------

def test_while_executa_zero_vezes():
    # a condição já começa falsa: o corpo não executa
    saida, tabela = rodar(*contagem_while(0))
    assert saida == []
    assert tabela.buscar("i").valor == 0


def test_while_executa_uma_vez():
    saida, tabela = rodar(*contagem_while(1))
    assert saida == ["0"]
    assert tabela.buscar("i").valor == 1


def test_while_executa_n_vezes():
    saida, tabela = rodar(*contagem_while(5))
    assert saida == ["0", "1", "2", "3", "4"]
    assert tabela.buscar("i").valor == 5


def test_while_acumula_soma():
    # Exemplo 1 da gramática: soma de 10 até 1 = 55
    saida, _ = rodar(
        Atribuicao("x", Num(10)),
        Atribuicao("soma", Num(0)),
        While(
            BinOp(">", Var("x"), Num(0)),
            Bloco([
                Atribuicao("soma", BinOp("+", Var("soma"), Var("x"))),
                Atribuicao("x", BinOp("-", Var("x"), Num(1))),
            ]),
        ),
        Print(Var("soma")),
    )
    assert saida == ["55"]


# --- for -----------------------------------------------------------------------

def test_for_executa_zero_vezes():
    # a inicialização roda mesmo assim; o corpo e a atualização, não
    saida, tabela = rodar(contagem_for(0))
    assert saida == []
    assert tabela.buscar("i").valor == 0


def test_for_executa_uma_vez():
    saida, tabela = rodar(contagem_for(1))
    assert saida == ["0"]
    assert tabela.buscar("i").valor == 1


def test_for_executa_n_vezes():
    saida, tabela = rodar(contagem_for(5))
    assert saida == ["0", "1", "2", "3", "4"]
    # depois do laço, i vale o primeiro valor que torna a condição falsa
    assert tabela.buscar("i").valor == 5


def test_for_com_corpo_alterando_a_variavel_de_controle():
    # for (i = 0; i < 10; i = i + 1) { print(i); i = i + 2; }
    # cada volta soma 2 no corpo e 1 na atualização: i = 0, 3, 6, 9
    saida, tabela = rodar(contagem_for(10, corpo_extra=[incremento("i", 2)]))
    assert saida == ["0", "3", "6", "9"]
    assert tabela.buscar("i").valor == 12


def test_for_com_corpo_que_encerra_o_laco():
    # o corpo põe i no limite: só uma volta
    saida, _ = rodar(contagem_for(10, corpo_extra=[Atribuicao("i", Num(10))]))
    assert saida == ["0"]


def test_for_ordem_inicializacao_condicao_corpo_atualizacao():
    # for (i = 0; i < 2; i = i + 1) { print(i); }  seguido de print(i)
    # o corpo vê i antes da atualização; ao sair, i = 2
    saida, _ = rodar(contagem_for(2), Print(Var("i")))
    assert saida == ["0", "1", "2"]


def test_lacos_aninhados():
    # for (i = 0; i < 3; i = i + 1) { for (j = 0; j < 2; j = j + 1) { total = total + 1; } }
    interno = For(
        Atribuicao("j", Num(0)),
        BinOp("<", Var("j"), Num(2)),
        incremento("j"),
        Bloco([incremento("total")]),
    )
    externo = For(
        Atribuicao("i", Num(0)), BinOp("<", Var("i"), Num(3)), incremento("i"), Bloco([interno])
    )
    saida, _ = rodar(Atribuicao("total", Num(0)), externo, Print(Var("total")))
    assert saida == ["6"]
