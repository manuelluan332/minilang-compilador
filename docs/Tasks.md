# Divisão de Tarefas — Projeto Unidade II (MiniLang)

**Disciplina:** Linguagens Formais e Compiladores
**Repositório:** minilang-compilador

## Integrantes

| Sigla | Integrante | Frente principal |
|---|---|---|
| **AL** | Alexandre Afonso Silva Virgens | Análise sintática (parser + AST) |
| **DA** | Davi Santana Loz | Análise semântica (interpretador + erros) |
| **MA** | Manuel Luan Santos Assis | Definição formal + análise léxica |

### Regras de trabalho

1. **Cada um implementa a sua frente e revisa a de outro colega.** Na arguição, que é individual, qualquer integrante pode ser perguntado sobre qualquer parte. Por isso todo item tem um responsável **e** um revisor.
2. **Cada um escreve os testes do próprio módulo** e a seção do relatório correspondente.
3. **Um commit por fase, feito pelo próprio responsável.** O histórico do Git é evidência de quem fez o quê (item g).
4. **O uso de IA em cada tarefa é registrado** no diário de bordo, na coluna "IA" abaixo e no `declaracao_IA.md`.

---

## Itens do enunciado

Status: ⬜ não iniciado · 🟡 em andamento · 🔍 em revisão · ✅ concluído


### Item a — Definição formal da linguagem (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Alfabeto, EBNF, tabela de precedência/associatividade | `docs/gramatica.md` | MA | AL | 🔍 | Sim (Claude Sonnet 5.5, rascunho) | `0203694` |
| 5 exemplos comentados (válido + inválido léxico/sintático/semântico) | `docs/gramatica.md` | MA | DA | 🔍 | Sim (Claude Sonnet 5.5 ,analise da documentação) | `0203694` |
| Programa válido com while e for | `exemplos/programa_valido.ml` | MA | DA |  🔍| 	Sim (ChatGPT, apoio e revisão)|`c48e250` |
| Programa inválido com laço mal formado | `exemplos/programa_invalido.ml` | MA | AL | 🔍 |	Sim (ChatGPT, apoio e revisão) | `c48e250` |
| Fechar as decisões em aberto (`/* */`, comparação não associativa, sem menos unário) | `docs/gramatica.md` | **Todos** | — | 🟡 | Sim (Claude Sonnet 5.5 e ChatGPT,revisão) |  `c48e250` |

### Item b — Lexer (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Implementação do lexer | `src/lexer.py` | MA | AL | 🔍 | Sim (Claude Sonnet 5.5,apoio nos teste)|`c48e250` |
| Tabela de tokens e tabela de transições (seção "Lexer") | `docs/gramatica.md` | MA | AL | 🔍 | Sim  (Claude Sonnet 5.5,analise da documentação )| `0203694` |
| Testes válidos | `tests/validos/test_lexer_valido.py` | MA | DA | 🔍 | Sim (Claude Sonnet 5.5,apoio nos testes)|`c48e250` |
| Testes inválidos (`@`, `1x`, comentário não fechado) | `tests/invalidos/test_lexer_invalido.py` | MA | DA | 🔍 |Sim (Claude Sonnet 5.5,apoio nos testes)  | `c48e250`  |
| Relatório: seção "Análise léxica" (ER → AFN → AFD → lexer) | `docs/relatorio.pdf` | MA | AL | 🔍 | 	Sim (ChatGPT, apoio na documentação)| `c48e250` |


### Item c — Parser descendente recursivo (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Implementação do parser | `src/parser.py` | AL | MA | 🟡 | Sim (Claude Opus 5.5, Claude Code, geração do código) | aguardando PR |
| Testes válidos (incluindo while e for) | `tests/validos/test_parser_valido.py` | AL | MA | ⬜ | | |
| Testes inválidos (incluindo laço mal formado) | `tests/invalidos/test_parser_invalido.py` | AL | MA | ⬜ | | |
| Relatório: árvores de `1+2*3`, `(1+2)*3`, while e for, mais a justificativa formal | `docs/relatorio.pdf` | AL | DA | ⬜ | | |
| Relatório: comparação com outra técnica (LL(1) com tabela / LR) | `docs/relatorio.pdf` | AL | MA | ⬜ | | |

