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

**Revisão (itens a e b), feita em 23/11:** conferi a gramática, o `programa_invalido.ml`, o lexer,
as tabelas de tokens e de transições e a seção "Análise léxica" do relatório. Executei o lexer em
cada comportamento descrito na seção (`42;`, `a<=b`, `1x`, `é`, `while`/`whiles` e os dois tipos de
comentário), e todos bateram com o texto. A construção dos subconjuntos do NUM (A = {q0},
B = {q1, q2}, C = {q2, q3}) está correta, e os testes do lexer são 16 válidos e 10 inválidos.
Pontos levantados: a seção de uso de IA do relatório não tinha um exemplo concreto (exigido no
item g); a justificativa de que o lexer reconhece **exatamente** os tokens estava só no rascunho
da seção 5.2 da gramática e não ligava o autômato ao código; o estado `q_div` da tabela é
implementado por lookahead (`_seguinte()`) no código; o `requirements.txt` estava vazio (risco de
nota zero pela obs. 10); e a tabela do relatório não tinha título. As correções entraram em 23/11
(commits `b37aad9`, `5207802`, `70b0273` e `4af8332`). Em 24/11 li a versão corrigida da seção
léxica: atendeu os pontos, e sugeri mais quatro ajustes (completar o parágrafo do BOM com a remoção
em `tokenizar()`, ligar o BOM ao alfabeto Σ, citar o teste do BOM em vez do `git diff` e retirar a
frase dos 34 testes, que ficou desatualizada).

**Uso de IA:** Claude Opus 5.5, via Claude Code, para gerar a AST, o parser e os testes, conferir o
trabalho contra o enunciado e redigir esta entrada. Revisei o código e o texto antes de registrar.
A IA errou em pontos que precisaram de correção: os campos do `for` não seguiam os nomes do item (d),
o README não declarava a ferramenta de IA e o teste da AST dependia do parser. Os detalhes estão em
`CONTEXTO_IA.md`.

**Testes realizados:** `python -m pytest -q` com a AST e o parser juntos: 75 testes aprovados.
Os 6 testes das três decisões passam.

**Dificuldades encontradas:** organizar as entregas em branches separadas sabendo que o parser
depende da AST. Ao criar a branch do parser antes de a AST entrar na `main`, os testes falharam com
`ImportError`, porque `src/ast_nodes.py` ainda estava vazio naquela branch. A solução foi abrir a
AST num PR próprio e só subir o parser depois. Outra dificuldade foi renomear `docs/Relatorio.pdf`
para `docs/relatorio.pdf`: como o Windows não diferencia maiúsculas de minúsculas
(`core.ignorecase = true`), o `git mv` direto não funcionaria, e foi preciso passar por um nome
temporário.

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

## Atualização — 24/11/2026

**Responsável:** Davi

**Etapa:** interpretador sobre a AST, testes de laço, catálogo de erros e revisão geral do projeto.

**O que foi feito:** fiz o merge dos PRs #1 (AST) e #2 (renomeação do relatório) e do branch `docs/revisao-a-b-alexandre`, resolvendo o conflito no diário (as entradas de Alexandre e Manuel foram mantidas, em ordem de data). Fiz uma revisão geral do repositório e corrigi: o BOM passou a ser removido em `tokenizar()`, e não só no `main` do lexer; os `.ml` ganharam a saída esperada no topo; o README ganhou requisitos, instruções de execução e a ferramenta de IA; o `Tasks.md` foi atualizado (commit `3742f56`). Defini duas regras que faltavam na gramática: a divisão trunca em direção a zero (`(0-7)/2 = -3`, e não `-4` como no `//` do Python) e o `print` mostra booleanos como `true`/`false`. Implementei o interpretador sobre a AST (classe `Interpretador`), com verificação das restrições S1 a S5 durante a execução, o `for` executado como `inicializacao; while (condicao) { corpo; atualizacao; }` e um limite de iterações por laço para detectar laço infinito. As mensagens do interpretador passaram a seguir o formato do lexer (`Erro semântico na linha X, coluna Y: ...`). Escrevi `test_lacos.py` (0, 1 e N iterações, `for` alterando a variável de controle, laços aninhados) e `test_laco_infinito.py`, e redigi as seções do relatório sobre tabela de símbolos, semântica operacional, catálogo de erros e estratégia de diagnóstico em `docs/relatorio_semantica_e_erros.md`.

**Uso de IA:** Claude Opus 5.5 (Claude Code) para revisar o projeto, resolver o conflito de merge, gerar o interpretador, os testes e o texto das seções do relatório. Conferi o código e rodei os testes antes do commit. Um acerto da IA que vale registrar: ela apontou que, sem verificar o tipo antes de comparar, o Python avaliaria `1 == true` como verdadeiro (porque `True` é subclasse de `int`), e o teste `test_igualdade_entre_tipos_diferentes` cobre esse caso. Uma falha: na primeira tentativa, a IA tentou gravar os testes num único comando de shell, que falhou por erro de aspas e não gravou nada; os arquivos foram reescritos com o editor.

**Testes realizados:** `python -m pytest -q`: 87 testes aprovados.

**Dificuldades encontradas:** o interpretador foi escrito antes do parser, então a integração com os arquivos `.ml` (`python -m src.interpreter arquivo.ml`) só poderá ser testada quando o parser entrar na `main`. O teste `test_programa_valido_ml` monta à mão a mesma AST que o parser deve gerar para o `programa_valido.ml`.

