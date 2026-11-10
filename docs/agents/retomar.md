# Retomar o projeto numa sessão nova

Só leia e relate. Comece um card só depois que o dono escolher.

1. Leia a seção "Status" do `README.md`: a fatia atual, o último card entregue e o próximo.
2. Rode `gh pr list --state open`. Um PR aberto aguarda a leitura do dono: avise, com o link.
3. Confira se os papéis da tabela "Subagentes" do `AGENTS.md` estão disponíveis nesta sessão. O `quadro` só conta se houver quadro. No Claude Code, eles são os arquivos de `.claude/agents/`.
   - Se o arquivo de um deles não existe, avise que ele sumiu.
   - Se o arquivo existe e o subagente não aparece, peça ao dono para reiniciar o agente: a pasta pode ter sido criada depois do início da sessão.
4. Rode `gh issue list --search "is:open -is:blocked" --json number,title,labels,milestone,assignees`.

Responda com três coisas e termine perguntando qual card o dono quer:

- o ponto em que o trabalho parou;
- a fatia atual;
- os cards desbloqueados, com o card em Fazendo primeiro.
