### Uso de inteligência artificial na Análise Léxica

Durante o desenvolvimento do analisador léxico da MiniLang, foi utilizada a ferramenta Claude, da Anthropic, como apoio à geração do código Python e à estruturação das regras de reconhecimento de tokens.

Também foi utilizado o ChatGPT, da OpenAI, para estudar os conceitos de expressões regulares, autômatos finitos não determinísticos (AFN), autômatos finitos determinísticos (AFD), construção dos subconjuntos e minimização.

O ChatGPT também auxiliou na revisão e organização do texto da seção de Análise Léxica do relatório.

A implementação foi submetida a testes automatizados com Pytest. Na execução realizada, os 34 testes disponíveis foram aprovados, abrangendo o Lexer e outras partes do projeto.

O uso dessas ferramentas contribuiu para o desenvolvimento e a compreensão dos conceitos estudados. Entretanto, os resultados dos testes não garantem a ausência de erros em todos os cenários possíveis.

Na definição formal da linguagem (`docs/gramatica.md`: tokens, EBNF, precedência, tabela de
transições e os 5 exemplos) e nos programas de exemplo (`exemplos/*.ml`), o Claude gerou o
rascunho inicial. O código do lexer (`src/lexer.py`) e os testes do lexer
(`tests/validos/test_lexer_valido.py` e `tests/invalidos/test_lexer_invalido.py`) também
foram gerados pelo Claude e, em seguida, executados e conferidos por mim (Manuel).


### Uso de inteligência artificial na Análise Léxica

Na definição formal da linguagem (`docs/gramatica.md`: tokens, EBNF, precedência, tabela de transições e os 5 exemplos) e nos programas de exemplo (`exemplos/*.ml`), o Claude gerou o rascunho inicial. O código do lexer (`src/lexer.py`) e os testes do lexer (`tests/validos/test_lexer_valido.py` e `tests/invalidos/test_lexer_invalido.py`) também foram gerados pelo Claude e, em seguida, executados e conferidos por mim (Manuel).

O Claude Sonnet 5.5 também foi usado para revisar e enxugar o texto da seção 2.1 do relatório e gerar o arquivo `docs/relatorio_analise_lexica.md`; o conteúdo foi conferido contra `docs/gramatica.md` e `src/lexer.py`.

O ChatGPT, da OpenAI, foi usado para estudar expressões regulares, AFN, AFD, construção dos subconjuntos e minimização, e auxiliou na revisão e organização do texto da seção de Análise Léxica do relatório.

A implementação foi submetida a testes automatizados com Pytest. Em 23/11, os 34 testes então disponíveis foram aprovados; em 27/11, com o trabalho do grupo integrado, a suíte do projeto passou com 125 testes, 26 deles do lexer. Os resultados dos testes não garantem a ausência de erros em todos os cenários possíveis.

### Uso de inteligência artificial na Análise Semântica (Davi)

**Ferramenta/modelo:** Claude, da Anthropic, via Claude Code (Claude Opus 5.5 na sessão de 22/11).

**Etapas em que foi usada:** divisão de tarefas do grupo (`docs/Tasks.md`), tabela de
símbolos e exceção `ErroSemantico` (`src/interpreter.py`), testes do interpretador,
revisão da definição formal e do lexer, atualização do cronograma e redação da
entrada no diário de bordo.

**Finalidade:** apoio na geração de código e testes, revisão do trabalho dos colegas e organização da documentação.

**O que foi aceito, reescrito ou descartado:** o código da tabela de símbolos e os
testes foram aceitos depois de revisão e da execução com Pytest (34 testes aprovados).
Da revisão dos itens a e b, aceitei as observações e deixei a padronização das
mensagens de erro para o catálogo do item (f). Os textos de documentação foram
revisados antes de cada commit.

### Uso de inteligência artificial na Análise Sintática (Alexandre)

<!-- Transcrito da entrada de 22/11 do diário de bordo. Alexandre: conferir e completar. -->

**Ferramenta/modelo:** Claude Opus 5.5 (Anthropic), via Claude Code.

**Etapas em que foi usada:** classes da AST (`src/ast_nodes.py`) e seus testes, parser
descendente recursivo (`src/parser.py`) e seus testes, conferência do trabalho contra o
enunciado e redação da entrada no diário de bordo.

**Finalidade:** geração de código e testes e revisão da documentação.

**O que foi aceito, reescrito ou descartado:** o código e o texto foram revisados antes do
registro. Foram corrigidos três erros da IA: os campos do `for` não seguiam os nomes do
item (d), o README não declarava a ferramenta de IA e o teste da AST dependia do parser.