**Próximos passos:** revisar o parser do Alexandre quando o PR for aberto; testar o pipeline completo com os dois `.ml`; conferir as mensagens sintáticas do catálogo; passar as seções para o relatório em PDF; gravar a demo do vídeo.

## Atualização — 25/11/2026

**Responsável:** Alexandre

**Etapa:** integração do parser com o interpretador, README e revisões.

**O que foi feito:** em 23/11, concluí a revisão dos itens a e b (registrada na entrada de 22/11)
e passei a ler os arquivos `.ml` com `utf-8-sig` no `python -m src.parser`, para aceitar arquivos
salvos com BOM. Em 24/11, li a versão corrigida da seção "Análise léxica" e sugeri quatro ajustes.
Em 25/11, atualizei o repositório local, que estava 12 commits atrás da `main`, e integrei o parser
ao interpretador: o `src/parser.py` ganhou `parse(tokens)`, a função que o `python -m src.interpreter`
chama. Atualizei o teste do `programa_invalido.ml`, porque o arquivo ganhou comentários no topo e o
erro do laço passou da linha 3 para a linha 7. No README, acrescentei os comandos do parser e do
interpretador. PR #4 (diário) e PR #5 (parser e README, commits `165eaa6` e `5534629`).

**Uso de IA:** Claude Opus 5.5, via Claude Code, para testar o parser sobre a `main` atualizada,
fazer a integração com o interpretador, corrigir o teste e o README e redigir esta entrada. Revisei
as alterações e rodei os testes antes de cada commit. Uma falha que exigiu correção: o teste do
`programa_invalido.ml` fixava o erro na linha 3 e quebrou quando o arquivo de exemplo ganhou
comentários. O conceito envolvido é que o lexer calcula a linha e a coluna de cada token sobre o
texto inteiro, comentários incluídos.

**Testes realizados:** `python -m pytest -q`: 122 testes aprovados. `python -m src.interpreter
exemplos/programa_valido.ml` imprime `30`, `10` a `1` e `10`, a saída documentada no topo do arquivo.
`python -m src.interpreter exemplos/programa_invalido.ml` dá "Erro sintático na linha 7, coluna 19:
esperado ';', encontrado ')'".

**Dificuldades encontradas:** manter o repositório local em dia enquanto o grupo trabalhava em
paralelo. Com a cópia 12 commits atrás, o parser não tinha a função que o interpretador esperava,
e o teste do arquivo de exemplo quebrou. O PR #3 também entrou na `main` antes de o campo da revisão
ser preenchido, o que exigiu um commit novo (PR #4).

**Próximos passos:** escrever as seções dos itens c e d do relatório; revisar o interpretador, a
tabela de símbolos, os testes de laço e as seções de semântica e erros (sou o revisor do item e);
conferir a minha seção do `declaracao_IA.md`; montar o PDF final; gravar o meu trecho do vídeo.

## Atualização — 26/11/2026

**Responsável:** Davi

**Etapa:** integração final, conferência do catálogo de erros e testes de variável de controle.

**O que foi feito:** fiz o merge dos PRs #4, #5 (parser integrado) e #6 do Alexandre. Com o parser
na `main`, executei os 17 exemplos do catálogo (os 16 anteriores e o S1′ novo) de erros pelo compilador completo
(`tokenizar` → `parse` → `executar`): todas as mensagens saíram exatamente como documentadas, e as
três fases usam o mesmo formato `Erro <fase> na linha L, coluna C: ...`. Completei as mensagens
sintáticas P2 e P5, que estavam abreviadas no catálogo, e troquei "erro do parser" pelo nome real da
exceção, `ParserError`. Na conferência contra o enunciado, percebi que o item (e) pede um teste de
rejeição com **variável de controle não definida** em laço, e o `test_interpreter_invalido.py` só
testava variável não definida fora de laço. Acrescentei três testes: `while (k < 3)` sem `k`,
`for (i = 0; j < 10; i = i + 1)` sem `j` (o teste confirma que a inicialização roda, que o erro
aparece no primeiro teste da condição e que o corpo nunca executa) e o mesmo `for` ponta a ponta,
do código-fonte ao erro (lexer → parser → interpretador), que é o primeiro teste da suíte a passar
pelas três fases. O caso também entrou no catálogo (S1′). No `src/interpreter.py`, troquei o
`getattr(parser, "ParserError", ...)`, que existia enquanto o parser não estava na `main`, pelo
import direto de `ParserError`. Atualizei o `Tasks.md` com os commits e o status das minhas tarefas.

**Uso de IA:** Claude Opus 5.5 (Claude Code) para conferir o projeto contra o enunciado, rodar os
exemplos do catálogo, escrever os dois testes novos e redigir esta entrada. Conferi o diff e rodei
a suíte antes do commit. Antes do commit, pedi ao agente revisor do Claude Code uma revisão
independente: ele apontou que o teste do `for` não verificava de fato a inicialização, que faltava
um teste ponta a ponta e que a contagem de exemplos estava errada (16 em vez de 17); corrigi os três. A lacuna dos testes de variável de controle não foi apontada quando a IA
gerou os testes em 24/11; só apareceu agora, comparando cada entrega do item (e) com o que existia.

**Testes realizados:** `python -m pytest -q`: 125 testes aprovados.

**Dificuldades encontradas:** nenhuma técnica. O cuidado foi não mexer nas partes dos colegas: as
seções do relatório dos itens c e d, a fundamentação e a montagem do PDF continuam com os responsáveis.

**Próximos passos:** enviar ao Alexandre o texto final das seções e e f para a montagem do PDF;
revisar as seções c e d quando ficarem prontas (sou o revisor); gravar a demo sem cortes do vídeo.
