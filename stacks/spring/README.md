# Stack: Spring Boot com SPA React

Para uma API Spring Boot com banco versionado pelo Flyway e uma SPA React que usa tipos gerados do contrato OpenAPI. Opcional: só vale se o `AGENTS.md` disser `Stacks em uso: spring`.

## Usar

1. No `AGENTS.md`, ponha `Stacks em uso: spring` e preencha a seção "Comandos": `./mvnw -B verify` no `backend/`, `npm run lint` e `npm run build` no `frontend/`.
2. Em `scripts/guardrails/guardrails.py`, ponha a pasta das migrações em `MIGRACOES`, como `("backend/src/main/resources/db/migration/",)`. Faça isso à mão: o arquivo é protegido pelo G10.
3. Cole os jobs de `ci-jobs.yaml` sob `jobs:` em `.github/workflows/ci.yaml`.
4. Copie as ADRs de `adr/` que valerem para o projeto para `docs/adr/`, com o próximo número livre.
5. Acrescente ao `.gitignore`: `target/`, `*.class`, `hs_err_pid*`, `node_modules/`, `dist/`, `coverage/` e `*.tsbuildinfo`.

## Guardrails da stack

Valem junto com os do `AGENTS.md`.

| # | Guardrail | Quem garante |
|---|---|---|
| S1 | Migração do Flyway já aplicada se corrige com uma migração nova | pre-commit e CI, pela `MIGRACOES` |
| S2 | A API continua compatível com a versão anterior do front: uma aba aberta guarda o front antigo | CI (contrato e tipos em dia) e `revisor-regras` |

## Privacidade nos logs (G3)

- Para identificar alguém num log, use o id interno da pessoa.
- Se o documento ou o e-mail ajudarem a investigar, passe-os por uma função de máscara do projeto.
- Senha e token não aparecem nem mascarados.
- Os valores das consultas SQL e as query strings ficam fora dos traces, e um teste garante isso. Sem o `datasource-micrometer-opentelemetry`, os literais do SQL vão inteiros para o trace (ver `armadilhas.md`).

## Definição de Pronto, a mais

- [ ] A verificação dos módulos do Spring Modulith passa no CI (ADR de módulos por funcionalidade).
- [ ] Mudanças na API continuam compatíveis com a versão anterior do front, e os tipos foram regenerados (S2).

## Arquivos

- `adr/autenticacao-por-sessao.md`: sessão com cookie em vez de JWT.
- `adr/modulos-por-funcionalidade-com-spring-modulith.md`: um pacote por conceito do domínio, com as fronteiras verificadas no build.
- `armadilhas.md`: fatos conferidos de Spring, testes, observabilidade, Postgres e contrato.
- `ci-jobs.yaml`: os jobs `backend` e `frontend`.
