"""Casos que passam e que devem ser barrados, com e sem agent_type.

Rode da raiz: python3 -m unittest discover -s scripts/guardrails
"""
import unittest

from guardrails import (
    conferencias_pr,
    motivo_comando,
    motivo_commit,
    motivo_ferramenta,
    motivo_mensagem,
    motivo_push,
)

RAIZ = "/repo"
ZERO = "0" * 40
A, B = "a" * 40, "b" * 40


class ComandoGlobal(unittest.TestCase):
    """Regras que valem para qualquer agente."""

    BARRADOS = [
        # G1: main e merge
        "git push origin main",
        "git push origin HEAD:main",
        "git push origin feature:refs/heads/main",
        "git push --all",
        "git push --mirror origin",
        "git push origin --delete main",
        "cd backend && git push origin main",
        "git -C /repo push origin main",
        "gh pr merge 12",
        "gh pr merge 12 --squash",
        "gh api -X PUT repos/dona/projeto/pulls/12/merge",
        "gh api repos/x/y/merges -f base=main -f head=xx-02",
        # G6: git destrutivo
        "git push --force",
        "git push -f origin xx-02",
        "git push -uf origin xx-02",
        "git push --force-with-lease origin xx-02",
        "git push origin +xx-02",
        "git reset --hard HEAD~1",
        "git branch -D xx-02",
        "git branch --delete --force xx-02",
        "git branch -df xx-02",
        "git clean -fd",
        "git clean --force",
        # G5: infraestrutura
        "ssh ubuntu@10.0.0.1",
        "scp app.jar ubuntu@10.0.0.1:/opt",
        "FOO=1 ssh vm",
        "sudo ssh vm",
        # G4: segredos por comando
        "cat .env",
        "less ./.env.local",
        "grep SENHA .env.producao",
        "source .env",
        "cp backend/.env /tmp/x",
        "cat ~/.ssh/id_ed25519",
        "ls ~/.ssh",
        # G10: pular os git hooks
        "git commit --no-verify -m 'x'",
        "git commit -n -m 'x'",
        "git commit -anm 'x'",
        "git push --no-verify origin xx-02",
        "git commit --no-verif -m x",
        "git show HEAD:.env",
        "git -c core.hooksPath=/dev/null commit -m 'x'",
        "git config core.hooksPath /dev/null",
        "git config --unset core.hooksPath",
        # G10: editar os guardrails por comando
        "sed -i 's/x/y/' scripts/guardrails/guardrails.py",
        "echo x > .githooks/pre-push",
        "echo '{}' >> .claude/settings.json",
        "echo '{\"disableAllHooks\": true}' > .claude/settings.local.json",
        "rm -rf scripts/guardrails",
        "mv .claude/hooks/a .claude/hooks/b",
        "tee .claude/settings.json",
        "chmod -x .githooks/pre-commit",
        "git checkout -- scripts/guardrails/guardrails.py",
        "git restore .githooks/pre-push",
        "python3 -c \"open('scripts/guardrails/guardrails.py','w')\"",
        "cat > /repo/scripts/guardrails/x.py <<'EOF'\nx\nEOF",
        # o que não dá para analisar não passa
        "echo 'aspa aberta",
    ]

    PASSAM = [
        "git push -u origin xx-02-guardrails",
        "git push origin xx-02-guardrails",
        "git push",
        "git push --dry-run origin xx-02",
        "git status",
        "git log --oneline main..HEAD",
        "git diff main",
        "git switch -c xx-02-guardrails",
        "git branch -d xx-02",
        "git clean -n",
        "git reset --soft HEAD~1",
        "git commit -m 'feat: x'",
        "git commit -m \"$(cat <<'EOF'\nfeat: lógica\n\ncorpo\nEOF\n)\"",
        "git config core.hooksPath .githooks",
        "git config core.hooksPath",
        "gh pr create --title x --body y",
        "gh pr view 12",
        "gh pr list --state open",
        "gh issue close 3",
        "cat .env.example",
        "cat scripts/guardrails/guardrails.py",
        "grep -n motivo scripts/guardrails/guardrails.py",
        "ls .githooks",
        "git diff -- scripts/guardrails",
        "git add scripts/guardrails .githooks",
        "python3 scripts/guardrails/guardrails.py claude",
        "python3 -m unittest discover -s scripts/guardrails",
        "sh .githooks/pre-commit",
        "echo ssh",
        "git commit -m 'feat: git hooks versionados em .githooks'",
        "git commit -m 'docs: o agente não lê o .env'",
        "gh pr create --title 'XX-02' --body 'muda scripts/guardrails e o .claude/settings.json'",
        "git grep motivo scripts/guardrails",
    ]

    def test_barrados(self):
        for comando in self.BARRADOS:
            with self.subTest(comando=comando):
                self.assertIsNotNone(motivo_comando(comando))

    def test_passam(self):
        for comando in self.PASSAM:
            with self.subTest(comando=comando):
                self.assertIsNone(motivo_comando(comando))

    def test_regras_globais_valem_para_subagente(self):
        for agente in ("implementador", "Explore", "general-purpose"):
            with self.subTest(agente=agente):
                self.assertIsNotNone(motivo_comando("git push --force", agente))
                self.assertIsNotNone(motivo_comando("cat .env", agente))


