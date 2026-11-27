# Seções do relatório — Análise semântica e catálogo de erros (Davi)

> Texto-base das seções dos itens (e) e (f) para colar no `docs/relatorio.pdf`.
> Todas as mensagens do catálogo foram conferidas em 26/11, executando cada exemplo
> pelo compilador completo (`tokenizar` → `parse` → `executar`) na `main` com o parser
> integrado.

---

## 1. Tabela de símbolos

**Estrutura.** A tabela de símbolos (`TabelaSimbolos` em `src/interpreter.py`) é um
dicionário Python `nome → Simbolo`, em que cada `Simbolo` guarda o nome, o tipo
(`int` ou `bool`) e o valor atual da variável. Inserção e busca custam O(1) em média.

**Operações.**

| Operação | Quando é usada | Comportamento |
|---|---|---|
| `definir(nome, valor)` | Atribuição `x = e;` (inclusive na inicialização e na atualização do `for`) | Insere a variável ou substitui o valor **e o tipo** de uma existente |
| `buscar(nome, linha, coluna)` | Uso de `x` dentro de uma expressão | Devolve o símbolo; se não existir, lança `ErroSemantico` (restrição **S1**) |

**Escopo único.** A MiniLang não tem funções nem declarações locais, então um único
escopo global basta: uma variável criada dentro de um bloco `{ }` (por exemplo, no corpo
de um `while`) continua visível depois dele. A variável de controle do `for` também
continua existindo depois do laço, com o primeiro valor que tornou a condição falsa.

**Tipagem dinâmica.** Não há declaração de tipo; o tipo de uma variável é o do último
valor atribuído (`x = 1; x = true;` é válido). Por isso a verificação de tipos é feita
**durante a execução**, no momento em que cada operação é avaliada.

**Detalhe de implementação.** Em Python, `bool` é subclasse de `int`
(`isinstance(True, int)` é verdadeiro, e `1 == True` também). A função `tipo_de` testa o
tipo exato (`type(v) is bool`) antes de `int`; sem isso, `1 + true` passaria como soma de
inteiros e `1 == true` daria verdadeiro, violando S2 e S5.

## 2. Semântica operacional

O interpretador (`Interpretador` em `src/interpreter.py`) percorre a AST recursivamente.
Expressões são **avaliadas** e devolvem um valor; comandos são **executados** e alteram o
estado σ (a tabela de símbolos) e a saída. Em notação de semântica natural (*big-step*),
`⟨e, σ⟩ ⇓ v` significa "a expressão e, no estado σ, avalia para o valor v" e
`⟨c, σ⟩ ⇓ σ'` significa "o comando c leva o estado σ ao estado σ'".

**Expressões**

| Nó | Regra | Restrição |
|---|---|---|
| `Num(n)` | ⟨n, σ⟩ ⇓ n | — |
| `Bool(b)` | ⟨b, σ⟩ ⇓ b | — |
| `Var(x)` | ⟨x, σ⟩ ⇓ σ(x), se x ∈ dom(σ) | S1: senão, erro |
| `BinOp(op, e1, e2)`, op ∈ {+, −, *} | se ⟨e1, σ⟩ ⇓ n1 e ⟨e2, σ⟩ ⇓ n2, com n1, n2 inteiros, então ⇓ n1 op n2 | S2 |
| `BinOp(/, e1, e2)` | ⇓ trunc(n1 / n2), se n2 ≠ 0 (trunca em direção a zero: −7 / 2 = −3) | S2, S3 |
| `BinOp(op, e1, e2)`, op ∈ {<, >, <=, >=} | ⇓ verdadeiro se n1 op n2, senão falso (n1, n2 inteiros) | S5 |
| `BinOp(op, e1, e2)`, op ∈ {==, !=} | ⇓ v1 op v2, se v1 e v2 têm o mesmo tipo | S5 |

Os dois operandos são sempre avaliados, da esquerda para a direita, antes da operação.

**Comandos**