### Item d — AST (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Classes da AST (incluindo While e For) — **fazer primeiro, porque o interpretador depende delas** | `src/ast_nodes.py` | AL | DA | 🔍 | Sim (Claude Opus 5.5, Claude Code, geração do código) | `0ba5ceb` |
| Testes da AST (`1+2*3`, for com 3 cláusulas) | `tests/validos/test_ast.py` | AL | DA | 🔍 | Sim (Claude Opus 5.5, Claude Code, geração dos testes) | `0ba5ceb` |
| Relatório: diagrama da AST e justificativa árvore concreta × AST | `docs/relatorio.pdf` | AL | DA | ⬜ | | |

### Item e — Interpretador (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Tabela de símbolos (inserção e busca) | `src/interpreter.py` | DA | AL | 🔍 | Sim (Claude, Claude Code, apoio no código) | `68c22e0` |
| Interpretador sobre a AST (incluindo while e for) | `src/interpreter.py` | DA | AL | ⬜ | | |
| Testes válidos | `tests/validos/test_interpreter_valido.py` | DA | MA | 🟡 | Sim (Claude, Claude Code, apoio nos testes) | `68c22e0` |
| Testes inválidos (condição não booleana, variável não definida) | `tests/invalidos/test_interpreter_invalido.py` | DA | MA | 🟡 | Sim (Claude, Claude Code, apoio nos testes) | `68c22e0` |
| Relatório: tabela de símbolos, semântica operacional e justificativa | `docs/relatorio.pdf` | DA | AL | ⬜ | | |

### Item f — Catálogo de erros (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Padronizar as mensagens de erro (linha/coluna) nas três fases | `src/*.py` | DA | Todos | ⬜ | | |
| Catálogo: tabela com mensagem, causa e exemplo (≥3 por categoria) | `docs/relatorio.pdf` | DA | MA | ⬜ | | |
| Comentário com o resultado esperado no topo de cada teste inválido | `tests/invalidos/` | Cada dono do arquivo | DA | ⬜ | | |
| Justificativa da estratégia de recuperação/diagnóstico | `docs/relatorio.pdf` | DA | AL | ⬜ | | |

### Item g — Testes, diário e relatório (1,0)
| Tarefa | Arquivo | Responsável | Revisor | Status | IA usada? | Commit |
|---|---|---|---|---|---|---|
| Testes de laço: executa 0, 1 e N vezes; for alterando a variável de controle | `tests/validos/test_lacos.py` | DA | AL | ⬜ | | |
| Laço infinito com limite de iterações | `tests/invalidos/test_laco_infinito.py` | DA | MA | ⬜ | | |
| Diário de bordo (cada um registra a própria entrada) | `docs/diario_de_bordo.md` | **Todos** | — | 🟡 | | `fd6ed77`, `c4c0689`, `eb2e406`, `553dd0d` |
| Relatório: pergunta de pesquisa + 3 a 4 exemplos de acerto/falha da IA (cada um traz pelo menos 1) | `docs/relatorio.pdf` | **Todos** | — | ⬜ | | |
| Relatório: fundamentação teórica | `docs/relatorio.pdf` | MA | Todos | ⬜ | | |
| Montagem final do PDF (2 a 3 páginas na parte de análise) | `docs/relatorio.pdf` | AL | Todos | ⬜ | | |

### Item h — Vídeo e arguição (1,0)
| Tarefa | Responsável | Status |
|---|---|---|
| Visão geral da arquitetura (fases e dependências) | MA | ⬜ |
| Demo sem cortes: `programa_valido.ml` e `programa_invalido.ml` | DA | ⬜ |
| Trecho gerado por IA (aceito, reescrito ou descartado) e o conceito teórico envolvido | AL | ⬜ |
| Gravação/edição e entrega em `docs/apresentacao.mp4` ou link no README | **Todos** (todos falam e aparecem) | ⬜ |
| Ensaio da arguição: cada um explica o módulo que **revisou** | **Todos** | ⬜ |

### Itens gerais
| Tarefa | Arquivo | Responsável | Status |
|---|---|---|---|
| README: como executar, integrantes, ferramenta de IA | `README.md` | AL | 🔍 (rascunho feito por DA; falta o comando do parser/interpretador) |
| Declaração de IA: ferramenta/modelo, etapas e finalidade | `declaracao_IA.md` | **Todos** (cada um declara o próprio uso) | 🟡 (MA e DA feitos; falta AL confirmar a sua) |
| Dependências (pytest) | `requirements.txt` | MA | ✅ `b37aad9` |

---

## Cronograma