class ComandoPorSubagente(unittest.TestCase):
    """O que cada subagente pode rodar no Bash."""

    CASOS = {
        "po": (
            [
                "gh issue list",
                "gh issue view 6",
                "gh issue list --json number,title",
                "gh issue list --search 'updated:>2026-11-01'",
            ],
            [
                "gh issue close 3",
                "gh issue edit 6 --add-label x",
                "gh issue list && gh issue close 3",
                "gh issue list; gh issue close 3",
                "gh issue list || gh issue close 3",
                "gh issue list | sh",
                "gh issue view $(gh issue close 3)",
                "gh issue view `rm x`",
                "gh issue list > lista.txt",
                "gh issue view < x",
                "gh issue list\ngh issue close 3",
                "gh issue list & gh issue close 3",
                "python3 -c 'print(1)'",
                "git log",
            ],
        ),
        "quadro": (
            ["gh issue list --state all", "gh pr list", "gh issue list --json title --jq '.[] | .title'"],
            ["gh issue view 6", "gh pr merge 1", "gh pr list; ls"],
        ),
        "revisor-card": (
            ["git log --oneline main..HEAD", "git diff main...HEAD", "git show HEAD", "gh issue view 6"],
            ["git push", "git commit -m x", "gh issue list", "git diff | tee x", "grep -rn x docs/adr"],
        ),
        "revisor-regras": (
            ["git log main..HEAD", "git diff main", "git show HEAD:README.md", "gh issue view 6"],
            ["git checkout main", "gh issue comment 6 -b x"],
        ),
        "implementador": (
            ["./mvnw -B verify", "npm run build && npm test", "git status", "git diff", "git add -A"],
            [
                "git commit -m 'feat: x'",
                "cd backend && git commit -m x",
                "git push -u origin xx-02",
                "gh pr create --title x",
                "gh pr view 3",
                "git -C /repo commit -m x",
            ],
        ),
    }

    def test_listas(self):
        for agente, (passam, barrados) in self.CASOS.items():
            for comando in passam:
                with self.subTest(agente=agente, comando=comando, esperado="passa"):
                    self.assertIsNone(motivo_comando(comando, agente))
            for comando in barrados:
                with self.subTest(agente=agente, comando=comando, esperado="barrado"):
                    self.assertIsNotNone(motivo_comando(comando, agente))


