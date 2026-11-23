"""Analisador léxico da MiniLang.

Implementa o autômato finito determinístico descrito em docs/gramatica.md
(seção "Lexer"). Cada trecho do código indica o estado do autômato que ele
representa (q0, q_num, q_id, q_div, q_lc, q_bc, ...).

Uso:
    python -m src.lexer exemplos/programa_valido.ml
"""

import sys
from dataclasses import dataclass

RESERVADAS = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "print": "PRINT",
    "true": "TRUE",
    "false": "FALSE",
}

SIMBOLOS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMI",
}

# caractere -> (token se vier sozinho, token se vier seguido de '=')
OPERADORES_COMPARACAO = {
    "<": ("LT", "LE"),
    ">": ("GT", "GE"),
    "=": ("ASSIGN", "EQ"),
}

ESPACOS = " \t\r\n"
DIGITOS = "0123456789"


class LexerError(Exception):
    """Erro léxico, com posição (linha e coluna começam em 1)."""

    def __init__(self, mensagem, linha, coluna):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(f"Erro léxico na linha {linha}, coluna {coluna}: {mensagem}")


@dataclass(frozen=True)
class Token:
    tipo: str
    lexema: str
    linha: int
    coluna: int


def _eh_digito(c):
    return c != "" and c in DIGITOS


def _eh_letra(c):
    return c != "" and (("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_")


def _eh_letra_ou_digito(c):
    return _eh_letra(c) or _eh_digito(c)


class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linha = 1
        self.coluna = 1

    # ---- leitura de caracteres -------------------------------------------

    def _atual(self):
        """Caractere atual, ou '' no fim da entrada (EOF)."""
        return self.codigo[self.pos] if self.pos < len(self.codigo) else ""

    def _seguinte(self):
        """Caractere após o atual (lookahead de 2), ou '' no EOF."""
        return self.codigo[self.pos + 1] if self.pos + 1 < len(self.codigo) else ""

    def _avancar(self):
        c = self.codigo[self.pos]
        self.pos += 1
        if c == "\n":
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return c

    def _consumir_enquanto(self, predicado):
        inicio = self.pos
        while predicado(self._atual()):
            self._avancar()
        return self.codigo[inicio:self.pos]

    # ---- comentários (estados q_lc, q_bc e q_bcs) ------------------------

    def _pular_comentario(self):
        linha, coluna = self.linha, self.coluna
        self._avancar()  # consome '/'
        if self._atual() == "/":
            # q_lc: comentário de linha, termina em '\n' ou EOF
            while self._atual() not in ("", "\n"):
                self._avancar()
            return
        self._avancar()  # consome '*'
        # q_bc: dentro do comentário de bloco
        while True:
            c = self._atual()
            if c == "":
                raise LexerError("comentário de bloco não fechado", linha, coluna)
            self._avancar()
            if c == "*" and self._atual() == "/":
                # q_bcs -> fim do comentário
                self._avancar()
                return

    # ---- próximo token ---------------------------------------------------

    def proximo(self):
        # q0: ignora espaços e comentários
        while True:
            c = self._atual()
            if c == "":
                return Token("EOF", "", self.linha, self.coluna)
            if c in ESPACOS:
                self._avancar()
                continue
            # q_div: '/' seguida de '/' ou '*' abre comentário (decidido por
            # lookahead, sem consumir); caso contrário cai em q_sym e vira SLASH
            if c == "/" and self._seguinte() in ("/", "*"):
                self._pular_comentario()
                continue
            break

        linha, coluna = self.linha, self.coluna

        # q_num: [0-9]+ (seguido de letra é erro: 1x)
        if _eh_digito(c):
            lexema = self._consumir_enquanto(_eh_digito)
            if _eh_letra(self._atual()):
                resto = self._consumir_enquanto(_eh_letra_ou_digito)
                raise LexerError(
                    f"número seguido de letra: '{lexema}{resto}'", linha, coluna
                )
            return Token("NUM", lexema, linha, coluna)

        # q_id: identificador ou palavra reservada
        if _eh_letra(c):
            lexema = self._consumir_enquanto(_eh_letra_ou_digito)
            return Token(RESERVADAS.get(lexema, "ID"), lexema, linha, coluna)

        # q_lt, q_gt, q_eq (e q_le, q_ge, q_eqeq): maior casamento
        if c in OPERADORES_COMPARACAO:
            self._avancar()
            simples, duplo = OPERADORES_COMPARACAO[c]
            if self._atual() == "=":
                self._avancar()
                return Token(duplo, c + "=", linha, coluna)
            return Token(simples, c, linha, coluna)

        # q_bang: '!' só é válido seguido de '='
        if c == "!":
            self._avancar()
            if self._atual() == "=":
                self._avancar()
                return Token("NE", "!=", linha, coluna)
            raise LexerError("'!' isolado (esperado '!=')", linha, coluna)

        # q_sym: símbolos de um caractere
        if c in SIMBOLOS:
            self._avancar()
            return Token(SIMBOLOS[c], c, linha, coluna)

        # q_err: caractere fora do alfabeto
        raise LexerError(f"caractere inválido '{c}'", linha, coluna)


def tokenizar(codigo):
    """Devolve a lista de tokens do código, terminada por um token EOF."""
    lexer = Lexer(codigo)
    tokens = []
    while True:
        token = lexer.proximo()
        tokens.append(token)
        if token.tipo == "EOF":
            return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("uso: python -m src.lexer <arquivo.ml>")
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8-sig") as arquivo:
        texto = arquivo.read()
    try:
        for t in tokenizar(texto):
            print(f"{t.linha}:{t.coluna}\t{t.tipo}\t{t.lexema!r}")
    except LexerError as erro:
        print(erro)
        sys.exit(1)