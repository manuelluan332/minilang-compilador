## Semana 1 — 14/11/2026

**Responsável:** Manuel
**Etapa:** definição formal da linguagem (docs/gramatica.md)

**O que foi feito:** alfabeto e tabela de tokens, gramática EBNF com
precedência e associatividade (incluindo while e for), restrições
semânticas, tabela de transições do lexer e 5 programas de exemplo.

**Uso de IA:** Claude Sonnet 5.5, para gerar um rascunho inicial de
tokens, EBNF, tabela de transições e exemplos justificados, a partir
da especificação do enunciado.

**O que revisamos/alteramos:** [preencher: o que você conferiu, mudou
ou descartou e por quê]

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
