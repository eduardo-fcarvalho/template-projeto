# O quadro: espelho opcional das Issues

O backlog mora nas GitHub Issues. O quadro é opcional: um espelho visual delas, para quem não abre o GitHub. Só o subagente `quadro` o atualiza, e ninguém mexe nos cards à mão.

## Escolher

O campo **Quadro** do `AGENTS.md` diz qual ferramenta o projeto usa:

| Valor | O que acontece |
|---|---|
| `nenhum` (padrão) | Só as GitHub Issues. O fluxo do card pula as chamadas ao `quadro`. |
| `trello` | Siga `stacks/quadro-trello/README.md`: ele traz o subagente com as ferramentas do Trello. |
| outra ferramenta | Escreva um subagente que siga as regras abaixo, no mesmo formato do `stacks/quadro-trello/`. |

Montar o quadro (o board, as listas, as etiquetas) é pedido do dono, nunca iniciativa do agente. Se a ferramenta não deixar o agente criar alguma peça, como as etiquetas no Trello, diga ao dono o que ele precisa criar à mão.

## As regras do espelho

O GitHub é a fonte da verdade. A cada chamada, o `quadro` relê tudo e reconcilia o quadro inteiro: o resultado é o mesmo não importa quantas vezes ele rode.

### 1. Ler o GitHub

`gh issue list --state all --limit 200 --json number,title,state,stateReason,labels,milestone,assignees,closedAt,url` e `gh pr list --state open --json number,body`.

### 2. O status de cada issue

De cima para baixo, vale a primeira regra que bater. As listas do quadro têm estes nomes, nesta ordem:

| Lista | Regra |
|---|---|
| Feito | issue fechada com `stateReason` `COMPLETED` |
| (arquivar) | issue fechada com `NOT_PLANNED` ou `DUPLICATE` |
| Em revisão | um PR aberto tem `Closes #N` desta issue |
| Fazendo | issue com responsável |
| Preparado | etiqueta `preparado` |
| Backlog | nenhuma das anteriores |

### 3. O card de cada issue

- **Nome:** o título da issue, que começa pelo prefixo dos cards do `AGENTS.md`. **Descrição:** só o `url` da issue.
- **Etiquetas do quadro,** achadas pelo nome: o tamanho (`tamanho: P` → "P") e a fatia (o nome do milestone). Tire as que não batem mais.
- **Posição:** na ordem do número da issue.
- **Feito:** a data de entrega é o `closedAt`, e o card fica marcado como concluído.

### 4. Reconciliar

- Card que falta: crie na lista certa. Card na lista errada: mova.
- Arquive o card com o prefixo em três casos: a issue foi fechada como `NOT_PLANNED` ou `DUPLICATE`; não existe issue com aquele título; ou há dois cards com o mesmo ID (fica o mais antigo).
- Os cards cujo nome não começa pelo prefixo, como uma legenda, ficam exatamente como estão.
- O `quadro` só escreve cards: nunca cria, renomeia ou apaga listas e quadros.

Termine relendo o quadro e responda com uma linha por card alterado (o que mudou) e qualquer chamada que falhou, com o erro.
