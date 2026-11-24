# MiniLang — Definição formal da linguagem

> Documento de referência das fases léxica e sintática. Todas as decisões abaixo
> devem ser compreendidas e defendidas por todos os integrantes.

## 1. Visão geral

MiniLang é uma linguagem imperativa didática com dois tipos de valor (**inteiro** e
**booleano**), variáveis criadas por atribuição, `print`, aritmética, comparações,
`if/else`, `while` e `for`. Um programa é uma sequência de comandos.

Decisões de projeto (a confirmar pelo grupo):

| Decisão | Escolha | Motivo |
|---|---|---|
| Tipagem | Dinâmica: o tipo da variável é o do último valor atribuído | Não há declaração de tipos na especificação |
| Corpo de `if`/`else`/`while`/`for` | Sempre um bloco `{ ... }` | Elimina a ambiguidade do *dangling else* |
| Comparação | Não associativa (`a < b < c` é erro sintático) | O resultado é booleano; encadear comparações não faz sentido |
| Atribuição | É comando, não expressão (`a = b = 1` é inválido) | Simplifica a gramática e o `for` |
| Menos unário | Fora do escopo (usar `0 - x`) | Não consta na especificação |
| Comentário de bloco `/* ... */` | Incluído como extensão | Torna significativo o teste "comentário não fechado" exigido no item (b), já que `//` termina sempre no fim da linha |
| Operadores lógicos (`&&`, `\|\|`, `!`) | Fora do escopo | Não constam na especificação |
| Divisão inteira | Trunca em direção a zero: `7 / 2 = 3`, `(0 - 7) / 2 = -3` | Comportamento de C e Java; o `//` do Python arredondaria para baixo (`-4`) |
| Saída de booleanos no `print` | `true` e `false`, como os literais da linguagem | O Python imprimiria `True` e `False` |

## 2. Alfabeto e tokens

**Alfabeto Σ:** letras `a-z A-Z`, dígitos `0-9`, `_`, espaço, tab, quebra de linha e os
símbolos `+ - * / < > = ! ( ) { } ;`.
Qualquer outro caractere (por exemplo `@`, `#`, `$`) fora de comentário é **erro léxico**.

### Tabela de tokens

| Tipo | Padrão (expressão regular) | Exemplo |
|---|---|---|
| `NUM` | `[0-9]+` | `42`, `0` |
| `ID` | `[a-zA-Z_][a-zA-Z0-9_]*` (exceto palavras reservadas) | `x`, `soma_1` |
| `TRUE` / `FALSE` | `true` / `false` | `true` |
| `IF` / `ELSE` | `if` / `else` | `if` |
| `WHILE` | `while` | `while` |
| `FOR` | `for` | `for` |
| `PRINT` | `print` | `print` |
| `PLUS`, `MINUS`, `STAR`, `SLASH` | `+`, `-`, `*`, `/` | `+` |
| `LT`, `GT`, `LE`, `GE` | `<`, `>`, `<=`, `>=` | `<=` |
| `EQ`, `NE` | `==`, `!=` | `==` |
| `ASSIGN` | `=` | `=` |
| `LPAREN`, `RPAREN` | `(`, `)` | `(` |
| `LBRACE`, `RBRACE` | `{`, `}` | `{` |
| `SEMI` | `;` | `;` |
| *(descartado)* espaço | `[ \t\r\n]+` | |
| *(descartado)* comentário de linha | `//[^\n]*` | `// nota` |
| *(descartado)* comentário de bloco | `/\*([^*]\|\*+[^*/])*\*+/` | `/* nota */` |

Regras do lexer:

- **Maior casamento (maximal munch):** `<=` é um token, não `<` seguido de `=`.
- **Palavras reservadas:** o autômato reconhece `ID` e depois consulta uma tabela de
  reservadas; se o lexema estiver nela, o token passa a ser a palavra reservada.
- **Número colado em letra** (`1x`) é erro léxico, e não `NUM` seguido de `ID`.
- `!` isolado (sem `=`) é erro léxico.

## 3. Gramática (EBNF)

```ebnf
programa    = { comando } ;

comando     = atribuicao ";"
            | impressao ";"
            | condicional
            | enquanto
            | para
            | bloco ;

atribuicao  = ID "=" expressao ;
impressao   = "print" "(" expressao ")" ;
condicional = "if" "(" expressao ")" bloco [ "else" bloco ] ;
enquanto    = "while" "(" expressao ")" bloco ;
para        = "for" "(" atribuicao ";" expressao ";" atribuicao ")" bloco ;
bloco       = "{" { comando } "}" ;

expressao   = comparacao ;
comparacao  = soma [ op_comp soma ] ;
soma        = termo { ( "+" | "-" ) termo } ;
termo       = fator { ( "*" | "/" ) fator } ;
fator       = NUM | "true" | "false" | ID | "(" expressao ")" ;

op_comp     = "<" | ">" | "<=" | ">=" | "==" | "!=" ;
```

