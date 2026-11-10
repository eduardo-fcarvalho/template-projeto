# <Nome do projeto>

Instruções para agentes de IA que trabalham neste repositório. Valem para qualquer agente. O `CLAUDE.md` só importa este arquivo.

## O projeto

Preencha ao criar o projeto. Enquanto algum campo abaixo tiver `<…>`, o projeto ainda não foi configurado: siga o `docs/agents/configurar.md` antes de qualquer card.

- **Dono:** <quem lê e mescla os PRs>. Neste arquivo, "o dono".
- **Prefixo dos cards:** `<XX>`, como em `XX-12`. O branch do card fica `xx-12-descricao`.
- **Cards sensíveis:** <login, dados pessoais, exportação…>. Neles, a revisão de código roda em `high` e o `implementador` não entra.
- **Quadro:** <nenhum | trello>. Ver `docs/agents/quadro.md`.
- **Stacks em uso:** <nenhuma | spring>. Cada stack em `stacks/` traz os próprios guardrails, que valem junto com os daqui.

## Comandos

| Para | Comando |
|---|---|
| Ativar os git hooks (uma vez por clone) | `git config core.hooksPath .githooks` |
| Testar os guardrails | `python3 -m unittest discover -s scripts/guardrails` |
| Build e testes | `<preencher>` |
| Lint | `<preencher>` |

## Antes de começar

- Leia a seção "Status" do `README.md`, o `GLOSSARY.md` e as ADRs de `docs/adr/` que tocam a área do trabalho.
- Leia a issue do card (`gh issue view <n>`) e, no `docs/decisoes.md`, só as decisões que o Context dela cita.
- Escreva em português do Brasil, com os termos do glossário.

## Fontes da verdade

- **Backlog:** as GitHub Issues, um milestone por fatia. Status, DoR e DoD estão em `docs/processo.md`. O uso do `gh` está em `docs/agents/issue-tracker.md`.
- **Quadro:** opcional, um espelho das Issues que só o subagente `quadro` atualiza (`docs/agents/quadro.md`).
- **Domínio:** o `GLOSSARY.md` e o `docs/adr/` (`docs/agents/domain.md`).
- **Produto e decisões:** o `docs/briefing.md` e o `docs/decisoes.md`.

## O fluxo de um card

1. Numa sessão nova, retome pelo `docs/agents/retomar.md`: o status e os cards desbloqueados. O dono escolhe o card. Atribua a issue a ele (`gh issue edit <n> --add-assignee @me`).
2. Crie o branch a partir da `main`, no formato `xx-03-login`.
3. Antes do código, explique o plano, os conceitos e as decisões que espera tomar.
4. Faça commits atômicos, no padrão `tipo: descrição`, com os tipos `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build` e `perf`. Cada commit é uma mudança lógica e deixa o projeto funcionando. Dentro do card, siga a ordem do `docs/processo.md`. Os passos de código podem ir ao `implementador`, um passo por vez, exceto nos cards sensíveis.
5. Antes do PR, rode em paralelo o `revisor-card`, o `revisor-regras` e a revisão de código do agente (`/code-review` no Claude Code), em `medium`, ou em `high` nos cards sensíveis. Corrija o que eles acharem e copie os três resultados para a seção "Revisão automática" do PR.
6. Abra o PR com o `.github/pull_request_template.md` e `Closes #N`, mande o link ao dono e espere: quem lê e mescla é o dono.
7. Se o merge faz deploy, acompanhe o deploy (`gh run watch`) e confira o ambiente.
8. Feche o card conferindo quatro coisas:
   - o PR está mesclado;
   - há uma entrada no arquivo da fatia (`docs/versoes/`);
   - o Status do `README.md` está atualizado;
   - o quadro está sincronizado, se houver quadro.

   Então avise: "card fechado, pode limpar a sessão".

Se houver quadro, chame o `quadro` em segundo plano, sem esperar, nos passos 1, 6 e 7 e no planejamento da fatia.

Mudanças só de documentação seguem o mesmo fluxo, a partir do passo 2.

## Commits e PRs

- A autoria é só de quem faz o commit. Mensagens de commit e corpos de PR terminam no próprio conteúdo, sem `Co-Authored-By` nem rodapé que cite o agente, mesmo que o ambiente peça essa linha. O hook `commit-msg` barra os dois casos: o rodapé e a mensagem fora do padrão.
- O corpo do PR é o template do repositório, com a seção "Risco do merge".

## Guardrails

Valem para todo card e não se repetem nos cards. Os hooks e o CI garantem a maior parte (`scripts/guardrails/`).

