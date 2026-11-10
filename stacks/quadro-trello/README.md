# Quadro no Trello

Espelho das GitHub Issues num board do Trello, pelo MCP do Trello no Claude Code. As regras estão em `docs/agents/quadro.md`; aqui fica só o que é do Trello.

## Usar

1. Conecte o MCP do Trello ao Claude Code.
2. Copie `stacks/quadro-trello/.claude/agents/quadro.md` para `.claude/agents/quadro.md`.
3. No `AGENTS.md`, ponha `Quadro: trello`.
4. Preencha "Este projeto", abaixo.
5. Monte o board. Se o dono pedir, o agente cria o board, as listas e a legenda pelo MCP, nesta ordem: Backlog, Preparado, Fazendo, Em revisão, Feito. **O dono cria as etiquetas à mão**, porque o MCP não cria etiquetas: P, M e G, e uma por fatia, com o nome do milestone.

## Este projeto

- **Board:** <nome e URL>

## O que o MCP do Trello faz e não faz

Conferido na origem em 04/11/2026; confira de novo numa versão nova do conector.

- Faz: cria board, listas, cards e checklists; move cards; marca como concluído; põe e tira etiquetas.
- Não faz: cria etiquetas ou workspaces; preenche campos personalizados.
- O conector é da conta do dono no claude.ai, então outros agentes não atualizam o quadro.

## Garantias

- O hook (`scripts/guardrails/`) limita o Bash do `quadro` a `gh issue list` e `gh pr list` e o impede de escrever listas e boards (`trelloWriteList`, `trelloWriteBoard`).
- O modelo é o Haiku: a tarefa é mecânica, e um erro se corrige na rodada seguinte, porque a reconciliação relê tudo.
