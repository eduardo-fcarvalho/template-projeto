"""A lógica dos guardrails, num lugar só. Os git hooks, o CI e o hook do Claude Code a chamam.

Cada função `motivo_*` devolve o motivo do bloqueio, ou None quando passa. Os números (G1…)
são os da tabela de guardrails do AGENTS.md; S1… são os de uma stack em stacks/.

Uso:
  guardrails.py claude          JSON do PreToolUse na stdin; sai com 2 se barrar
  guardrails.py commit-msg ARQ  mensagem do commit
  guardrails.py pre-commit      arquivos no stage
  guardrails.py pre-push        linhas do pre-push na stdin
  guardrails.py pr BASE BRANCH  conferências do PR; sai com 1 se alguma falhar

Limite: o modelo de ameaça é o agente que erra, não o que sabota. Um comando escondido em
`bash -c`, `eval`, um script ou um `cd` antes do caminho passa pela análise do comando.
"""
import json
import os
import re
import shlex
import subprocess
import sys

# Preenchidos pela stack em uso (ver stacks/<stack>/README.md). Vazios, as regras deles não valem.
MIGRACOES = ()  # S1: pastas de migrações já aplicadas, que não se editam

SEPARADORES = {";", "&", "&&", "|", "||", "\n", "(", ")"}
PREFIXOS = {"sudo", "env", "command", "time", "nohup", "exec"}

# G10
PROTEGIDO = re.compile(r"(^|/)(scripts/guardrails|\.githooks|\.claude/hooks)(/|$)|(^|/)\.claude/settings(\.local)?\.json$")
PROTEGIDO_NO_TEXTO = re.compile(r"(scripts/guardrails|\.githooks|\.claude/hooks|\.claude/settings(\.local)?\.json)")
LEITURA = {"cat", "head", "tail", "less", "more", "grep", "rg", "ls", "wc", "diff", "stat", "file"}
GIT_LEITURA = {"log", "diff", "show", "status", "blame", "add", "ls-files", "grep"}
# texto livre (mensagem de commit, corpo de PR) não é caminho: citar .env ou .githooks ali não lê nem edita nada
TEXTO = {"-m", "--message", "-b", "--body", "-t", "--title"}

# G4
SEGREDO = re.compile(r"(^|[/\s'\"=:])(\.env(?!\.example\b)(\.[\w.-]+)?|\.ssh)(/|$|[\s'\"])")

# Subagentes: nas listas com "só", qualquer encadeamento é recusado
SO = {
    "po": [["gh", "issue", "list"], ["gh", "issue", "view"]],
    "quadro": [["gh", "issue", "list"], ["gh", "pr", "list"]],
    "revisor-card": [["git", "log"], ["git", "diff"], ["git", "show"], ["gh", "issue", "view"]],
    "revisor-regras": [["git", "log"], ["git", "diff"], ["git", "show"], ["gh", "issue", "view"]],
}
SUBSTITUICAO = re.compile(r"`|\$\(")
QUADRO_SO_CARD = re.compile(r"trelloWrite(List|Board)$")  # stacks/quadro-trello

# Commits: o padrão `tipo: descrição` do AGENTS.md
FORMATO = re.compile(r"^(feat|fix|docs|refactor|test|chore|ci|build|perf): \S")
DO_GIT = re.compile(r"^(Merge |Revert \"|(fixup|squash|amend)! )")

PLANILHA = re.compile(r"\.(csv|xlsx?|ods)$", re.I)
CHAVE = re.compile(r"(^|/)(\.env(\.(?!example$)[\w.-]+)?|id_(rsa|ecdsa|ed25519|dsa)|[^/]+\.(pem|key|p12|pfx))$")
COMPOSE = re.compile(r"(^|/)(docker-)?compose(\.[\w-]+)?\.ya?ml$")
RESTART = re.compile(r"(?m)^\s*restart:")
DEPENDENCIA = re.compile(r"(^|/)(pom\.xml|build\.gradle(\.kts)?|package\.json|pyproject\.toml|requirements[\w.-]*\.txt|go\.mod|Cargo\.toml|Gemfile)$")
SINALIZADO = re.compile(r"^(\.github/workflows/|\.gitignore$)")
BRANCH_DE_CARD = re.compile(r"^[a-z]+-\d+-")