Observações:

- As três cláusulas do `for` são **obrigatórias**: não existe `para` com cláusula vazia.
- A inicialização e a atualização do `for` são `atribuicao` **sem** `;` próprio; os `;`
  dentro dos parênteses são separadores.
- A gramática não tem recursão à esquerda (as repetições usam `{ }`) e cada alternativa
  de `comando` começa com um token distinto (`ID`, `print`, `if`, `while`, `for`, `{`),
  o que a torna adequada a um **parser descendente recursivo preditivo** com 1 token de
  lookahead.
- **Consequência do corpo sempre em bloco:** `else if` não é aceito, pois o `else` exige
  `{`; escreve-se `else { if (...) { ... } }`.
- **Comparações não associam:** `a < b == c` é erro sintático, porque as seis
  comparações estão no mesmo nível; escreve-se `(a < b) == c`.

### Precedência e associatividade

| Nível | Operadores | Associatividade | Produção |
|---|---|---|---|
| 1 (maior) | `( )` | — | `fator` |
| 2 | `*` `/` | esquerda | `termo` |
| 3 | `+` `-` | esquerda | `soma` |
| 4 (menor) | `<` `>` `<=` `>=` `==` `!=` | não associativa | `comparacao` |

A precedência vem da **estrutura em níveis** da gramática: quem fica mais fundo
(`fator`) liga mais forte. A associatividade à esquerda é definida pela tabela acima
e implementada pelo parser: dentro do laço `{ ... }` ele acumula a árvore pela
esquerda, agrupando `a - b - c` como `(a - b) - c`. Isso equivale à regra recursiva
à esquerda `soma = soma ( "+" | "-" ) termo | termo`, reescrita como repetição
porque um parser descendente não aceita recursão à esquerda.

## 4. Restrições semânticas (fora da EBNF)

| Cód. | Restrição |
|---|---|
| S1 | Uma variável só pode ser usada depois de receber valor |
| S2 | Operandos de `+ - * /` devem ser inteiros |
| S3 | Divisão por zero é erro; a divisão é inteira e trunca em direção a zero |
| S4 | A condição de `if`, `while` e `for` deve ser booleana |
| S5 | `< > <= >=` exigem inteiros; `==` e `!=` exigem operandos do mesmo tipo |

## 5. Lexer

### 5.1 Autômato finito determinístico

Classes de entrada: **D** = dígito; **L** = letra ou `_`; **sym** = `+ - ( ) { } ;`;
**WS** = espaço, tab, `\r`, `\n`; **outro** = qualquer caractere fora do alfabeto.
`↩X` significa "aceita o token X sem consumir o caractere lido" (maximal munch).
`q_sym` agrupa os estados finais dos símbolos simples (o token é decidido pelo caractere lido).

| Estado | D | L | `<` | `>` | `=` | `!` | `/` | `*` | sym | WS | outro |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **q0** (inicial) | q_num | q_id | q_lt | q_gt | q_eq | q_bang | q_div | q_sym | q_sym | q0 | q_err |
| q_num | q_num | **q_err** (`1x`) | ↩NUM | ↩NUM | ↩NUM | ↩NUM | ↩NUM | ↩NUM | ↩NUM | ↩NUM | ↩NUM |
| q_id | q_id | q_id | ↩ID | ↩ID | ↩ID | ↩ID | ↩ID | ↩ID | ↩ID | ↩ID | ↩ID |
| q_lt | ↩LT | ↩LT | ↩LT | ↩LT | q_le | ↩LT | ↩LT | ↩LT | ↩LT | ↩LT | ↩LT |
| q_gt | ↩GT | ↩GT | ↩GT | ↩GT | q_ge | ↩GT | ↩GT | ↩GT | ↩GT | ↩GT | ↩GT |
| q_eq | ↩ASSIGN | ↩ASSIGN | ↩ASSIGN | ↩ASSIGN | q_eqeq | ↩ASSIGN | ↩ASSIGN | ↩ASSIGN | ↩ASSIGN | ↩ASSIGN | ↩ASSIGN |
| q_bang | q_err | q_err | q_err | q_err | q_ne | q_err | q_err | q_err | q_err | q_err | q_err |
| q_div | ↩SLASH | ↩SLASH | ↩SLASH | ↩SLASH | ↩SLASH | ↩SLASH | q_lc | q_bc | ↩SLASH | ↩SLASH | ↩SLASH |