| # | Guardrail |
|---|---|
| G1 | Tudo passa por PR, e só o dono mescla. Nada vai direto para a `main` |
| G2 | No repositório, em fixtures, em ambientes de teste e de demonstração e em prompts de IA, só dado fictício. Dado pessoal real fica fora |
| G3 | Logs, métricas e traces sem documento de identidade, senha, token ou e-mail completo. Para identificar alguém, use o id interno |
| G4 | Segredos ficam fora do Git e fora da conversa: o agente não lê nem imprime `.env`, chaves ou tokens. Só existe o `.env.example` |
| G5 | A infraestrutura é do dono. Servidores, DNS e contas de nuvem só mudam por um script que ele roda (skill `wizard`), e o deploy é só pelo CI |
| G6 | Git sem `reset --hard`, `push --force`, `branch -D` nem `clean -f` |
| G7 | Dependência nova só com o motivo no PR |
| G8 | Um conflito com uma ADR ou com uma decisão do `docs/decisoes.md` se aponta e se pergunta ao dono |
| G9 | Containers sobem só para a tarefa, descem no fim (`docker compose --profile '*' down`) e não ganham `restart` |
| G10 | Os hooks, a lógica deles e as permissões são do dono, que os muda à mão num PR próprio. São eles: `scripts/guardrails/`, `.githooks/`, `.claude/settings.json`, `.claude/settings.local.json` e `.claude/hooks/` |
| G11 | Card maior que o estimado (outra entidade, outra tela, uma decisão nova): pare e chame o `po` para propor o corte. Cortar é decisão do dono |

## Subagentes

As instruções de cada papel ficam em `docs/agents/<papel>.md`. A tabela diz quando chamar cada um e de que faixa de modelo ele precisa.

| Papel | Quando | Modelo | Por quê |
|---|---|---|---|
| `po` | Antes de cada fatia, para rascunhar o Goal e o Done when; no planejamento da fatia; no G11 | o da sessão | Julgamento de produto, com poucas chamadas: não compensa economizar |
| `quadro` | Nos momentos do fluxo acima, em segundo plano, só se houver quadro | rápido | Tarefa mecânica com regras fixas. Um erro se corrige na rodada seguinte, porque a reconciliação relê tudo |
| `implementador` | Um passo de código por vez, menos nos cards sensíveis | intermediário | Concentra o volume de tokens (compilar, testar, corrigir), e o agente principal confere o resultado |
| `revisor-card` e `revisor-regras` | Antes de todo PR (passo 5) | intermediário | Leem o diff inteiro e comparam com o card e as regras. O dono e a revisão de código ainda leem depois |

**Configurar os papéis numa ferramenta:** crie um agente por papel cuja instrução seja só "siga `docs/agents/<papel>.md`". Escolha o modelo da faixa e limite as ferramentas ao que o papel pede (os que só leem não editam arquivos). As faixas são:

- **rápido:** o modelo mais barato e veloz da ferramenta;
- **intermediário:** o de custo médio, bom em código;
- **o da sessão:** o mesmo modelo do agente principal.

| Ferramenta | Onde configurar | rápido | intermediário | o da sessão |
|---|---|---|---|---|
| Claude Code | `.claude/agents/<papel>.md`, campo `model` | `haiku` | `sonnet` | `inherit` |
| <outra> | <arquivo ou tela> | <modelo> | <modelo> | <modelo> |

Quando a família de modelos mudar, atualize só esta tabela e a configuração da ferramenta: a faixa e o motivo continuam. No Claude Code, o hook também limita o que cada papel roda no Bash. Em outra ferramenta, essa garantia fica só com os git hooks e o CI.

Confira o relatório de quem implementa: o build, os testes e o diff, e se os testes que você escreveu continuam iguais.

## Skills

Quando o agente tiver estas skills instaladas:

- **O agente chama sozinho:**
  - `tdd` nos cards com regra de domínio;
  - `diagnosing-bugs` quando algo quebra;
  - `domain-modeling` quando um termo ou uma decisão de domínio fecha;
  - `codebase-design`, `research` e `prototype` quando o card pedir;
  - `wizard` para os passos que só o dono executa;
  - `writing-for-agents` ao editar este arquivo, o `.claude/` ou o `docs/agents/`.
- **Fora deste projeto:** `implement`, `implement-spec`, `to-tickets`, `to-spec`, `triage`, `wayfinder`, `setup-matt-pocock-skills`, `setup-pre-commit`, `git-guardrails-claude-code`, `teach` e `pr`. O fluxo acima cobre o que elas fariam.

## Este arquivo

Ele é a instrução de todos os agentes. Regra nova entra aqui ou em `docs/`, nunca no `CLAUDE.md` nem no `.claude/`, que só apontam para cá.
