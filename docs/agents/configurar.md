# Configurar um projeto criado a partir da base

Roteiro para a primeira sessão num repositório que nasceu do template. Cada passo termina num critério verificável. Siga na ordem.

## 1. Partida

- Ative os git hooks: `git config core.hooksPath .githooks`.
- Crie o branch `configuracao-inicial` a partir da `main`.
- Rode `python3 -m unittest discover -s scripts/guardrails`.

**Pronto quando:** `git config core.hooksPath` responde `.githooks`, você está no branch novo e os testes passam.

## 2. Perguntas ao dono

Faça todas as perguntas de uma vez, cada uma com a sugestão que você recomenda. Não preencha nada antes das respostas.

| Campo | Pergunta | Onde vai |
|---|---|---|
| Nome | Como o projeto se chama? | `<Nome do projeto>` no `AGENTS.md`, no `README.md`, no `GLOSSARY.md` e no `docs/briefing.md` |
| Descrição | O que o sistema faz, e para quem, numa frase? | A segunda linha do `README.md` e do `GLOSSARY.md` |
| Dono | Quem lê e mescla os PRs? | "Dono" no `AGENTS.md` |
| Prefixo | Que prefixo de duas letras os cards usam? | "Prefixo dos cards" no `AGENTS.md`, com o branch em minúsculas |
| Cards sensíveis | Que tipos de card tocam segurança ou dado pessoal? | "Cards sensíveis" no `AGENTS.md` |
| Áreas | Quais partes do sistema viram etiquetas `área: …`? | Passo 4 |
| Stack | Qual pasta de `stacks/` o projeto usa, ou nenhuma? | "Stacks em uso" no `AGENTS.md` e o passo 5 |
| Quadro | Só GitHub Issues, ou um quadro espelho (Trello)? Se for Trello, qual o board? | "Quadro" no `AGENTS.md` e o passo 5 |
| Comandos | Quais os comandos de build e testes e de lint? A stack escolhida já sugere os dela | A tabela "Comandos" do `AGENTS.md` |
| Ferramentas | Além do Claude Code, que agentes vão trabalhar aqui? | A tabela de faixas de modelo do `AGENTS.md`: preencha a linha `<outra>`, ou apague-a se for só o Claude Code |

**Pronto quando:** cada linha da tabela tem uma resposta do dono.

## 3. Preencher os campos

Troque cada marcador da tabela pela resposta. No `README.md`:

- a tabela "Status" fica com "nenhuma ainda" nos três campos;
- a seção "Ao criar um projeto a partir da base" sai, porque já foi cumprida.

Faça um commit: `docs: configuração inicial do projeto`.

**Pronto quando:** nenhum dos marcadores da tabela do passo 2 aparece mais no `AGENTS.md`, no `README.md`, no `GLOSSARY.md` nem no `docs/briefing.md`. Confira com o `grep -n '<' ` desses quatro arquivos. Os `<n>` e `<número>` dentro de comandos são sintaxe e ficam.

## 4. Etiquetas no GitHub

Crie as etiquetas que o `docs/processo.md` usa. O `--force` deixa o passo repetível:

```
gh label create "tamanho: P" --force
gh label create "tamanho: M" --force
gh label create "tamanho: G" --force
gh label create "prioridade: Essencial" --force
gh label create "prioridade: Desejável" --force
gh label create "preparado" --force
gh label create "área: <nome>" --force   # uma por área do passo 2
```

**Pronto quando:** `gh label list` mostra todas elas.

## 5. Stack e quadro

Para a stack escolhida, siga o `stacks/<stack>/README.md`. Duas regras valem para qualquer stack:

- **As ADRs da stack** vão para `docs/adr/` com o próximo número livre (`0001-`, `0002-`…).
- **Arquivos protegidos pelo G10** (`scripts/guardrails/`, `.githooks/`, `.claude/settings.json`) são do dono. Mostre a ele a linha exata a mudar, como o valor de `MIGRACOES` da stack Spring, e espere que ele edite à mão. O hook barra a edição pelo agente, e esse bloqueio é o comportamento certo.

Se o quadro for o Trello, siga o `stacks/quadro-trello/README.md`. Montar o board só acontece se o dono pedir.

Depois, apague as pastas de `stacks/` que o projeto não usa.

Faça um commit por peça: `ci: jobs da stack <stack>`, `docs: ADRs da stack <stack>`, `feat: quadro no Trello`, e assim por diante.

**Pronto quando:** cada passo do README da stack e do quadro está feito, ou foi entregue ao dono com a linha exata. Só ficam em `stacks/` as pastas em uso.

## 6. Limpeza

Apague o `INVENTARIO.md` e o `CANDIDATOS.md`: eles registram a origem da base, não o projeto. Commit: `chore: remove os arquivos da base`.

**Pronto quando:** `ls` na raiz não mostra nenhum dos dois.

## 7. PR

Rode os testes dos guardrails de novo. Abra o PR com o template do repositório. Na seção "Técnico", liste:

- o que foi configurado;
- o que ficou com o dono (as edições à mão do passo 5).

Mande o link ao dono.

**Pronto quando:** o PR está aberto, o job `guardrails` do CI terminou verde e o dono tem o link.

## 8. Proteção da `main`

O template não copia as configurações do repositório. Ofereça ao dono proteger a `main` no GitHub: exigir PR e o job `guardrails` verde, sem aprovação obrigatória, porque ninguém aprova o próprio PR. Pergunte também se a regra vale para ele. Aplique só com o sim dele:

```
gh api -X PUT repos/{owner}/{repo}/branches/main/protection \
  -F 'required_status_checks[strict]=false' -f 'required_status_checks[contexts][]=guardrails' \
  -F enforce_admins=true -F 'required_pull_request_reviews[required_approving_review_count]=0' \
  -F restrictions=null -F allow_force_pushes=false -F allow_deletions=false
```

Se a regra não vale para o dono, use `enforce_admins=false`. Num repositório privado no plano Free, a API responde 403: diga ao dono que a proteção pede repositório público ou plano pago e que, até lá, o G1 fica só com os hooks.

**Pronto quando:** `gh api repos/{owner}/{repo}/branches/main/protection` mostra o check `guardrails` e o PR obrigatório, ou o dono foi avisado do 403, ou ele recusou.
