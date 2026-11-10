# Processo: cards e Definição de Pronto

Como o trabalho é organizado. Os cards ficam nas GitHub Issues, agrupados por fatia nos milestones. Os termos seguem o `GLOSSARY.md`.

## Como ler os cards

- **Fonte da verdade:** as GitHub Issues. Se houver quadro, ele é só um espelho, que o subagente `quadro` reconcilia com o GitHub (`docs/agents/quadro.md`).
- **Fatias verticais:** cada card entrega algo que funciona de ponta a ponta. Dentro do card, a ordem é do servidor para a tela: ① a regra ou o endpoint, com os testes; ② o que liga as duas pontas (contrato, tipos gerados); ③ a tela.
- **IDs:** o título da issue começa pelo ID do card (ex.: `XX-12`). O número da issue (`#7`) é outro, porque o GitHub numera issues e PRs na mesma sequência.
- **Fatia:** o milestone da issue, como `v0.1 Esqueleto andante`, na ordem do `docs/decisoes.md`.
- **Tamanho:** etiqueta `tamanho: P` (até 1 dia), `tamanho: M` (2 a 3 dias) ou `tamanho: G` (cerca de 1 semana). Card maior que G deve ser dividido.
- **Prioridade:** etiqueta `prioridade: Essencial` (necessário para a fatia sair) ou `prioridade: Desejável` (primeiro candidato a corte se o prazo apertar).
- **Área:** etiquetas `área: <nome>`, uma por parte do sistema (ex.: `área: Backend`, `área: Frontend`, `área: Infra`).
- **Preparado:** a etiqueta `preparado` diz que o card passou na DoR.
- **Bloqueado por:** a dependência nativa do GitHub ("Blocked by" na lateral da issue), repetida na última linha do corpo. Um card está desbloqueado quando todas as issues que o bloqueiam estão fechadas.
- **Status:** issue aberta está A fazer; com responsável, Fazendo; com PR aberto, Em revisão. Issue fechada como concluída (`COMPLETED`) está Feita, e a data do fechamento é o "Feito em". Fechada como `NOT_PLANNED` ou `DUPLICATE` não é Feita. O PR fecha a issue sozinho quando a descrição diz `Closes #N`.

Buscas úteis:

- Cards desbloqueados: `is:open -is:blocked`
- Desejáveis ainda abertos (candidatos a corte): `is:open label:"prioridade: Desejável"`

## O corpo do card (GCCD)

Card novo vira issue: título com o próximo ID livre, etiquetas, milestone e o corpo em quatro seções, com os títulos em inglês e o conteúdo em português:

- **Goal:** o que fica funcionando no fim, em uma ou duas frases, do ponto de vista de quem usa.
- **Context:** ponteiros, não cópias: as decisões do `docs/decisoes.md`, as ADRs, os termos do glossário, a história de usuário e os arquivos que o card deve tocar.
- **Constraints:** só os guardrails específicos do card. Os globais estão no `AGENTS.md` e valem sempre.
- **Done when:** critérios de aceite verificáveis, cada um com o modo de checar (teste, comando ou tela).

Depois das seções, a linha `Tamanho: M · Bloqueado por: #N`.

## Definição de Preparado (DoR)

Um card entra no trabalho quando:

- [ ] O GCCD está completo, com o Done when verificável.
- [ ] O tamanho vai até G.
- [ ] Nenhum bloqueio aberto fora da própria fatia.
- [ ] As decisões de que ele depende estão fechadas no `docs/decisoes.md`.

## Definição de Pronto (DoD)

Um card só está pronto quando:

- [ ] O Done when do card está cumprido.
- [ ] Os testes estão no seam certo (a interface pública: a API ou o agregado do domínio) e passam no CI. Nos cards com regra de domínio, os testes vieram primeiro (skill `tdd`).
- [ ] Código, telas e testes usam o vocabulário do `GLOSSARY.md`. Termo novo vai para o glossário.
- [ ] Decisão difícil de reverter, surpreendente e resultado de trade-off real virou ADR.
- [ ] Os guardrails do `AGENTS.md` e os das stacks em uso estão sem pendência do `revisor-card`, do `revisor-regras` e da revisão de código.
- [ ] Se o card tem tela, ela foi conferida em largura de celular.
- [ ] A rotina de fechamento foi feita: a entrada no arquivo da fatia (Para a equipe, Técnico, Como testar, Próximo) e o Status do README.
- [ ] O PR segue o template, com "Risco do merge", foi mesclado na `main` com o CI verde e fechou a issue do card.
- [ ] Se houver quadro, o card está em Feito.
