# Inventário da origem

De onde veio cada peça da base, em que camada ela fica e o que se fez com ela. A origem foi lida em 10/11/2026, no commit `15f7165`, só para leitura.

**Camadas:**

- **mecânica:** hooks, CI e scripts. Valem para qualquer ferramenta.
- **neutra:** `AGENTS.md` e `docs/`, que qualquer agente lê.
- **adaptador:** `.claude/`, fino, só aponta para as outras duas.
- **stack:** vai para `stacks/<stack>/`, opcional.
- **negócio:** fica fora, no máximo como modelo vazio.

**Ações:**

- **copiar:** entra como está.
- **neutralizar:** entra sem o negócio, com marcadores que cada projeto preenche.
- **deixar de fora:** não entra. O que ainda não se provou vai para o `CANDIDATOS.md`.

**Critério de estável:** a peça já rodou em trabalho real (os PRs #12, #16 e #22 da origem) ou é texto que não mudou desde que foi decidido. Peça só decidida, sem uso, vira candidata. Exceção aprovada em 10/11/2026: o `implementador`, o `po` e o `quadro` entram mesmo sem uso real, porque a origem ainda não chegou à implementação.

## Arquivos

| Arquivo da origem | Camada | Ação | Motivo |
|---|---|---|---|
| `AGENTS.md` | neutra | neutralizar | É o núcleo da base. Ficam: o fluxo do card, os commits, os guardrails do núcleo (ver o mapa abaixo), a tabela de subagentes e as skills. Saem: o nome do projeto, o Trello, a Demonstração, o `/actuator/health`, os IDs EP/ST/AG e a lista de cards sensíveis (as do domínio da origem), que vira um campo para o projeto preencher. A seção "Privacidade nos logs" vai para `stacks/spring/`. A nota "Este arquivo" é trocada pelo `CLAUDE.md` com `@AGENTS.md`. |
| `GLOSSARY.md` | neutra | neutralizar | O corpo já é um modelo vazio. Sai só o cabeçalho com a descrição do negócio. |
| `docs/processo.md` | neutra | neutralizar | Ficam: o GCCD, os status pelo estado da issue, a DoR, a DoD por card, os IDs, os tamanhos, as prioridades, as áreas e os bloqueios. Saem para o `CANDIDATOS.md`: as sprints, a carga × capacidade, o `calendario.py` e o checklist de fechamento da fatia, porque nenhuma fatia fechou ainda. Saem da DoD: Spring Modulith (vai para a stack), Demonstração, Trello e "grill 2b". |
| `docs/agents/domain.md` | neutra | copiar | Já é genérico. Troca-se só o exemplo de ADR (`0001-frontend-react…`) por um neutro. |
| `docs/agents/issue-tracker.md` | neutra | neutralizar | O uso do `gh` é genérico. O prefixo `GA-` vira `XX-`, e as etiquetas seguem o `docs/processo.md`. |
| `docs/adr/0001-frontend-react-separado-da-api.md` | stack | deixar de fora | Foi substituída pela 0004, então não há decisão viva nela. |
| `docs/adr/0002-autenticacao-por-sessao.md` | stack | neutralizar → `stacks/spring/adr/` | Decisão de stack, herdada do template e válida para qualquer sistema Spring com login próprio. Sai o `SegurancaConfig` como nome concreto. |
| `docs/adr/0003-modulos-por-funcionalidade-com-spring-modulith.md` | stack | copiar → `stacks/spring/adr/` | Decisão de stack, sem negócio. |
| `docs/adr/0004-spa-servida-pela-api-na-mesma-origem.md` | negócio | deixar de fora | O motivo dela é do negócio da origem: a hospedagem, o tamanho da equipe e o prazo. |
| (novo) `docs/adr/0000-modelo.md` | neutra | criar | Modelo vazio de ADR, no formato das ADRs da origem (contexto, Considered Options, Consequences). |
| `docs/decisoes.md` (fora da sua lista) | negócio | modelo vazio | As decisões EP/ST/AG ficam fora. Entra só o formato de um registro (Decisão, Quem, Por quê, Descartado, Revisto em), porque o `revisor-regras` e o G10 apontam para ele. |
| `docs/versoes/modelo.md` (fora da sua lista) | neutra | copiar | O AGENTS.md e o guardrail da rotina do card apontam para ele. Está genérico. |
| `README.md`, seção "Status" (fora da sua lista) | neutra | neutralizar | O `/retomar` e o fluxo leem essa seção. Entra um README com a seção Status vazia. |
| `docs/armadilhas.md` (fora da sua lista) | stack | neutralizar → `stacks/spring/armadilhas.md` | Fatos de Spring, Postgres e observabilidade, conferidos. Sai o link para o repositório do legado. |
| `.githooks/commit-msg`, `pre-commit`, `pre-push` | mecânica | copiar | Três linhas cada, sem negócio. Só chamam o `guardrails.py`. |
| `scripts/guardrails/guardrails.py` | mecânica | neutralizar | Fica a lógica geral: G1, G5, G7, G13, `--no-verify`, `core.hooksPath`, `Co-Authored-By`, as listas de Bash por subagente e as conferências do PR. Saem: o `calendario.py` da lista do `po` e o `oci` do G6. A regra "o `quadro` só escreve cards" fica, e só tem efeito quando o projeto usa o Trello. Vão para a stack: o caminho das migrações do Flyway e os arquivos de dependência (`pom.xml`, `package.json`). O prefixo do branch de card (`ga-`) vira genérico. Os IDs AG nas mensagens viram os números do guardrail da base. |
| `scripts/guardrails/test_guardrails.py` | mecânica | neutralizar | Acompanha o script: saem o caso do `calendario.py` e os do Flyway (que vão com a stack), e os casos que citam o dono real do repositório trocam por um dono fictício. |
| `scripts/guardrails/__pycache__/` | mecânica | deixar de fora | Bytecode gerado, já ignorado no `.gitignore`. |
| `.github/workflows/ci.yaml` | mecânica + stack | neutralizar | O job `guardrails` vai para o núcleo, como está. O job `backend` (Maven e contrato OpenAPI) vai para `stacks/spring/`. O job `frontend` (npm, tipos gerados) também vai para `stacks/spring/`, porque depende do contrato da API. |
| `.github/pull_request_template.md` | neutra | neutralizar | As seções ficam. Saem: `GA-NN`, Spring Modulith, Demonstração, Trello e "grill 2b". "Risco do merge" fica, sem afirmar que o merge é deploy. |
| `.gitignore` (fora da sua lista) | mecânica | neutralizar | Entram: segredos (`.env*`, `!.env.example`), IDEs, logs e `__pycache__`. Java e Node vão para a stack. Saem os áudios e as transcrições das reuniões. |
| `.claude/settings.json` | adaptador | neutralizar | O hook `PreToolUse` só chama o `guardrails.py`. No `deny`, sai o `~/.oci` e, no matcher, o Trello. O `deny` repete regras do AGENTS.md como primeira linha de defesa (AG12): não cria regra nova, por isso fica. |
| `.claude/agents/revisor-card.md` | adaptador | neutralizar | Rodou nos três PRs. O prefixo `ga-03` vira genérico. |
| `.claude/agents/revisor-regras.md` | adaptador | neutralizar | Rodou nos três PRs. Os itens G2, G3, G10 e DoD continuam concretos, apontando para os arquivos que o projeto preenche. O G4 (isolamento por cliente) sai. O G12 vai para a stack. Saem o `docs/decisoes.md` por EP/ST/AG e o "Sonnet" do rodapé. **Defeito conhecido:** no PR #22, o hook barrou o `grep` dele no Bash, e as ADRs ficaram sem leitura. Na base, o prompt manda usar as ferramentas Read, Grep e Glob, não o Bash, para ler arquivos. |
| `.claude/agents/implementador.md` | adaptador | neutralizar | Entra por decisão sua de 10/11/2026: ainda não rodou porque a origem está na estruturação, não porque falhou. Os comandos de build (`./mvnw verify`, `npm run build`) saem do prompt e vão para a seção "Comandos" do `AGENTS.md`, que o projeto preenche. |
| `.claude/agents/po.md` | adaptador | neutralizar | Entra pelo mesmo motivo. Lê o `docs/briefing.md` (modelo vazio), o `docs/decisoes.md` e o `docs/processo.md`. Saem a EP3, a EP4, a EP19 e o `calendario.py`, que fica candidato. O Bash dele fica só com `gh issue list` e `gh issue view`. |
| `.claude/agents/quadro.md` | neutra + adaptador | neutralizar, opcional | Entra por decisão sua de 10/11/2026, como espelho opcional das Issues. As regras vão para `docs/agents/quadro.md` (camada neutra): a ferramenta escolhida (`nenhuma` por padrão, só GitHub Issues), a tabela de status e a reconciliação. O subagente com as ferramentas do Trello vai para `stacks/quadro-trello/`, e o projeto o copia para `.claude/agents/` só se escolher o Trello. Saem o nome do board, a URL e o prefixo `GA-`. |
| `docs/briefing.md` (fora da sua lista) | negócio | modelo vazio | O `po` lê. Entram só os títulos das seções (Fatos, Decidido, Perguntas em aberto, Fora do escopo), sem conteúdo. |
| `.claude/commands/retomar.md` | adaptador | neutralizar | Ficam: Status do README, PRs abertos, subagentes presentes e cards desbloqueados. Saem o `calendario.py`, as sprints e a AG15. |

## Mapa dos guardrails

A base renumera os guardrails, porque o G4 sai e outros vão para a stack. As mensagens do `guardrails.py` usam os números novos.

| Origem | Base | Onde | Observação |
|---|---|---|---|
| G1 tudo por PR, só o dono mescla | G1 | núcleo | "o Dev" vira "o dono do repositório" |
| G2 só dado do gerador | G2 | núcleo | "Demonstração" vira "ambientes de teste e demonstração" |
| G3 logs sem dado pessoal | G3 | núcleo | `Mascara` e `ObservabilidadeTest` vão para `stacks/spring/` |
| G4 isolamento por cliente na SQL nativa | (sai) | negócio | Isolamento por cliente é do domínio |
| G5 segredos | G4 | núcleo | `~/.oci` sai da lista |
| G6 infraestrutura do dono | G5 | núcleo | Sai o `oci`. `ssh` e `scp` ficam |
| G7 git destrutivo | G6 | núcleo | |
| G8 Flyway | — | `stacks/spring/` | Volta como G-S1, se a stack for usada |
| G9 dependência com motivo | G7 | núcleo | Sai a ST15 (bibliotecas de componentes) |
| G10 conflito com ADR ou decisão | G8 | núcleo | "EP, ST ou AG" vira "decisões registradas" |
| G11 contêineres só na tarefa | G9 | núcleo | |
| G12 API compatível com o front anterior | — | `stacks/spring/` | Só vale com SPA separada da API |
| G13 guardrails são do dono | G10 | núcleo | |
| G14 card que cresce | G11 | núcleo | Pare e chame o `po` para propor o corte |

## Fora da base: código novo que a etapa 4 exige

A etapa 4 pede que o hook barre um commit fora do padrão `tipo: descrição`. **A origem não tem essa regra:** o `commit-msg` dela só barra o `Co-Authored-By`. O padrão de commit é estável (todos os commits da origem o seguem), mas a conferência seria código novo, que nunca rodou na origem.

Aprovado em 10/11/2026: uma função `motivo_formato` no `commit-msg`, com uma regex, testada como as outras, e com os tipos usados na origem: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build` e `perf`. As mensagens de merge e de revert do próprio git passam.

## Para o CANDIDATOS.md

- O espelho do quadro em outra ferramenta, como o Miro: a origem não tem implementação. O Miro foi descartado lá porque uma tabela num canvas só imita o kanban (AG23). Para usar outra ferramenta, basta escrever o subagente seguindo o contrato de `docs/agents/quadro.md`, como o de `stacks/quadro-trello/`.
- Sprints, carga × capacidade e `calendario.py` (AG15, EP4): a estimativa nunca foi medida.
- O checklist de fechamento da fatia, a tag e a Release (AG6, AG11): nenhuma fatia fechou.
- O portão do deploy (AG13, camada 3): é o GA-05 da origem, ainda aberto.
- O CI barrar o `Co-Authored-By` mesmo com `--no-verify` (GA-11, issue #21 da origem, aberta).
- A acessibilidade na DoD: "a definir no grill 2b".
- O `/clear` a cada card e o `/handoff` (AG28): só três cards fechados até aqui. Fica no fluxo como recomendação, e a regra entra quando se provar.
