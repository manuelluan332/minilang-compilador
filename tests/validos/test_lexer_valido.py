
"""Testes do lexer com entradas VÁLIDAS.
 
Resultado esperado: tokenizar() devolve a lista de tokens indicada e
termina sempre com um token EOF, sem lançar LexerError.
"""
 
from src.lexer import tokenizar
 
 
def tipos(codigo):
    return [t.tipo for t in tokenizar(codigo)]
 
 
def test_entrada_vazia():
    assert tipos("") == ["EOF"]
 
 
def test_numero():
    tokens = tokenizar("42")
    assert (tokens[0].tipo, tokens[0].lexema) == ("NUM", "42")
 
 
def test_identificador():
    tokens = tokenizar("soma_1")
    assert (tokens[0].tipo, tokens[0].lexema) == ("ID", "soma_1")
 
 
def test_palavras_reservadas():
    assert tipos("while for if else print true false") == [
        "WHILE", "FOR", "IF", "ELSE", "PRINT", "TRUE", "FALSE", "EOF",
    ]
 
 
def test_reservada_como_prefixo_e_identificador():
    # 'whiles' e 'iff' não são palavras reservadas
    assert tipos("whiles iff forx") == ["ID", "ID", "ID", "EOF"]
 
 
def test_todos_os_operadores_e_delimitadores():
    codigo = "+ - * / < > <= >= == != = ( ) { } ;"
    assert tipos(codigo) == [
        "PLUS", "MINUS", "STAR", "SLASH", "LT", "GT", "LE", "GE",
        "EQ", "NE", "ASSIGN", "LPAREN", "RPAREN", "LBRACE", "RBRACE",
        "SEMI", "EOF",
    ]
 
 
def test_maior_casamento_dois_caracteres():
    # '<=' é um token; '< =' são dois
    assert tipos("<=") == ["LE", "EOF"]
    assert tipos("< =") == ["LT", "ASSIGN", "EOF"]
    assert tipos("==") == ["EQ", "EOF"]
    assert tipos("= =") == ["ASSIGN", "ASSIGN", "EOF"]
 
 
def test_sem_espacos_entre_tokens():
    assert tipos("x=1+2;") == ["ID", "ASSIGN", "NUM", "PLUS", "NUM", "SEMI", "EOF"]
 
 
def test_divisao_nao_e_comentario():
    assert tipos("a/b") == ["ID", "SLASH", "ID", "EOF"]
 
 
def test_comentario_de_linha_e_ignorado():
    assert tipos("x = 1; // comentário\ny = 2;") == [
        "ID", "ASSIGN", "NUM", "SEMI", "ID", "ASSIGN", "NUM", "SEMI", "EOF",
    ]
 
 
def test_comentario_de_linha_no_fim_sem_quebra():
    assert tipos("x // sem quebra de linha no fim") == ["ID", "EOF"]
 
 
def test_comentario_de_bloco_e_ignorado():
    assert tipos("x /* a\nb */ y") == ["ID", "ID", "EOF"]
 
 
def test_comentarios_de_bloco_de_borda():
    assert tipos("/**/") == ["EOF"]
    assert tipos("/***/") == ["EOF"]
    assert tipos("/* a * b / c */") == ["EOF"]
 
 
def test_posicao_linha_e_coluna():
    tokens = tokenizar("x = 1;\n  y")
    x, _, _, _, y, _ = tokens
    assert (x.linha, x.coluna) == (1, 1)
    assert (y.linha, y.coluna) == (2, 3)
 
 
def test_laco_for_completo():
    codigo = "for (i = 0; i < 10; i = i + 1) { print(i); }"
    assert tipos(codigo) == [
        "FOR", "LPAREN", "ID", "ASSIGN", "NUM", "SEMI",
        "ID", "LT", "NUM", "SEMI",
        "ID", "ASSIGN", "ID", "PLUS", "NUM", "RPAREN",
        "LBRACE", "PRINT", "LPAREN", "ID", "RPAREN", "SEMI", "RBRACE", "EOF",
    ]
 
 
def test_bom_no_inicio_e_ignorado():
    # Arquivos salvos como "UTF-8 com BOM" (comum no Windows) começam com U+FEFF.
    tokens = tokenizar("﻿x = 1;")
    assert [t.tipo for t in tokens] == ["ID", "ASSIGN", "NUM", "SEMI", "EOF"]
    assert (tokens[0].linha, tokens[0].coluna) == (1, 1)


def test_programa_completo_sem_erro():
    codigo = """
    // soma decrescente e contagem
    x = 10;
    soma = 0;
    while (x > 0) {
        soma = soma + x;
        x = x - 1;
    }
    if (soma > 20) { print(soma); } else { print(0); }
    """
    tokens = tokenizar(codigo)
    assert tokens[-1].tipo == "EOF"
    assert "WHILE" in [t.tipo for t in tokens]
 