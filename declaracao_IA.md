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

**Modelos utilizados:** Claude Sonnet 5.5 (Anthropic) e ChatGPT (GPT-6, OpenAI).

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
