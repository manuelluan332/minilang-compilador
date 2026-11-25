"""Testes do parser com entradas INVÁLIDAS (erros sintáticos).

Resultado esperado: analisar() lança ParserError, com a mensagem e a
posição (linha, coluna) do token inesperado indicadas em cada teste.
"""

from pathlib import Path

import pytest

from src.parser import ParserError, analisar

RAIZ = Path(__file__).resolve().parents[2]


def erro(codigo):
    with pytest.raises(ParserError) as info:
        analisar(codigo)
    return info.value


# --- Laços mal formados ----------------------------------------------------------


def test_for_sem_clausula_de_atualizacao():
    # Exemplo 3 da gramática: depois de i < 10 espera ';' e encontra ')'
    e = erro("for (i = 0; i < 10) { print(i); }")
    assert e.mensagem == "esperado ';', encontrado ')'"
    assert (e.linha, e.coluna) == (1, 19)


def test_programa_invalido_ml():
    # o próprio arquivo documenta, no topo, o erro esperado (linha 7, coluna 19)
    codigo = (RAIZ / "exemplos" / "programa_invalido.ml").read_text(encoding="utf-8")
    e = erro(codigo)
    assert e.mensagem == "esperado ';', encontrado ')'"
    assert (e.linha, e.coluna) == (7, 19)


def test_for_com_clausula_vazia():
    # as três cláusulas são obrigatórias
    e = erro("for (; i < 3; i = i + 1) { }")
    assert e.mensagem == "esperado identificador, encontrado ';'"


def test_for_sem_parenteses():
    e = erro("for i = 0; i < 3; i = i + 1 { }")
    assert e.mensagem == "esperado '(', encontrado identificador 'i'"


def test_while_sem_chaves():
    # corpo é sempre um bloco { ... }
    e = erro("while (x > 0) x = x - 1;")
    assert e.mensagem == "esperado '{', encontrado identificador 'x'"


def test_while_sem_condicao():
    e = erro("while () { }")
    assert e.mensagem == "esperado número, 'true', 'false', identificador ou '(', encontrado ')'"


def test_bloco_nao_fechado():
    e = erro("while (x > 0) { x = x - 1;")
    assert e.mensagem == "esperado '}', encontrado fim do arquivo"


# --- Expressões ------------------------------------------------------------------


def test_expressao_incompleta():
    # Exemplo 4 da gramática
    e = erro("x = (1 + ;")
    assert e.mensagem == "esperado número, 'true', 'false', identificador ou '(', encontrado ';'"
    assert (e.linha, e.coluna) == (1, 10)


def test_comparacao_nao_associativa():
    e = erro("x = a < b < c;")
    assert e.mensagem == "esperado ';', encontrado '<'"


def test_parentese_nao_fechado():
    e = erro("print((1 + 2);")
    assert e.mensagem == "esperado ')', encontrado ';'"


def test_menos_unario_fora_do_escopo():
    e = erro("x = -1;")
    assert "encontrado '-'" in e.mensagem


# --- Comandos --------------------------------------------------------------------


def test_falta_ponto_e_virgula():
    e = erro("x = 1\nprint(x);")
    assert e.mensagem == "esperado ';', encontrado 'print'"
    assert (e.linha, e.coluna) == (2, 1)


def test_atribuicao_encadeada():
    # atribuição é comando, não expressão
    e = erro("a = b = 1;")
    assert e.mensagem == "esperado ';', encontrado '='"


def test_else_sem_if():
    e = erro("else { }")
    assert e.mensagem.startswith("esperado um comando")


def test_if_sem_parenteses():
    e = erro("if x > 0 { }")
    assert e.mensagem == "esperado '(', encontrado identificador 'x'"
