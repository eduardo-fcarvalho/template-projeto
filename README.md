# <Nome do projeto>

<Uma frase: o que o sistema faz e para quem.>

## Status

| | |
|---|---|
| **Fatia atual** | <milestone> |
| **Último entregue** | <XX-NN título (DD/MM/AAAA)> |
| **Próximo** | <XX-NN título> |

O fluxo do card no `AGENTS.md` e o `docs/agents/retomar.md` leem esta seção.

## A base

Este repositório nasceu de um template de regras, guardrails e agentes, sem lógica de negócio. A base tem três camadas:

| Camada | Onde | Quem lê |
|---|---|---|
| 1. Mecânica | `.githooks/`, `scripts/guardrails/`, `.github/workflows/` | o git e o CI, para qualquer agente ou pessoa |
| 2. Instrução neutra | `AGENTS.md`, `docs/`, `GLOSSARY.md`, `.github/pull_request_template.md` | qualquer agente (Codex, Cursor, Claude etc.) |
| 3. Adaptador do Claude Code | `CLAUDE.md`, `.claude/` | só o Claude Code; aponta para as camadas 1 e 2, sem regra própria |

Peças opcionais ficam em `stacks/<nome>/`, cada uma com um README que diz o que copiar para onde.

## Ao criar um projeto a partir da base

1. Preencha os campos `<…>` do `AGENTS.md`, deste README, do `GLOSSARY.md` e do `docs/briefing.md`.
2. Ative os git hooks: `git config core.hooksPath .githooks`.
3. Se usar uma stack ou um quadro, siga o README dela em `stacks/`.
4. Apague o `INVENTARIO.md` e o `CANDIDATOS.md`, que são da base, não do projeto.

Os hooks pedem `python3`, e o fluxo do card pede o `gh` autenticado.
