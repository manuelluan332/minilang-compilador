"""Analisador sintático (parser) descendente recursivo da MiniLang.

Cada produção da EBNF (docs/gramatica.md, seção 3) vira um método:

    programa    = { comando } ;                       -> programa()
    comando     = atribuicao ";" | impressao ";"
                | condicional | enquanto | para | bloco ;  -> comando()
    atribuicao  = ID "=" expressao ;                  -> atribuicao()
    impressao   = "print" "(" expressao ")" ;         -> impressao()
    condicional = "if" "(" expressao ")" bloco [ "else" bloco ] ; -> condicional()
    enquanto    = "while" "(" expressao ")" bloco ;   -> enquanto()
    para        = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ; -> para()
    bloco       = "{" { comando } "}" ;               -> bloco()
    expressao   = comparacao ;                        -> expressao()
    comparacao  = soma [ op_comp soma ] ;             -> comparacao()
    soma        = termo { ( "+" | "-" ) termo } ;     -> soma()
    termo       = fator { ( "*" | "/" ) fator } ;     -> termo()
    fator       = NUM | "true" | "false" | ID | "(" expressao ")" ; -> fator()

- A repetição { ... } vira um laço while; o opcional [ ... ] vira um if.
- O laço em soma() e termo() constrói a árvore à esquerda: a - b - c = (a - b) - c.
- comparacao() aceita no máximo um operador: a < b < c é erro sintático
  (comparação não associativa).
- A escolha da alternativa de comando() olha só o token atual (1 token de lookahead),
  porque cada alternativa começa com um token distinto.

Uso:
    python -m src.parser exemplos/programa_valido.ml
"""

import sys

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
    formatar,
)
from src.lexer import LexerError, tokenizar

OPS_COMPARACAO = {"LT", "GT", "LE", "GE", "EQ", "NE"}
OPS_SOMA = {"PLUS", "MINUS"}
OPS_TERMO = {"STAR", "SLASH"}

# Como cada token aparece nas mensagens de erro.
DESCRICAO = {
    "NUM": "número",
    "ID": "identificador",
    "TRUE": "'true'",
    "FALSE": "'false'",
    "IF": "'if'",
    "ELSE": "'else'",
    "WHILE": "'while'",
    "FOR": "'for'",
    "PRINT": "'print'",
    "PLUS": "'+'",
    "MINUS": "'-'",
    "STAR": "'*'",
    "SLASH": "'/'",
    "LT": "'<'",
    "GT": "'>'",
    "LE": "'<='",
    "GE": "'>='",
    "EQ": "'=='",
    "NE": "'!='",
    "ASSIGN": "'='",
    "LPAREN": "'('",
    "RPAREN": "')'",
    "LBRACE": "'{'",
    "RBRACE": "'}'",
    "SEMI": "';'",
    "EOF": "fim do arquivo",
}


class ParserError(Exception):
    """Erro sintático, com a posição (linha e coluna) do token inesperado."""

    def __init__(self, mensagem, linha, coluna):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(f"Erro sintático na linha {linha}, coluna {coluna}: {mensagem}")


