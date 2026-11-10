# Issue tracker: GitHub

Issues e specs deste projeto ficam nas GitHub Issues. Use o `gh` CLI em todas as operações.

## Convenções

- **Criar uma issue**: `gh issue create --title "..." --body "..."`. Use um heredoc para corpos com várias linhas.
- **Ler uma issue**: `gh issue view <número> --json number,title,body,labels,comments`.
- **Listar issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`, com os filtros `--label` e `--state` que fizerem sentido.
- **Tornar uma issue sub-issue de outra**: `gh issue create --parent <pai> ...`, ou `gh issue edit <pai> --add-sub-issue <filha>` depois (`gh` 2.94+). Sem sub-issues, ponha `Parte de #<pai>` no topo do corpo da filha.
- **Comentar**: `gh issue comment <número> --body "..."`
- **Pôr / tirar etiquetas**: `gh issue edit <número> --add-label "..."` / `--remove-label "..."`
- **Fechar**: `gh issue close <número> --comment "..."`

O `gh` descobre o repositório pelo `git remote -v` quando roda dentro do clone.

## Neste projeto: os cards

- O título começa pelo ID do card (ex.: `XX-12`). O número da issue é outro, porque o GitHub numera issues e PRs na mesma sequência.
- Cada card tem as etiquetas `tamanho: …`, `prioridade: …` e `área: …`, e o milestone da fatia.
- O formato do corpo e a Definição de Pronto estão em `docs/processo.md`.
- Bloqueios usam a dependência nativa e são repetidos na última linha do corpo. Para criar: `gh api --method POST repos/{owner}/{repo}/issues/<bloqueado>/dependencies/blocked_by -F issue_id=<id>`, onde `<id>` é o id interno do bloqueador (`gh api repos/{owner}/{repo}/issues/<n> --jq .id`), não o `#número`. Cards desbloqueados: `gh issue list --search "is:open -is:blocked"`.
- O PR fecha a issue do card com `Closes #N` na descrição.

## Quando uma skill disser "publish to the issue tracker"

Crie uma GitHub issue.

## Quando uma skill disser "fetch the relevant ticket"

Leia como em **Ler uma issue** acima.
