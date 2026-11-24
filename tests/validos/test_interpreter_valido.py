"""Testes válidos do interpretador.

Resultado esperado: todos passam sem lançar ErroSemantico. Nos testes de
execução, as árvores são montadas à mão (sem o parser), na forma que o parser
gera; a saída do print é comparada linha a linha.
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
    Programa,
    Var,
    While,
)
from src.interpreter import (
    TIPO_BOOL,
    TIPO_INT,
    TabelaSimbolos,
    dividir,
    executar,
    formatar_valor,
    tipo_de,
)


def rodar(*comandos):
    """Executa os comandos e devolve (linhas impressas, tabela de símbolos)."""
    saida = []
    tabela = executar(Programa(list(comandos)), escrever=saida.append)
    return saida, tabela


# --- Tabela de símbolos -------------------------------------------------------

def test_definir_e_buscar_inteiro():
    tabela = TabelaSimbolos()
    tabela.definir("x", 10)
    simbolo = tabela.buscar("x")
    assert simbolo.valor == 10
    assert simbolo.tipo == TIPO_INT


def test_definir_e_buscar_booleano():
    tabela = TabelaSimbolos()
    tabela.definir("ok", True)
    assert tabela.buscar("ok").tipo == TIPO_BOOL


def test_reatribuicao_atualiza_valor():
    tabela = TabelaSimbolos()
    tabela.definir("x", 1)
    tabela.definir("x", 2)
    assert tabela.buscar("x").valor == 2
    assert len(tabela) == 1  # atualiza, não duplica


def test_reatribuicao_muda_tipo():
    # Tipagem dinâmica: o tipo é o do último valor atribuído.
    tabela = TabelaSimbolos()
    tabela.definir("x", 1)
    tabela.definir("x", False)
    assert tabela.buscar("x").tipo == TIPO_BOOL


def test_existe():
    tabela = TabelaSimbolos()
    assert not tabela.existe("x")
    tabela.definir("x", 0)
    assert tabela.existe("x")


# --- Tipos --------------------------------------------------------------------

def test_bool_nao_e_classificado_como_int():
    # Em Python, isinstance(True, int) é True; a MiniLang precisa distinguir.
    assert tipo_de(True) == TIPO_BOOL
    assert tipo_de(False) == TIPO_BOOL
    assert tipo_de(0) == TIPO_INT
    assert tipo_de(1) == TIPO_INT


# --- Divisão inteira (S3) -----------------------------------------------------

def test_divisao_inteira_positiva():
    assert dividir(7, 2) == 3
    assert dividir(6, 3) == 2


def test_divisao_trunca_em_direcao_a_zero():
    # Python: -7 // 2 == -4. MiniLang (como C e Java): -7 / 2 == -3.
    assert dividir(-7, 2) == -3
    assert dividir(7, -2) == -3
    assert dividir(-7, -2) == 3


# --- Saída do print -----------------------------------------------------------

def test_print_mostra_booleanos_como_na_linguagem():
    assert formatar_valor(True) == "true"
    assert formatar_valor(False) == "false"
    assert formatar_valor(42) == "42"
    assert formatar_valor(-3) == "-3"


# --- Execução sobre a AST -----------------------------------------------------

def test_atribuicao_e_print():
    saida, tabela = rodar(Atribuicao("x", Num(5)), Print(Var("x")))
    assert saida == ["5"]
    assert tabela.buscar("x").valor == 5


def test_precedencia_1_mais_2_vezes_3():
    # a AST de 1 + 2 * 3 tem o * abaixo do +: resultado 7, não 9
    saida, _ = rodar(Print(BinOp("+", Num(1), BinOp("*", Num(2), Num(3)))))
    assert saida == ["7"]


def test_parenteses_1_mais_2_vezes_3():
    # (1 + 2) * 3: o parêntese não vira nó, só muda a forma da árvore
    saida, _ = rodar(Print(BinOp("*", BinOp("+", Num(1), Num(2)), Num(3))))
    assert saida == ["9"]


def test_subtracao_associa_a_esquerda():
    # 10 - 3 - 2 = (10 - 3) - 2 = 5 (seria 9 se associasse à direita)
    saida, _ = rodar(Print(BinOp("-", BinOp("-", Num(10), Num(3)), Num(2))))
    assert saida == ["5"]


def test_divisao_na_ast_trunca():
    saida, _ = rodar(Print(BinOp("/", BinOp("-", Num(0), Num(7)), Num(2))))
    assert saida == ["-3"]


def test_comparacoes_devolvem_booleano():
    casos = [
        ("<", 1, 2, "true"),
        (">", 1, 2, "false"),
        ("<=", 2, 2, "true"),
        (">=", 1, 2, "false"),
        ("==", 3, 3, "true"),
        ("!=", 3, 3, "false"),
    ]
    for op, a, b, esperado in casos:
        saida, _ = rodar(Print(BinOp(op, Num(a), Num(b))))
        assert saida == [esperado], op


def test_igualdade_entre_booleanos():
    saida, _ = rodar(
        Print(BinOp("==", Bool(True), Bool(True))),
        Print(BinOp("!=", Bool(True), Bool(False))),
    )
    assert saida == ["true", "true"]


def test_if_executa_entao():
    saida, _ = rodar(If(Bool(True), Bloco([Print(Num(1))]), Bloco([Print(Num(2))])))
    assert saida == ["1"]


def test_if_executa_senao():
    saida, _ = rodar(If(Bool(False), Bloco([Print(Num(1))]), Bloco([Print(Num(2))])))
    assert saida == ["2"]


def test_if_sem_else_com_condicao_falsa_nao_faz_nada():
    saida, _ = rodar(If(Bool(False), Bloco([Print(Num(1))])))
    assert saida == []


def test_reatribuicao_muda_tipo_na_execucao():
    # tipagem dinâmica: x começa inteiro e passa a booleano
    saida, tabela = rodar(
        Atribuicao("x", Num(1)), Atribuicao("x", Bool(True)), Print(Var("x"))
    )
    assert saida == ["true"]
    assert tabela.buscar("x").tipo == TIPO_BOOL


def test_variavel_criada_no_bloco_continua_visivel():
    # escopo único: a variável criada no bloco existe depois dele
    saida, _ = rodar(Bloco([Atribuicao("y", Num(3))]), Print(Var("y")))
    assert saida == ["3"]


def test_programa_valido_ml():
    # Mesma AST que o parser deve gerar para exemplos/programa_valido.ml;
    # a saída esperada é a do comentário no topo do arquivo.
    programa = [
        Atribuicao("x", Num(10)),
        Atribuicao("y", BinOp("*", Num(2), BinOp("+", Var("x"), Num(5)))),
        Print(Var("y")),
        While(
            BinOp(">", Var("x"), Num(0)),
            Bloco([Print(Var("x")), Atribuicao("x", BinOp("-", Var("x"), Num(1)))]),
        ),
        Atribuicao("soma", Num(0)),
        For(
            Atribuicao("i", Num(0)),
            BinOp("<", Var("i"), Num(5)),
            Atribuicao("i", BinOp("+", Var("i"), Num(1))),
            Bloco([Atribuicao("soma", BinOp("+", Var("soma"), Var("i")))]),
        ),
        If(
            BinOp(">", Var("soma"), Num(5)),
            Bloco([Print(Var("soma"))]),
            Bloco([Print(Num(0))]),
        ),
    ]
    saida, _ = rodar(*programa)
    assert saida == ["30", "10", "9", "8", "7", "6", "5", "4", "3", "2", "1", "10"]