def _descrever(token):
    if token.tipo in ("NUM", "ID"):
        return f"{DESCRICAO[token.tipo]} '{token.lexema}'"
    return DESCRICAO.get(token.tipo, token.tipo)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ---- utilitários ------------------------------------------------------

    def _atual(self):
        return self.tokens[self.pos]

    def _avancar(self):
        token = self.tokens[self.pos]
        if token.tipo != "EOF":
            self.pos += 1
        return token

    def _erro(self, esperado):
        token = self._atual()
        raise ParserError(
            f"esperado {esperado}, encontrado {_descrever(token)}", token.linha, token.coluna
        )

    def _consumir(self, tipo):
        """Consome o token do tipo indicado ou lança ParserError."""
        if self._atual().tipo != tipo:
            self._erro(DESCRICAO[tipo])
        return self._avancar()

    # ---- comandos ---------------------------------------------------------

    def programa(self):
        """programa = { comando } ;  (seguido de EOF)"""
        inicio = self._atual()
        comandos = []
        while self._atual().tipo != "EOF":
            comandos.append(self.comando())
        return Programa(comandos, linha=inicio.linha, coluna=inicio.coluna)

    def comando(self):
        tipo = self._atual().tipo
        if tipo == "ID":
            no = self.atribuicao()
            self._consumir("SEMI")
            return no
        if tipo == "PRINT":
            no = self.impressao()
            self._consumir("SEMI")
            return no
        if tipo == "IF":
            return self.condicional()
        if tipo == "WHILE":
            return self.enquanto()
        if tipo == "FOR":
            return self.para()
        if tipo == "LBRACE":
            return self.bloco()
        self._erro("um comando (identificador, 'print', 'if', 'while', 'for' ou '{')")

    def atribuicao(self):
        """atribuicao = ID "=" expressao ;"""
        nome = self._consumir("ID")
        self._consumir("ASSIGN")
        expr = self.expressao()
        return Atribuicao(nome.lexema, expr, linha=nome.linha, coluna=nome.coluna)

    def impressao(self):
        """impressao = "print" "(" expressao ")" ;"""
        tok = self._consumir("PRINT")
        self._consumir("LPAREN")
        expr = self.expressao()
        self._consumir("RPAREN")
        return Print(expr, linha=tok.linha, coluna=tok.coluna)

    def condicional(self):
        """condicional = "if" "(" expressao ")" bloco [ "else" bloco ] ;"""
        tok = self._consumir("IF")
        self._consumir("LPAREN")
        cond = self.expressao()
        self._consumir("RPAREN")
        entao = self.bloco()
        senao = None
        if self._atual().tipo == "ELSE":
            self._avancar()
            senao = self.bloco()
        return If(cond, entao, senao, linha=tok.linha, coluna=tok.coluna)

    def enquanto(self):
        """enquanto = "while" "(" expressao ")" bloco ;"""
        tok = self._consumir("WHILE")
        self._consumir("LPAREN")
        cond = self.expressao()
        self._consumir("RPAREN")
        corpo = self.bloco()
        return While(cond, corpo, linha=tok.linha, coluna=tok.coluna)

    def para(self):
        """para = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ;"""
        tok = self._consumir("FOR")
        self._consumir("LPAREN")
        inicializacao = self.atribuicao()
        self._consumir("SEMI")
        cond = self.expressao()
        self._consumir("SEMI")
        atualizacao = self.atribuicao()
        self._consumir("RPAREN")
        corpo = self.bloco()
        return For(inicializacao, cond, atualizacao, corpo, linha=tok.linha, coluna=tok.coluna)

    def bloco(self):
        """bloco = "{" { comando } "}" ;"""
        tok = self._consumir("LBRACE")
        comandos = []
        while self._atual().tipo not in ("RBRACE", "EOF"):
            comandos.append(self.comando())
        self._consumir("RBRACE")
        return Bloco(comandos, linha=tok.linha, coluna=tok.coluna)

    # ---- expressões -------------------------------------------------------

    def expressao(self):
        """expressao = comparacao ;"""
        return self.comparacao()

    def comparacao(self):
        """comparacao = soma [ op_comp soma ] ;"""
        esq = self.soma()
        if self._atual().tipo in OPS_COMPARACAO:
            op = self._avancar()
            dir_ = self.soma()
            esq = BinOp(op.lexema, esq, dir_, linha=op.linha, coluna=op.coluna)
        return esq

    def soma(self):
        """soma = termo { ( "+" | "-" ) termo } ;"""
        esq = self.termo()
        while self._atual().tipo in OPS_SOMA:
            op = self._avancar()
            dir_ = self.termo()
            esq = BinOp(op.lexema, esq, dir_, linha=op.linha, coluna=op.coluna)
        return esq

    def termo(self):
        """termo = fator { ( "*" | "/" ) fator } ;"""
        esq = self.fator()
        while self._atual().tipo in OPS_TERMO:
            op = self._avancar()
            dir_ = self.fator()
            esq = BinOp(op.lexema, esq, dir_, linha=op.linha, coluna=op.coluna)
        return esq

    def fator(self):
        """fator = NUM | "true" | "false" | ID | "(" expressao ")" ;"""
        tok = self._atual()
        if tok.tipo == "NUM":
            self._avancar()
            return Num(int(tok.lexema), linha=tok.linha, coluna=tok.coluna)
        if tok.tipo == "TRUE":
            self._avancar()
            return Bool(True, linha=tok.linha, coluna=tok.coluna)
        if tok.tipo == "FALSE":
            self._avancar()
            return Bool(False, linha=tok.linha, coluna=tok.coluna)
        if tok.tipo == "ID":
            self._avancar()
            return Var(tok.lexema, linha=tok.linha, coluna=tok.coluna)
        if tok.tipo == "LPAREN":
            self._avancar()
            expr = self.expressao()
            self._consumir("RPAREN")
            return expr  # parênteses não geram nó na AST
        self._erro("número, 'true', 'false', identificador ou '('")


def parse(tokens):
    """Lista de tokens (de tokenizar) -> AST (Programa). Lança ParserError.

    É a entrada usada pelo interpretador (python -m src.interpreter).
    """
    return Parser(tokens).programa()


def analisar(codigo):
    """Código-fonte -> AST (Programa). Lança LexerError ou ParserError."""
    return parse(tokenizar(codigo))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("uso: python -m src.parser <arquivo.ml>")
        sys.exit(2)
    # utf-8-sig: aceita arquivos salvos com BOM (comum no Windows) e sem BOM
    with open(sys.argv[1], encoding="utf-8-sig") as arquivo:
        texto = arquivo.read()
    try:
        print(formatar(analisar(texto)))
    except (LexerError, ParserError) as erro:
        print(erro)
        sys.exit(1)