A apresentação foi remarcada para **01/12 (ter)**. O vídeo deve ser entregue **2 dias antes da arguição**, ou seja, até 29/11. Meta do grupo: **tudo pronto até 26/11 (qui)**, deixando sexta a domingo como folga para ajustes.

| Data | Meta | Quem |
|---|---|---|
| 12–14/11 | Estrutura do repositório, rascunho da gramática | MA ✅ |
| 17/11 (ter) | Divisão de tarefas · tabela de símbolos | DA ✅ |
| 20/11 (sex) | Lexer e testes · exemplos `.ml` · seção léxica do relatório | MA ✅ |
| 23/11 (seg) | `ast_nodes.py` (**urgente: destrava o interpretador**) · fechar as decisões em aberto · revisões dos itens a e b | AL · Todos · DA, AL |
| 24/11 (ter) | Parser e testes · interpretador sobre a AST | AL · DA |
| 25/11 (qua) | Integração, testes de laço, catálogo de erros · revisões cruzadas · seções do relatório | Todos |
| 26/11 (qui) | **Tudo pronto:** relatório em PDF, README, declaração de IA e **gravação do vídeo** | Todos |
| 27–28/11 (sex–sáb) | Folga para ajustes e correções | Todos |
| 29/11 (dom) | **Prazo de entrega do vídeo** (2 dias antes da arguição) | Todos |
| 30/11 (seg) | Ensaio da arguição e revisão final | Todos |
| 01/12 (ter) | **Apresentação** | Todos |

---

## Registro de contribuições

Preencher ao concluir cada tarefa. É a evidência de quem fez o quê.

| Data | Integrante | O que foi feito | Commit | Uso de IA (ferramenta e para quê) | Revisado por |
|---|---|---|---|---|---|
| 12/11/2026 | MA | Estrutura inicial do repositório e README | `4a54bb8`, `567b499` | — | |
| 14/11/2026 | MA | Rascunho de tokens, EBNF, tabela de transições e exemplos | `0203694` | Claude Sonnet 5.5 — rascunho inicial | |
| 14/11/2026 | MA | Primeira entrada do diário de bordo | `fd6ed77` | — | |
| 17/11/2026 | DA | Divisão de tarefas (`docs/Tasks.md`) | `088174d` | Claude — apoio na organização da divisão de tarefas | |
| 17/11/2026 | DA | Tabela de símbolos, `ErroSemantico` e testes iniciais do interpretador | `68c22e0` | Claude (Claude Code) — apoio no código e nos testes | |
| 20/11/2026 | MA | Lexer, testes do lexer, exemplos `.ml` e seção léxica do relatório | `c48e250`, `a3615ec` | Claude Sonnet 5.5 e ChatGPT — código, testes e texto | DA, AL |
| 22/11/2026 | DA | Revisão dos itens a e b, cronograma, diário e declaração de IA | `236dc0b`, `3ea46ed`, `c4c0689` | Claude Opus 5.5 (Claude Code) — revisão e redação | |
| 22/11/2026 | AL | Classes da AST e testes (PR #1); renomeia `relatorio.pdf` (PR #2); diário e posição sobre as decisões em aberto | `0ba5ceb`, `b419c69`, `eb2e406` | Claude Opus 5.5 (Claude Code) — código, testes e texto | DA |
| 23/11/2026 | MA | Correções da revisão: `requirements.txt`, BOM no lexer, gramática, declaração de IA, diário | `b37aad9`, `5207802`, `70b0273`, `4af8332`, `553dd0d` | Claude Sonnet 5.5 — correções de código e texto | AL |
| 24/11/2026 | DA | Merge dos PRs #1 e #2 e do branch de revisão (conflito no diário resolvido); revisão geral; BOM tratado em `tokenizar` + teste; saída esperada nos `.ml`; README; atualização deste arquivo | `dacbd73`, `ef6281a`, `5f20a59` | Claude Opus 5.5 (Claude Code) — revisão, correções e redação | |
| | | | | | |

## Resumo por integrante

| Integrante | Itens como responsável | Itens como revisor | Commits |
|---|---|---|---|
| Alexandre (AL) | c, d, README, montagem do relatório, trecho de IA no vídeo | a, b, e, f | 3 |
| Davi (DA) | e, f, testes de laço, demo no vídeo | a, b, c, d | 5 (+3 merges) |
| Manuel (MA) | a, b, fundamentação teórica, arquitetura no vídeo | c, e, f, g | 11 |
