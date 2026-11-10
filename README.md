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

**Antes, uma vez por conta do GitHub:** em Settings → Emails, ligue "Keep my email addresses private" e "Block command line pushes that expose my email". Configure o git com o e-mail `noreply` que aparece nessa página (`git config --global user.email ID+usuario@users.noreply.github.com`). Assim, o e-mail pessoal não vai para os commits.

1. **Crie o repositório:** use o botão "Use this template" no GitHub, ou rode `gh repo create <nome> --template <dono>/template-projeto --private --clone`. O projeto novo começa com um histórico novo.
2. **Configure:** no Claude Code, rode `/configurar-projeto`. Com outro agente, peça para ele seguir o `docs/agents/configurar.md`. O roteiro:
   - pergunta o que falta;
   - preenche os campos `<…>`;
   - ativa os hooks;
   - cria as etiquetas;
   - aplica a stack e o quadro;
   - abre o PR de configuração;
   - oferece a proteção da `main`.
3. **Mescle o PR de configuração.**

O template copia os arquivos, mas não as configurações do repositório: as etiquetas e a proteção da `main` são criadas pelo roteiro.

Os hooks pedem `python3`, e o fluxo do card pede o `gh` autenticado.
