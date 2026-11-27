# 2.1 Análise léxica

O lexer da MiniLang (`src/lexer.py`), implementado em Python, transforma o código-fonte em tokens para o parser, descarta espaços e comentários e informa linha e coluna dos erros. Além de `//`, foi proposta a extensão `/* ... */` para permitir o teste de comentário não fechado. `NUM` segue `[0-9]+`; `ID` segue `[a-zA-Z_][a-zA-Z0-9_]*`. A consulta às palavras reservadas distingue `while` (WHILE) de `whiles` (ID).

## Justificativa formal

Pelo teorema de Kleene, os padrões regulares dos tokens possuem autômatos finitos equivalentes. A união desses padrões permite construir um AFN com estados finais identificados por categoria. A construção dos subconjuntos gera um AFD equivalente; a minimização preserva o reconhecimento e a classificação dos tokens. O método `proximo()` implementa as regras da tabela de transições (`docs/gramatica.md`, seção 5.1), com maior casamento (`<=` vira LE), consulta às reservadas e tratamento de erros. O estado `q_div` usa lookahead por `_seguinte()`; os estados `q_lc`, `q_bc` e `q_bcs` são tratados em `_pular_comentario()`. Assim, os lexemas são reconhecidos conforme a especificação léxica, e entradas inválidas são rejeitadas. A tabela foi conferida contra o código na revisão do Alexandre.

## Exemplo formal: token NUM

`NUM = [0-9]+ = dd*`, com `d` representando um dígito. O AFN pela construção de Thompson (Hopcroft, Motwani e Ullman) tem `s0` como estado inicial e `s5` como final:

`s0 —d→ s1; s1 —ε→ s2; s2 —ε→ s3, s5; s3 —d→ s4; s4 —ε→ s3, s5.`

Pela construção dos subconjuntos: `A = {s0}`; `B = {s1, s2, s3, s5}`; `C = {s3, s4, s5}`. As transições com `d` são A → B, B → C e C → C. B e C são finais equivalentes e podem ser reunidos.

AFD minimizado: `q0 —d→ [q_num]`; `[q_num] —d→ [q_num]`.

As demais transições do AFD isolado levam à rejeição. A entrada `1x` segue uma regra adicional do lexer completo.

**Tabela — Trecho das transições do lexer (NUM)**

| Estado | Entrada | Resultado |
|---|---|---|
| q0 | dígito | q_num |
| q_num | dígito | q_num |
| q_num | letra / `_` | q_err |
| q_num | `;` | Aceita NUM; não consome `;` |

Fonte interna: `docs/gramatica.md`, seções 2, 5.1 e 5.2; `src/lexer.py`.

## Testes e limitações

O lexer tem 16 testes válidos e 10 inválidos, incluindo `@`, `1x` e comentário não fechado. Os testes não substituem a justificativa formal. O lexer é manual, sem flex, e não aceita identificadores acentuados.

## Uso de IA e verificação humana

O Claude Sonnet 5.5 (Anthropic) gerou o rascunho do lexer, dos testes e da documentação; o ChatGPT (GPT-6, OpenAI) apoiou o estudo dos autômatos e a revisão do relatório. Conferi a rejeição de `1x` (`q_num → q_err`) e mantive a regra. Na revisão, Alexandre identificou que `encoding="utf-8"` mantinha o BOM inicial, causando erro léxico. Com apoio do Claude, alterei para `encoding="utf-8-sig"`, que remove o BOM quando presente, e conferi a alteração com `git diff`.

Um caso que exigiu conferência humana foi o exemplo inválido gerado pela IA, com um `for` sem a cláusula de atualização: `for (i = 0; i < 10) {...}`. O lexer reconhece os tokens até EOF, mas o parser rejeita o programa na linha 3, coluna 19, com a mensagem "esperado ';', encontrado ')'". Trata-se de um erro sintático, não léxico. Em 23/11, os 34 testes então existentes passaram; em 27/11, com o trabalho do grupo integrado, a suíte do projeto passou com 125 testes, 26 deles do lexer.