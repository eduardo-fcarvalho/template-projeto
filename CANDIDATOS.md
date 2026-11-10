# Candidatos

O que ficou fora da base por ainda não estar estável: foi decidido no projeto de origem, mas ainda não se provou em trabalho real. Um item entra na base quando a origem o usar sem precisar de ajuste. Ao entrar, ele sai daqui e ganha um commit próprio.

| Candidato | O que é | Por que ainda não entrou | Sinal para entrar |
|---|---|---|---|
| Sprints e carga × capacidade | Sprints de duas semanas, separadas das fatias. Capacidade de 80% dos dias úteis, com um script que soma os tamanhos e dá a linha de corte | A estimativa nunca foi medida contra o ritmo real | Duas sprints fechadas com o ritmo real anotado |
| Fechamento da fatia | Revisão do diff da fatia inteira, relatório técnico e para a equipe, tag `vX.Y.0`, Release e milestone fechado | Nenhuma fatia fechou na origem | A primeira fatia fechada seguindo o checklist |
| Portão do deploy | O deploy só roda com o CI verde e se o commit da `main` veio de um PR mesclado, conferido na API do GitHub | O card ainda está aberto na origem | O workflow rodando e barrando um push direto |
| CI confere os commits | O CI repete o `commit-msg` (padrão e `Co-Authored-By`) em cada commit do PR, para pegar quem usou `--no-verify` | Issue aberta na origem | O job mesclado e barrando um PR de teste |
| Acessibilidade na DoD | Como conferir a acessibilidade das telas | Ainda "a definir" na origem | A decisão registrada e aplicada em um card com tela |
| Limpar a sessão a cada card | `/clear` ao fechar o card; `/handoff` e `/clear` para pausar no meio, nunca `/compact` | Só três cards fecharam assim. Por enquanto, o fluxo só pede o aviso "pode limpar a sessão" | Uma fatia inteira assim, sem perda de contexto |
| Quadro em outra ferramenta (ex.: Miro) | Um subagente que siga `docs/agents/quadro.md` em outra ferramenta | A origem não tem. Ela descartou o Miro porque uma tabela num canvas só imita o kanban | Um subagente escrito e rodando num projeto |
| Testes de observabilidade | Um teste que garante que logs e traces não levam dado pessoal (G3) e a máscara de documento e e-mail | É código da stack que a base ainda não traz; só o texto entrou em `stacks/spring/` | Um esqueleto de código da stack na base |