| Nó | Regra |
|---|---|
| `Atribuicao(x, e)` | se ⟨e, σ⟩ ⇓ v, então ⟨x = e, σ⟩ ⇓ σ[x ↦ v] |
| `Print(e)` | se ⟨e, σ⟩ ⇓ v, escreve v (booleanos como `true`/`false`) e o estado não muda |
| `Bloco(c1 … cn)`, `Programa` | executa c1, …, cn em sequência, passando o estado adiante |
| `If(e, b1, b2)` | se ⟨e, σ⟩ ⇓ verdadeiro, executa b1; se ⇓ falso, executa b2 (ou nada, sem `else`) — S4: e deve ser booleana |
| `While(e, b)` | se ⟨e, σ⟩ ⇓ falso, ⇓ σ; se ⇓ verdadeiro, ⟨b, σ⟩ ⇓ σ' e então ⟨while (e) b, σ'⟩ ⇓ σ'' — S4 |
| `For(i, e, a, b)` | equivale a `i; while (e) { b; a; }`: a inicialização roda uma vez, a condição é testada antes de cada volta e a atualização roda depois do corpo — S4 |

**Laço infinito.** A regra do `while` é recursiva e pode não terminar (por exemplo,
`while (true) { }`). Como não é possível decidir em geral se um laço termina (problema
da parada), o interpretador impõe um **limite de iterações** por laço
(`LIMITE_ITERACOES = 100 000`). Ao passar do limite, a execução é interrompida com erro.
O limite é configurável, e um laço que dá exatamente o número limite de voltas termina
normalmente.

## 3. Justificativa

- **Interpretação direta da AST.** A AST já tem a precedência e a associatividade
  na própria forma (em `1 + 2 * 3`, o `*` fica abaixo do `+`), então avaliar os filhos
  antes do pai produz o resultado correto sem nenhuma regra extra. Não é preciso gerar
  código intermediário para uma linguagem deste tamanho.
- **Verificação de tipos na execução.** Com tipagem dinâmica, o tipo de `x` em
  `x + 1` só é conhecido quando a linha executa (`x` pode ter sido reatribuída a um
  booleano num ramo do `if`). As restrições S1 a S5 dependem dos valores e não são
  expressáveis por uma gramática livre de contexto, por isso ficam fora da EBNF e são
  verificadas pelo interpretador.
- **`for` como açúcar sintático de `while`.** Executar o `for` como
  `inicializacao; while (condicao) { corpo; atualizacao; }` reaproveita a mesma
  semântica e deixa claro o efeito de alterar a variável de controle dentro do corpo
  (testado em `tests/validos/test_lacos.py`).
- **Testes sem depender do parser.** Os testes do interpretador montam a AST à mão,
  na forma que o parser gera. Assim, um erro no parser não mascara um erro no
  interpretador, e as duas fases puderam ser desenvolvidas em paralelo.

---

## 4. Catálogo de erros

Todas as fases usam o mesmo formato:

```
Erro <fase> na linha L, coluna C: <mensagem>
```

Linha e coluna começam em 1. No erro léxico, a posição é a do primeiro caractere do
lexema problemático; no sintático, a do token inesperado; no semântico, a do nó da AST
que causou o erro (para operações, o token do operador).

### 4.1 Erros léxicos (`src/lexer.py`, exceção `LexerError`)

| # | Exemplo | Mensagem | Causa |
|---|---|---|---|
| L1 | `x = @;` | `Erro léxico na linha 1, coluna 5: caractere inválido '@'` | Caractere fora do alfabeto Σ (o AFD vai de q0 para q_err) |
| L2 | `y = 3 # 2;` | `Erro léxico na linha 1, coluna 7: caractere inválido '#'` | Idem; vale para `# $ % & ? " ' ^ ~ \| [ ]` |
| L3 | `valor = 1x + 2;` | `Erro léxico na linha 1, coluna 9: número seguido de letra: '1x'` | Em q_num chega uma letra; `1x` não é NUM nem ID |
| L4 | `a = b ! c;` | `Erro léxico na linha 1, coluna 7: '!' isolado (esperado '!=')` | Em q_bang só `=` tem transição |
| L5 | `x = 1;` ↵ `/* sem fim` | `Erro léxico na linha 2, coluna 1: comentário de bloco não fechado` | EOF em q_bc ou q_bcs; a posição é a do `/*` de abertura |

### 4.2 Erros sintáticos (`src/parser.py`, exceção `ParserError`)