class Ferramenta(unittest.TestCase):
    """A entrada do hook PreToolUse: o JSON que o Claude Code manda."""

    def payload(self, tool_name, tool_input, agente=None):
        p = {"tool_name": tool_name, "tool_input": tool_input, "cwd": RAIZ}
        if agente:
            p["agent_type"] = agente
        return p

    def test_edicao_dos_guardrails(self):
        for caminho in (
            "/repo/scripts/guardrails/guardrails.py",
            "/repo/.githooks/pre-push",
            "/repo/.claude/settings.json",
            "/repo/.claude/settings.local.json",
            "/repo/.claude/hooks/x.sh",
        ):
            for ferramenta in ("Edit", "Write", "MultiEdit"):
                with self.subTest(caminho=caminho, ferramenta=ferramenta):
                    self.assertIsNotNone(motivo_ferramenta(self.payload(ferramenta, {"file_path": caminho})))
        self.assertIsNotNone(
            motivo_ferramenta(self.payload("NotebookEdit", {"notebook_path": "/repo/.githooks/x.ipynb"}))
        )

    def test_edicao_livre(self):
        for caminho in ("/repo/README.md", "/repo/.claude/agents/po.md", "/repo/scripts/outro.py"):
            with self.subTest(caminho=caminho):
                self.assertIsNone(motivo_ferramenta(self.payload("Write", {"file_path": caminho})))

    def test_leitura_de_segredo(self):
        self.assertIsNotNone(motivo_ferramenta(self.payload("Read", {"file_path": "/repo/.env"})))
        self.assertIsNotNone(motivo_ferramenta(self.payload("Read", {"file_path": "/home/dev/.ssh/id_rsa"})))
        self.assertIsNone(motivo_ferramenta(self.payload("Read", {"file_path": "/repo/.env.example"})))
        self.assertIsNone(motivo_ferramenta(self.payload("Read", {"file_path": "/repo/scripts/guardrails/guardrails.py"})))
        self.assertIsNotNone(motivo_ferramenta(self.payload("Grep", {"pattern": ".", "path": "/repo/.env"})))
        self.assertIsNone(motivo_ferramenta(self.payload("Grep", {"pattern": "x", "path": "/repo/backend"})))

    def test_revisor_le_pelas_ferramentas(self):
        # o Bash do revisor é estreito; Read e Grep são o caminho para ler as ADRs
        self.assertIsNone(motivo_ferramenta(self.payload("Grep", {"pattern": "x", "path": "/repo/docs/adr"}, "revisor-regras")))
        self.assertIsNone(motivo_ferramenta(self.payload("Read", {"file_path": "/repo/AGENTS.md"}, "revisor-regras")))

    def test_bash_com_e_sem_agente(self):
        self.assertIsNone(motivo_ferramenta(self.payload("Bash", {"command": "gh issue close 3"})))
        self.assertIsNotNone(motivo_ferramenta(self.payload("Bash", {"command": "gh issue close 3"}, "po")))
        self.assertIsNotNone(motivo_ferramenta(self.payload("Bash", {"command": "gh pr merge 1"})))

    def test_quadro_nao_escreve_lista_nem_board(self):
        for nome in ("mcp__claude_ai_Trello__trelloWriteList", "mcp__claude_ai_Trello__trelloWriteBoard"):
            with self.subTest(nome=nome):
                self.assertIsNotNone(motivo_ferramenta(self.payload(nome, {}, "quadro")))
                self.assertIsNone(motivo_ferramenta(self.payload(nome, {})))
        self.assertIsNone(motivo_ferramenta(self.payload("mcp__claude_ai_Trello__trelloWriteCard", {}, "quadro")))


class Mensagem(unittest.TestCase):
    def test_atribuicao(self):
        self.assertIsNotNone(motivo_mensagem("feat: x\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n"))
        self.assertIsNotNone(motivo_mensagem("feat: x\n\nco-authored-by: alguém <a@b>\n"))
        self.assertIsNone(motivo_mensagem("feat: x\n\ncorpo\n# Co-Authored-By: comentário do git\n"))
        self.assertIsNone(motivo_mensagem("docs: explica o Co-Authored-By\n"))

    def test_formato(self):
        for texto in (
            "feat: tela de login\n",
            "docs: AGENTS.md núcleo\n\ncorpo com: dois pontos\n",
            "\n# comentário do git\nfix: corrige o hook\n",
            "Merge branch 'xx-02' into main\n",
            'Revert "feat: tela de login"\n',
            "fixup! feat: tela de login\n",
        ):
            with self.subTest(texto=texto):
                self.assertIsNone(motivo_mensagem(texto))
        for texto in (
            "ajusta o hook\n",
            "Feat: maiúscula\n",
            "feat:sem espaço\n",
            "feat(login): escopo fora do padrão\n",
            "feature: tipo que não existe\n",
            "feat: \n",
            "",
            "# só comentário\n",
        ):
            with self.subTest(texto=texto):
                self.assertIsNotNone(motivo_mensagem(texto))