Estados finais sem transições de saída: **q_le** (`<=`), **q_ge** (`>=`), **q_eqeq** (`==`),
**q_ne** (`!=`), **q_sym**. **q_err** é o estado de erro léxico.

No fim da entrada (EOF), `q0` devolve o token `EOF`; `q_num` e `q_id` aceitam o token
em andamento; `!` ou comentário de bloco abertos no fim levam a `q_err`.

Estados dos comentários (colunas próprias, pois a classe WS se divide):

| Estado | `\n` | `*` | `/` | EOF | outro |
|---|---|---|---|---|---|
| q_lc (dentro de `//`) | fim: descarta | q_lc | q_lc | fim: descarta | q_lc |
| q_bc (dentro de `/*`) | q_bc | q_bcs | q_bc | **q_err** (não fechado) | q_bc |
| q_bcs (viu `*` em `/*`) | q_bc | q_bcs | fim: descarta | **q_err** (não fechado) | q_bc |

### 5.2 Justificativa formal

1. Cada categoria de token tem padrão **regular** (tabela da seção 2).
2. Pelo teorema de Kleene, toda expressão regular tem um AFN equivalente (construção de
   Thompson), e todo AFN tem um AFD equivalente (construção de subconjuntos).
3. A união dos padrões, com a regra do maior casamento e a tabela de reservadas
   aplicada a `ID`, dá o autômato da seção 5.1.
4. **Ligação com o código** (`src/lexer.py`): cada estado da tabela corresponde a um
   bloco de `proximo()`, marcado por comentário (`# q_num`, `# q_id`, `# q_lt, q_gt, q_eq`,
   `# q_bang`, `# q_sym`, `# q_err`). Há duas exceções: `q_div` não tem bloco próprio, pois a
   decisão é tomada olhando o caractere seguinte (`_seguinte()`) sem consumi-lo, e, se a `/`
   não abre comentário, ela cai em `q_sym` e vira `SLASH`; e os estados `q_lc`, `q_bc` e
   `q_bcs` ficam em `_pular_comentario()`.
5. Logo, o lexer reconhece exatamente os lexemas de L(token) para cada token da
   linguagem; qualquer entrada que leve a `q_err` não pertence à linguagem léxica.

A justificativa completa, com o AFN/AFD do token `NUM`, está na seção "Análise léxica"
do `docs/relatorio.pdf`.

## 6. Programas de exemplo

### Exemplo 1 — válido

```
// soma decrescente e contagem
x = 10;
soma = 0;
while (x > 0) {
    soma = soma + x;
    x = x - 1;
}
for (i = 0; i < 3; i = i + 1) {
    print(i);
}
if (soma > 20) { print(soma); } else { print(0); }
```

**Justificativa:** todos os comandos casam com as produções `atribuicao`, `enquanto`,
`para` e `condicional`; as condições são booleanas (S4), e todas as variáveis são
atribuídas antes do uso (S1). Imprime `0`, `1`, `2` e `55`.

### Exemplo 2 — inválido (léxico)

```
valor = 1x + 2;
```

**Justificativa:** no autômato, o estado `q_num` recebe uma letra (`x`) e vai para
`q_err`. Nenhum token da tabela casa com `1x`. É erro léxico, detectado antes do parser.

### Exemplo 3 — inválido (sintático, laço mal formado)

```
for (i = 0; i < 10) { print(i); }
```

**Justificativa:** a produção `para` exige `atribuicao ";" expressao ";" atribuicao`.
Depois de `i < 10` o parser espera `;` e encontra `)`: falta a cláusula de atualização.
Sintaticamente inválido, pois a entrada não pertence a L(G).

### Exemplo 4 — inválido (sintático)

```
x = (1 + ;
```

**Justificativa:** após o operador `+`, a produção `soma` exige um `termo` e, em última
instância, um `fator` (`NUM`, `true`, `false`, `ID` ou `"(" expressao ")"`). O parser
encontra `;`, que não está no conjunto de início de `fator`.

### Exemplo 5 — inválido (semântico)

```
while (1 + 2) {
    print(1);
}
```

**Justificativa:** sintaticamente correto (`1 + 2` é uma `expressao` válida), mas a
condição tem tipo inteiro, violando **S4** (condição deve ser booleana). Só o
interpretador detecta o erro, porque ele depende do tipo dos valores, algo que a
gramática livre de contexto não expressa.

> Outros erros semânticos para o catálogo do item (f): `print(z);` sem `z` definida
> (S1), `x = 5 / 0;` (S3), `y = 1 + true;` (S2).