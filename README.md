# Compilador MiniLang

## Descrição
Projeto desenvolvido para a II Avaliação da disciplina de Linguagens Formais e Compiladores da Universidade Tiradentes. Consiste num compilador-intérprete completo para uma linguagem didática denominada MiniLang, englobando as fases de análise léxica, sintática, árvore sintática abstrata (AST) e interpretação.

## Integrantes do Grupo
| Integrante | Frente principal |
|---|---|
| Alexandre Afonso Silva Virgens | Análise sintática (parser e AST) |
| Davi Santana Loz | Análise semântica (interpretador e catálogo de erros) |
| Manuel Luan Santos Assis | Definição formal e análise léxica |

## Requisitos
- Python **3.10 ou superior** (o código usa `dataclass(kw_only=True)` e a sintaxe de tipos `int | bool`)
- pytest

```bash
pip install -r requirements.txt
```

## Como executar

Todos os comandos são executados na raiz do repositório.

```bash
# Compilador completo (lexer -> parser -> interpretador): executa o programa
python -m src.interpreter exemplos/programa_valido.ml
python -m src.interpreter exemplos/programa_invalido.ml

# Análise léxica: lista os tokens (linha:coluna, tipo, lexema)
python -m src.lexer exemplos/programa_valido.ml

# Análise sintática: mostra a AST como texto indentado
python -m src.parser exemplos/programa_valido.ml

# Testes automatizados
python -m pytest -q
```

Os programas de exemplo ficam em `exemplos/`: `programa_valido.ml` traz a saída
esperada num comentário no topo, e `programa_invalido.ml` traz o erro esperado.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `src/lexer.py` | Analisador léxico (AFD da seção 5 de `docs/gramatica.md`) |
| `src/parser.py` | Parser descendente recursivo |
| `src/ast_nodes.py` | Classes da AST e `formatar()` para visualizar a árvore |
| `src/interpreter.py` | Tabela de símbolos e interpretador sobre a AST |
| `tests/validos/`, `tests/invalidos/` | Testes de entradas válidas e inválidas, por fase |
| `docs/gramatica.md` | Definição formal: alfabeto, tokens, EBNF, precedência, restrições semânticas e AFD |
| `docs/relatorio.pdf` | Relatório |
| `docs/diario_de_bordo.md` | Diário de bordo do grupo |
| `docs/Tasks.md` | Divisão de tarefas, cronograma e registro de contribuições |
| `declaracao_IA.md` | Declaração de uso de inteligência artificial |

## Uso de inteligência artificial
O grupo usou **Claude** (Anthropic: Claude Sonnet 5.5 e Claude Opus 5.5, este via Claude Code)
e **ChatGPT** (OpenAI, GPT-6) como apoio na geração de código, testes e documentação e no
estudo dos conceitos. Todo trecho gerado foi revisado e testado antes do commit. O detalhamento
por integrante, etapa e finalidade está em [`declaracao_IA.md`](declaracao_IA.md) e no
[diário de bordo](docs/diario_de_bordo.md).
