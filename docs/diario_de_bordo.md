## Semana 1 — 14/11/2026

**Responsável:** Manuel
**Etapa:** definição formal da linguagem (docs/gramatica.md)

**O que foi feito:** alfabeto e tabela de tokens, gramática EBNF com
precedência e associatividade (incluindo while e for), restrições
semânticas, tabela de transições do lexer e 5 programas de exemplo.

**Uso de IA:** Claude Sonnet 5.5, para gerar um rascunho inicial de
tokens, EBNF, tabela de transições e exemplos justificados, a partir
da especificação do enunciado.

**O que revisamos/alteramos:** Li o rascunho completo e conferi se as tabelas renderizaram corretamente no GitHub. Mantive as decisões de projeto como proposta para o grupo confirmar (comentário `/* */` como extensão, comparação não associativa, sem menos unário e corpo sempre em bloco). A conferência da tabela de transições contra o código foi feita em 18/11, ao executar o lexer e os testes (ver entrada seguinte).

**Decisões em aberto:** comentário de bloco (/* */) incluído para dar
sentido ao teste "comentário não fechado"; comparação não associativa;
sem menos unário. [confirmar com o grupo/professora]

**Próximos passos:** implementar src/lexer.py a partir da tabela de
transições.

## Atualização — 20/11/2026

**Responsável:** Manuel

**Etapa:** Análise léxica e elaboração do relatório.

**O que foi feito:** Estudei o funcionamento do Lexer e sua relação com a tabela de transições do AFD. Revisei os conceitos de expressões regulares, AFN, AFD, transições ε, construção dos subconjuntos e minimização. Também preparei a seção de Análise Léxica para o relatório do grupo.

**Uso de IA:** O Claude Sonnet 5.5 foi utilizado para auxiliar na geração do código e da documentação do Lexer. O ChatGPT (GPT-6) foi utilizado para estudar os conceitos teóricos, resolver exercícios e revisar o texto do relatório.

**O que foi revisado:** Conferi as regras de reconhecimento dos tokens, o maior casamento, as palavras reservadas e o tratamento de entradas inválidas, como `1x`.

**Testes realizados:** Executei `python3 -m pytest tests/ -v`. Os 34 testes automatizados do projeto foram aprovados.

**Dificuldades encontradas:** Tive dificuldades para compreender as transições ε e a transformação de AFN em AFD. Revisei esses conceitos por meio de exemplos e exercícios.

**Próximos passos:** Conferir a versão final do relatório com o grupo e preparar a apresentação do projeto.

## Atualização — 22/11/2026

**Responsável:** Davi

**Etapa:** análise semântica (tabela de símbolos e erros) e revisão da definição formal e do lexer.

**O que foi feito:** divisão de tarefas do grupo (`docs/Tasks.md`). Implementei a tabela
de símbolos em `src/interpreter.py` (escopo único, dicionário nome → `Simbolo`, com
inserção/atualização e busca) e a exceção `ErroSemantico` com linha e coluna. A busca
de uma variável inexistente lança erro (restrição S1). A função `tipo_de` testa `bool`
antes de `int`, porque em Python `True` é instância de `int` e, na ordem inversa,
`1 + true` passaria como soma de inteiros.

**Revisão (itens a e b, autor: Manuel):** conferi os 5 exemplos da gramática (o
exemplo 1 imprime 0, 1, 2 e 55, como indicado), o `programa_valido.ml` e os testes
do lexer. Rodei o lexer nos dois `.ml` e em casos de borda (`1_a`, `x<=<`, `a!=!b`);
o comportamento bate com a tabela de transições. Não encontrei erros. Duas
observações: as mensagens de erro do lexer (`Erro léxico na linha X, coluna Y`) e do
interpretador (`Erro semântico (linha X, coluna Y)`) usam formatos diferentes, o que
será padronizado no catálogo de erros (item f); e o `programa_valido.ml` sempre cai
no `else` (a soma dá 10), então vale comentar a saída esperada para a demo. Concordo
em manter as decisões em aberto como estão (`/* */`, comparação não associativa e
sem menos unário).

**Uso de IA:** Claude (Claude Code) para organizar a divisão de tarefas e como apoio
na escrita da tabela de símbolos e dos testes do interpretador. Revisei o código
antes do commit, em especial a ordem de verificação `bool` antes de `int` em
`tipo_de`. Em 22/11, usei o Claude Opus 5.5 (Claude Code) para levantar o que estava
pendente, revisar os itens a e b, atualizar o cronograma e redigir esta entrada, que
conferi antes de registrar.

**Testes realizados:** `python -m pytest -q`: 34 testes aprovados.

**Dificuldades encontradas:** o interpretador depende das classes da AST
(`src/ast_nodes.py`), que ainda não foram entregues. Com a apresentação remarcada
para 01/12 e a meta de terminar tudo até 26/11, o cronograma ficou apertado.

**Próximos passos:** avaliar a AST sobre a tabela de símbolos (incluindo while e
for), verificação de tipos S2–S5, testes de laço (0, 1 e N iterações) e de laço
infinito com limite, e catálogo de erros com mensagens padronizadas nas três fases.

