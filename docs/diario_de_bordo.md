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


## Atualização — 23/11/2026

**Responsável:** Manuel

**Etapa:** correções da revisão do Alexandre (itens a e b).

**O que foi feito:** Recebi a revisão do Alexandre sobre a seção de Análise léxica, a gramática, o `programa_invalido.ml` e o lexer. Corrigi o `requirements.txt` vazio (adicionei `pytest`), a leitura de arquivos com BOM no Windows (`utf-8-sig` em `src/lexer.py`), o comentário sobre o estado `q_div`, que é implementado por lookahead, a justificativa da associatividade, a ligação da justificativa formal com o código (seção 5.2), a nota sobre EOF na tabela e a `declaracao_IA.md` com os modelos usados. Commits: `b37aad9`, `5207802`, `70b0273` e `4af8332`.

**Uso de IA:** O Claude Sonnet 5.5 foi usado para aplicar as correções de código e de documentação e para explicar a passagem de AFN para AFD do token NUM. Conferi cada alteração com `git diff` antes de commitar.

**Testes realizados:** `python3 -m pytest -q`: 34 testes aprovados.

**Dificuldades encontradas:** Distinguir erro léxico de erro sintático (o `programa_invalido.ml` passa pelo lexer sem erro, e só o parser o rejeita) e entender a construção dos subconjuntos do NUM.

**Próximos passos:** Fechar as decisões em aberto com o grupo, escrever o exemplo concreto de uso de IA (2.1) e a justificativa geral (2.2) do relatório e enviar o `.docx` ao Alexandre até 25/11.