def segmentos(comando):
    """Divide o comando em comandos simples. Cada um volta com os alvos de redirecionamento à parte."""
    lex = shlex.shlex(comando, posix=True, punctuation_chars=";&|<>()\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    atual, alvos, saida = [], [], []
    tokens = list(lex)
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in SEPARADORES:
            saida.append((atual, alvos))
            atual, alvos = [], []
        elif set(t) <= set("<>&") and ("<" in t or ">" in t):
            if i + 1 < len(tokens) and tokens[i + 1] not in SEPARADORES:
                alvos.append(tokens[i + 1])
                i += 1
        else:
            atual.append(t)
        i += 1
    saida.append((atual, alvos))
    return [(s, a) for s, a in saida if s or a]


def sem_texto(tokens):
    if not tokens or os.path.basename(tokens[0]) not in ("git", "gh"):
        return tokens
    saida, pula = [], False
    for t in tokens:
        if not pula and t.split("=")[0] not in TEXTO:
            saida.append(t)
        pula = t in TEXTO
    return saida


def sem_prefixo(tokens):
    while tokens and (tokens[0] in PREFIXOS or re.match(r"^\w+=", tokens[0])):
        tokens = tokens[1:]
    return tokens


def git_partes(tokens):
    """git [opções globais] sub args -> (globais, sub, args)."""
    i, globais = 1, []
    while i < len(tokens) and tokens[i].startswith("-"):
        globais.append(tokens[i])
        if tokens[i] in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            globais.append(tokens[i + 1] if i + 1 < len(tokens) else "")
            i += 1
        i += 1
    sub = tokens[i] if i < len(tokens) else ""
    return globais, sub, tokens[i + 1 :]


def tem_curta(args, letra, com_valor=""):
    """Procura a opção curta `letra` em grupos como -uf, parando numa opção que leva valor."""
    for a in args:
        if a.startswith("-") and not a.startswith("--"):
            for c in a[1:]:
                if c == letra:
                    return True
                if c in com_valor:
                    break
    return False


def motivo_git(tokens):
    globais, sub, args = git_partes(tokens)
    tudo = globais + [sub] + args
    if any("core.hookspath" in t.lower() for t in tudo):
        if not (sub == "config" and args in (["core.hooksPath"], ["core.hooksPath", ".githooks"])):
            return "G10: não mude o core.hooksPath; os git hooks ficam em .githooks"
    if any(len(a) > 5 and "--no-verify".startswith(a) for a in args) or (sub == "commit" and tem_curta(args, "n", "mFCctS")):
        return "G10: não pule os git hooks (--no-verify)"
    if sub == "push":
        if "--force" in args or any(a.startswith("--force-with-lease") for a in args) or tem_curta(args, "f", "o"):
            return "G6: push --force é proibido"
        posicionais = [a for a in args if not a.startswith("-")]
        if any(p.startswith("+") for p in posicionais[1:]):
            return "G6: refspec com + é force push"
        alvos = [p.split(":")[-1] for p in posicionais[1:]]
        if "--all" in args or "--mirror" in args or any(a in ("main", "refs/heads/main") for a in alvos):
            return "G1: nada vai direto para a main; abra um PR"
    if sub == "reset" and "--hard" in args:
        return "G6: reset --hard é proibido"
    if sub == "branch":
        apaga = "--delete" in args or tem_curta(args, "d")
        forca = "--force" in args or tem_curta(args, "f")
        if tem_curta(args, "D") or (apaga and forca):
            return "G6: branch -D é proibido"
    if sub == "clean" and ("--force" in args or tem_curta(args, "f")):
        return "G6: git clean -f é proibido"
    return None


def motivo_gh(tokens):
    posicionais = [t for t in tokens[1:] if not t.startswith("-")]
    if posicionais[:2] == ["pr", "merge"]:
        return "G1: só o dono mescla"
    if posicionais[:1] == ["api"] and any("/merge" in t for t in tokens):
        return "G1: só o dono mescla"
    return None


def motivo_protegido(tokens, alvos):
    """G10: o agente lê os guardrails e os roda, mas não os muda."""
    if any(PROTEGIDO_NO_TEXTO.search(a) for a in alvos):
        return True
    if not any(PROTEGIDO_NO_TEXTO.search(t) for t in tokens):
        return False
    nome = os.path.basename(tokens[0])
    if nome in LEITURA:
        return False
    if nome == "git":
        _, sub, args = git_partes(tokens)
        return sub not in GIT_LEITURA and args != ["core.hooksPath", ".githooks"]
    if nome in ("python3", "python", "sh", "bash"):
        # rodar o script ou os testes; -c com o caminho no código, não
        return not (PROTEGIDO.search(tokens[1]) if len(tokens) > 1 else False) and tokens[1:3] != ["-m", "unittest"]
    return True


def motivo_comando(comando, agente=None):
    if agente in SO:
        try:
            partes = segmentos(comando)
        except ValueError:
            return "comando que o guardrail não consegue analisar"
        # o shlex separa os operadores fora das aspas; $( e crase rodam até dentro de aspas duplas
        if len(partes) != 1 or partes[0][1] or SUBSTITUICAO.search(comando):
            return f"Subagentes: o {agente} não encadeia comandos nem redireciona"
        tokens = partes[0][0]
        if not any(tokens[: len(p)] == p for p in SO[agente]):
            return f"Subagentes: o {agente} só roda " + ", ".join(" ".join(p) for p in SO[agente])

    try:
        partes = segmentos(comando)
    except ValueError:
        return "comando que o guardrail não consegue analisar (aspa sem par?)"
    for tokens, alvos in partes:
        tokens = sem_texto(sem_prefixo(tokens))
        if any(SEGREDO.search(t) for t in tokens + alvos):
            return "G4: o agente não lê segredos (.env, ~/.ssh)"
        if motivo_protegido(tokens, alvos):
            return "G10: os guardrails são do dono; ele os muda à mão, num PR próprio"
        if not tokens:
            continue
        nome = os.path.basename(tokens[0])
        if nome in ("ssh", "scp"):
            return "G5: a infraestrutura é do dono (skill wizard); o deploy é só pelo CI"
        motivo = motivo_git(tokens) if nome == "git" else motivo_gh(tokens) if nome == "gh" else None
        if motivo:
            return motivo
        if agente == "implementador":
            git_sub = git_partes(tokens)[1] if nome == "git" else None
            gh_sub = [t for t in tokens[1:] if not t.startswith("-")][:1] if nome == "gh" else None
            if git_sub in ("commit", "push") or gh_sub == ["pr"]:
                return "Subagentes: o implementador não faz commit, push nem PR"
    return None


def motivo_ferramenta(payload):
    nome = payload.get("tool_name", "")
    entrada = payload.get("tool_input") or {}
    agente = payload.get("agent_type")
    if nome == "Bash":
        return motivo_comando(entrada.get("command", ""), agente)
    caminho = entrada.get("file_path") or entrada.get("notebook_path") or ""
    if nome in ("Edit", "Write", "MultiEdit", "NotebookEdit") and PROTEGIDO.search(caminho):
        return "G10: os guardrails são do dono; ele os muda à mão, num PR próprio"
    if nome in ("Read", "Grep", "Glob") and SEGREDO.search(caminho or entrada.get("path") or ""):
        return "G4: o agente não lê segredos (.env, ~/.ssh)"
    if agente == "quadro" and QUADRO_SO_CARD.search(nome):
        return "Subagentes: o quadro só escreve cards"
    return None


def motivo_mensagem(texto):
    if re.search(r"(?im)^co-authored-by:", texto):
        return "Commits: a autoria é só de quem faz o commit; tire o Co-Authored-By"
    # a primeira linha que o git guarda: ele descarta as linhas em branco do começo e os comentários
    titulo = next((l for l in texto.splitlines() if l.strip() and not l.startswith("#")), "")
    if not (FORMATO.match(titulo) or DO_GIT.match(titulo)):
        return f"Commits: a mensagem segue o padrão `tipo: descrição` (tipos: feat, fix, docs, refactor, test, chore, ci, build, perf), e veio {titulo!r}"
    return None


def motivo_push(linhas, eh_ancestral):
    """eh_ancestral(antigo, novo) -> True, False, ou None se o git não conhece o antigo."""
    zero = "0" * 40
    for linha in linhas:
        if not linha.strip():
            continue
        _, novo, ref_remota, antigo = linha.split()
        if ref_remota == "refs/heads/main":
            return "G1: nada vai direto para a main; abra um PR"
        if novo != zero and antigo != zero:
            resposta = eh_ancestral(antigo, novo)
            if resposta is None:
                return "G6: o remoto tem commits que este clone não conhece; rode git fetch antes"
            if not resposta:
                return "G6: push --force é proibido"
    return None


def motivo_commit(arquivos, conteudo, migracoes=MIGRACOES):
    """arquivos: tuplas (status, caminho[, novo]) do `git diff --cached --name-status`."""
    for status, *caminhos in arquivos:
        caminho = caminhos[-1]
        if status[0] in "MDR" and migracoes and caminhos[0].startswith(migracoes):
            return "S1: migração aplicada não se edita; crie uma migração nova"
        if status[0] == "D":
            continue
        if CHAVE.search(caminho):
            return f"G4: {caminho} parece segredo"
        if PLANILHA.search(caminho):
            return f"G2: planilha ou CSV fora do Git ({caminho})"
        if re.search(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", conteudo(caminho)):
            return f"G4: {caminho} tem uma chave privada"
    return None


def conferencias_pr(arquivos, conteudo, branch, migracoes=MIGRACOES):
    """O que o CI confere num PR. Devolve pares (nível, mensagem): "error" falha o CI e "warning" só avisa."""
    achados = []
    motivo = motivo_commit(arquivos, conteudo, migracoes)
    if motivo:
        achados.append(("error", motivo))
    mudados = []
    for status, *caminhos in arquivos:
        caminho = caminhos[-1]
        mudados.extend(caminhos)
        if status[0] != "D" and COMPOSE.search(caminho) and RESTART.search(conteudo(caminho)):
            achados.append(("error", f"G9: {caminho} tem restart:; os contêineres sobem só para a tarefa"))
        if DEPENDENCIA.search(caminho):
            achados.append(("warning", f"G7: {caminho} mudou; ponha no PR o motivo da dependência"))
        if any(PROTEGIDO.search(c) or SINALIZADO.search(c) for c in caminhos):
            achados.append(("warning", f"G10: {caminho} é caminho de guardrail; confira quem mudou e por quê"))
    if BRANCH_DE_CARD.match(branch) and not ("README.md" in mudados and any(c.startswith("docs/versoes/") for c in mudados)):
        achados.append(("warning", "Fluxo, passo 8: o card muda o arquivo da fatia em docs/versoes/ e o Status do README.md"))
    return achados


def _git(*args):
    # errors="replace": um binário no stage (imagem, .jar) não pode derrubar o hook
    return subprocess.run(["git", *args], capture_output=True, text=True, errors="replace")


def _ancestral(antigo, novo):
    codigo = _git("merge-base", "--is-ancestor", antigo, novo).returncode
    return {0: True, 1: False}.get(codigo)


def _arquivos(*args):
    """As tuplas (status, caminho[, novo]) do `git diff --name-status -z`."""
    resultado = _git("diff", "--name-status", "-z", *args)
    if resultado.returncode != 0:
        # falhar fechado: uma base que não existe não pode virar "nada mudou"
        sys.exit(f"Barrado pelo guardrail. O git diff falhou: {resultado.stderr.strip()}")
    saida = resultado.stdout.split("\0")
    arquivos, i = [], 0
    while i < len(saida) - 1:
        n = 3 if saida[i][0] in "RC" else 2
        arquivos.append(tuple(saida[i : i + n]))
        i += n
    return arquivos


def main(argv):
    modo = argv[1] if len(argv) > 1 else ""
    if modo == "claude":
        motivo = motivo_ferramenta(json.load(sys.stdin))
    elif modo == "commit-msg":
        with open(argv[2], encoding="utf-8") as f:
            motivo = motivo_mensagem(f.read())
    elif modo == "pre-push":
        motivo = motivo_push(sys.stdin.read().splitlines(), _ancestral)
    elif modo == "pre-commit":
        motivo = motivo_commit(_arquivos("--cached"), lambda c: _git("show", f":{c}").stdout)
    elif modo == "pr":
        achados = conferencias_pr(_arquivos(f"{argv[2]}...HEAD"), lambda c: _git("show", f"HEAD:{c}").stdout, argv[3])
        for nivel, mensagem in achados:
            print(f"::{nivel}::{mensagem}")
        return 1 if any(nivel == "error" for nivel, _ in achados) else 0
    else:
        print(__doc__, file=sys.stderr)
        return 1
    if motivo:
        print(f"Barrado pelo guardrail. {motivo}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