| # | Exemplo | Mensagem | Causa |
|---|---|---|---|
| P1 | `for (i = 0; i < 10) { ... }` (`programa_invalido.ml`) | `Erro sintático na linha 7, coluna 19: esperado ';', encontrado ')'` | Falta a cláusula de atualização: a produção `para` exige `atribuicao ";" expressao ";" atribuicao` |
| P2 | `x = (1 + ;` | `Erro sintático na linha 1, coluna 10: esperado número, 'true', 'false', identificador ou '(', encontrado ';'` | Depois de `+` a produção `soma` exige um `termo`; `;` não está em FIRST(fator) |
| P3 | `x = a < b < c;` | `Erro sintático na linha 1, coluna 11: esperado ';', encontrado '<'` | Comparação não associativa: `comparacao = soma [ op_comp soma ]` aceita no máximo um operador |
| P4 | `x = -1;` | `Erro sintático na linha 1, coluna 5: esperado número, 'true', 'false', identificador ou '(', encontrado '-'` | Não há menos unário; `-` não está em FIRST(fator) |
| P5 | `if (x > 0) print(x);` | `Erro sintático na linha 1, coluna 12: esperado '{', encontrado 'print'` | O corpo de `if`/`while`/`for` é sempre um bloco |

### 4.3 Erros semânticos (`src/interpreter.py`, exceção `ErroSemantico`)

| # | Exemplo | Mensagem | Causa |
|---|---|---|---|
| S1 | `print(z);` (sem `z` definida) | `Erro semântico na linha 1, coluna 7: variável 'z' não definida` | Uso antes de qualquer atribuição (S1) |
| S1′ | `for (i = 0; j < 10; i = i + 1) { }` | `Erro semântico na linha 1, coluna 13: variável 'j' não definida` | Variável de controle da condição nunca atribuída (S1, em laço) |
| S2 | `y = 1 + true;` | `Erro semântico na linha 1, coluna 7: operador '+' exige operandos inteiros, mas recebeu int e bool` | Aritmética com booleano (S2) |
| S3 | `x = 5 / 0;` | `Erro semântico na linha 1, coluna 7: divisão por zero` | Divisor avaliado como 0 (S3) |
| S4 | `while (1 + 2) { ... }` | `Erro semântico na linha 1, coluna 10: a condição do while deve ser booleana, mas é int` | Condição inteira em `if`/`while`/`for` (S4) |
| S5 | `if (1 == true) { }` | `Erro semântico na linha 1, coluna 7: operador '==' exige operandos do mesmo tipo, mas recebeu int e bool` | `==`/`!=` entre tipos diferentes; `< > <= >=` com booleano (S5) |
| S6 | `while (true) { }` | `Erro semântico na linha 1, coluna 1: o while excedeu o limite de 100000 iterações (provável laço infinito)` | O laço passou do limite de iterações |

Cada caso tem teste automatizado: `tests/invalidos/test_lexer_invalido.py`,
`test_parser_invalido.py`, `test_interpreter_invalido.py` e `test_laco_infinito.py`.
O comentário no topo de cada arquivo lista o resultado esperado.

## 5. Estratégia de diagnóstico e recuperação

**Estratégia adotada: parar no primeiro erro, com posição exata.** Cada fase lança
uma exceção no primeiro erro encontrado, e a execução termina com a mensagem acima.
Não há recuperação (por exemplo, modo pânico, que descartaria tokens até um `;` ou `}`
para continuar analisando).

**Justificativa.**

1. **Erros em cascata.** Depois de um erro sintático, o parser teria que adivinhar
   onde o comando terminava; um palpite errado gera erros falsos nas linhas
   seguintes, que confundem mais do que ajudam num programa curto.
2. **O interpretador não pode continuar.** Um erro semântico acontece durante a
   execução: depois de `x = 5 / 0;`, `x` não tem valor, e qualquer uso posterior daria
   um erro consequência do primeiro. O teste `test_erro_interrompe_a_execucao` confirma
   que nenhum comando roda depois do erro.
3. **Programas pequenos.** Programas MiniLang têm poucas linhas; corrigir um erro
   e rodar de novo é rápido, então listar vários erros de uma vez traz pouco ganho.
4. **Mensagem precisa compensa.** Em vez de vários diagnósticos, cada erro diz a
   fase, a linha, a coluna, o que era esperado e o que foi encontrado, o que basta para
   localizar e corrigir a causa.

**Separação por fase.** O tipo da exceção (`LexerError`, `ParserError` e
`ErroSemantico`) e o prefixo da mensagem ("Erro léxico", "Erro sintático", "Erro
semântico") mostram em que fase o erro foi detectado. Isso ilustra a diferença entre as
fases: `1x` é rejeitado pelo AFD; `for (i = 0; i < 10)` passa pelo lexer e só o parser
o rejeita; `while (1 + 2)` é sintaticamente válido e só o interpretador o rejeita, porque
depende do tipo dos valores.