class Push(unittest.TestCase):
    def ancestral(self, resposta):
        return lambda antigo, novo: resposta

    def test_main(self):
        self.assertIsNotNone(motivo_push([f"refs/heads/x {A} refs/heads/main {B}"], self.ancestral(True)))
        self.assertIsNotNone(motivo_push([f"(delete) {ZERO} refs/heads/main {B}"], self.ancestral(True)))

    def test_force(self):
        linha = f"refs/heads/xx-02 {A} refs/heads/xx-02 {B}"
        self.assertIsNotNone(motivo_push([linha], self.ancestral(False)))
        self.assertIsNotNone(motivo_push([linha], self.ancestral(None)))  # o remoto não existe aqui
        self.assertIsNone(motivo_push([linha], self.ancestral(True)))

    def test_branch_novo_e_apagado(self):
        self.assertIsNone(motivo_push([f"refs/heads/xx-02 {A} refs/heads/xx-02 {ZERO}"], self.ancestral(False)))
        self.assertIsNone(motivo_push([f"(delete) {ZERO} refs/heads/xx-02 {B}"], self.ancestral(False)))


class Commit(unittest.TestCase):
    PASTA = "db/migration/"
    MIGRACAO = "db/migration/V1__esquema_inicial.sql"

    def motivo(self, arquivos, conteudo="", migracoes=(PASTA,)):
        return motivo_commit(arquivos, lambda caminho: conteudo, migracoes)

    def test_barrados(self):
        for arquivos in (
            [("A", ".env")],
            [("A", "backend/.env.local")],
            [("A", "chave.pem")],
            [("A", "deploy/id_ed25519")],
            [("A", "dados/clientes.csv")],
            [("M", "docs/planilha.xlsx")],
            [("A", "dados.ods")],
            [("M", self.MIGRACAO)],
            [("D", self.MIGRACAO)],
            [("R100", self.MIGRACAO, "db/migration/V1__outro.sql")],
        ):
            with self.subTest(arquivos=arquivos):
                self.assertIsNotNone(self.motivo(arquivos))

    def test_chave_privada_no_conteudo(self):
        texto = "x\n-----BEGIN OPENSSH " + "PRIVATE KEY-----\nabc\n"  # em dois pedaços, senão o pre-commit barra este arquivo
        self.assertIsNotNone(self.motivo([("A", "config/qualquer.txt")], texto))

    def test_passam(self):
        for arquivos in (
            [("A", ".env.example")],
            [("M", "README.md")],
            [("A", "db/migration/V2__nova.sql")],
            [("D", "dados/velho.csv")],
            [("D", ".env")],
            [("A", "deploy/id_ed25519.pub")],
        ):
            with self.subTest(arquivos=arquivos):
                self.assertIsNone(self.motivo(arquivos))

    def test_sem_stack_migracao_nao_e_protegida(self):
        self.assertIsNone(self.motivo([("M", self.MIGRACAO)], migracoes=()))


class PullRequest(unittest.TestCase):
    CARD = "xx-03-guardrails-ci"
    ROTINA = [("M", "README.md"), ("M", "docs/versoes/v0.1.0-esqueleto-andante.md")]

    def niveis(self, arquivos, conteudo="", branch=CARD):
        # só os níveis, na ordem: o texto da mensagem pode mudar sem quebrar o teste
        return [nivel for nivel, _ in conferencias_pr(arquivos, lambda c: conteudo, branch, ("db/migration/",))]

    def test_migracao_alterada_falha(self):
        self.assertEqual(self.niveis([("M", "db/migration/V1__esquema_inicial.sql")] + self.ROTINA), ["error"])

    def test_restart_no_compose_falha(self):
        arquivos = [("M", "compose.yaml")] + self.ROTINA
        self.assertEqual(self.niveis(arquivos, "services:\n  db:\n    restart: always\n"), ["error"])
        self.assertEqual(self.niveis(arquivos, "services:\n  db:\n    image: postgres\n"), [])

    def test_dependencia_avisa(self):
        for caminho in ("backend/pom.xml", "frontend/package.json", "pyproject.toml", "go.mod"):
            with self.subTest(caminho=caminho):
                self.assertEqual(self.niveis([("M", caminho)] + self.ROTINA), ["warning"])

    def test_caminho_de_guardrail_avisa(self):
        for caminho in ("scripts/guardrails/guardrails.py", ".github/workflows/ci.yaml", ".gitignore"):
            with self.subTest(caminho=caminho):
                self.assertEqual(self.niveis([("M", caminho)] + self.ROTINA), ["warning"])

    def test_rotina_do_card(self):
        arquivos = [("M", "src/x.py")]
        self.assertEqual(self.niveis(arquivos), ["warning"])
        self.assertEqual(self.niveis(arquivos, branch="teste-x"), [])

    def test_pr_limpo_passa(self):
        self.assertEqual(self.niveis(self.ROTINA), [])


if __name__ == "__main__":
    unittest.main()
