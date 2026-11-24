"""Testes válidos do interpretador.

Resultado esperado: todos passam sem lançar ErroSemantico.
"""

from src.interpreter import (
    TIPO_BOOL,
    TIPO_INT,
    TabelaSimbolos,
    dividir,
    formatar_valor,
    tipo_de,
)


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