## Atualização — 22/11/2026

**Responsável:** Alexandre

**Etapa:** AST e parser (itens c e d) e fechamento das decisões em aberto da gramática.

**O que foi feito:** classes da AST em `src/ast_nodes.py`, uma por construção da EBNF
(`Programa`, `Bloco`, `Atribuicao`, `Print`, `If`, `While`, `For`, `BinOp`, `Num`, `Bool`, `Var`),
com linha e coluna em todo nó para as mensagens de erro do interpretador. `For` tem os campos
`inicializacao`, `condicao`, `atualizacao` e `corpo`, com os nomes do item (d). Testes em
`tests/validos/test_ast.py` (PR #1). Parser descendente recursivo em `src/parser.py`, com um método
por produção da EBNF, e testes válidos e inválidos (a ser enviado depois do merge da AST). Pedido de
renomear `docs/Relatorio.pdf` para `docs/relatorio.pdf`, como pede o enunciado (PR #2).

**Decisões em aberto (posição):** concordo com as três decisões propostas na gramática, e o parser
e o lexer já as implementam:

- *Comentário de bloco `/* */` como extensão:* sem ele, o teste "comentário não fechado" exigido no
  item (b) não teria sentido, porque `//` sempre termina no fim da linha. Testes:
  `test_comentario_de_bloco_e_ignorado` e `test_comentario_de_bloco_nao_fechado` (lexer) e
  `test_comentarios_sao_ignorados` (parser). Exemplo: `x = 1; /* sem fechar` dá
  "Erro léxico na linha 1, coluna 8: comentário de bloco não fechado".
- *Comparação não associativa:* a produção `comparacao = soma [ op_comp soma ]` aceita no máximo um
  operador de comparação. Como o resultado de uma comparação é booleano, `a < b < c` compararia um
  booleano com um inteiro, o que não faz sentido. No parser, `comparacao()` usa `if` (no máximo uma
  vez), enquanto `soma()` e `termo()` usam `while` (repetição). Teste: `test_comparacao_nao_associativa`.
  `x = a < b < c;` dá "Erro sintático na linha 1, coluna 11: esperado ';', encontrado '<'".
- *Sem menos unário:* não consta na especificação do enunciado; usa-se `0 - x`. O `-` não está no
  conjunto de início de `fator` (`NUM`, `true`, `false`, `ID`, `(`), então o parser o rejeita.
  Teste: `test_menos_unario_fora_do_escopo`. `x = -1;` dá "Erro sintático na linha 1, coluna 5:
  esperado número, 'true', 'false', identificador ou '(', encontrado '-'".

Falta a confirmação do Manuel, que propôs as decisões, para marcar a tarefa como concluída.

**Revisão (itens a e b, autor: Manuel):** [preencher depois de revisar: o que conferi, o que
encontrei e as observações]

**Uso de IA:** Claude Opus 5.5, via Claude Code, para gerar a AST, o parser e os testes, conferir o
trabalho contra o enunciado e redigir esta entrada. Revisei o código e o texto antes de registrar.
A IA errou em pontos que precisaram de correção: os campos do `for` não seguiam os nomes do item (d),
o README não declarava a ferramenta de IA e o teste da AST dependia do parser. Os detalhes estão em
`CONTEXTO_IA.md`.

**Testes realizados:** `python -m pytest -q` com a AST e o parser juntos: 75 testes aprovados.
Os 6 testes das três decisões passam.

**Próximos passos:** enviar o parser depois do merge da AST; escrever as seções dos itens c e d do
relatório (árvores sintáticas, justificativa formal, comparação com LL(1)/LR e diagrama da AST);
montar o PDF final.

## Atualização — 23/11/2026

**Responsável:** Manuel

**Etapa:** correções da revisão do Alexandre (itens a e b).

**O que foi feito:** Recebi a revisão do Alexandre sobre a seção de Análise léxica, a gramática, o `programa_invalido.ml` e o lexer. Corrigi o `requirements.txt` vazio (adicionei `pytest`), a leitura de arquivos com BOM no Windows (`utf-8-sig` em `src/lexer.py`), o comentário sobre o estado `q_div`, que é implementado por lookahead, a justificativa da associatividade, a ligação da justificativa formal com o código (seção 5.2), a nota sobre EOF na tabela e a `declaracao_IA.md` com os modelos usados. Commits: `b37aad9`, `5207802`, `70b0273` e `4af8332`.

**Uso de IA:** O Claude Sonnet 5.5 foi usado para aplicar as correções de código e de documentação e para explicar a passagem de AFN para AFD do token NUM. Conferi cada alteração com `git diff` antes de commitar.

**Testes realizados:** `python3 -m pytest -q`: 34 testes aprovados.

**Dificuldades encontradas:** Distinguir erro léxico de erro sintático (o `programa_invalido.ml` passa pelo lexer sem erro, e só o parser o rejeita) e entender a construção dos subconjuntos do NUM.

**Próximos passos:** Fechar as decisões em aberto com o grupo, escrever o exemplo concreto de uso de IA (2.1) e a justificativa geral (2.2) do relatório e enviar o `.docx` ao Alexandre até 25/11.
