# Documentação do domínio

Como as skills de engenharia devem usar a documentação do domínio ao explorar o projeto.

## Antes de explorar, leia

- **`GLOSSARY.md`** na raiz: o glossário do projeto.
- **`docs/adr/`**: as ADRs que tocam a área em que você vai trabalhar.

Se algum desses arquivos não existir, **siga em silêncio**: não aponte a ausência nem sugira criá-los. O `/domain-modeling` (usado pelo `/grill-with-docs` e pelo `/improve-codebase-architecture`) cria esses arquivos quando um termo ou uma decisão é resolvido.

## Estrutura (single-context)

```
/
├── GLOSSARY.md
└── docs/adr/
    ├── 0001-titulo-curto.md
    └── ...
```

## Use o vocabulário do glossário

Quando o seu texto citar um conceito do domínio (título de issue, proposta de refatoração, hipótese, nome de teste), use o termo como está definido no `GLOSSARY.md`. Não troque por sinônimos que o glossário manda evitar (ex.: se o glossário diz "Cliente" e manda evitar "comprador", nunca escreva "comprador").

Se o conceito que você precisa ainda não está no glossário, isso é um sinal: ou você está inventando uma linguagem que o projeto não usa (reconsidere), ou existe uma lacuna real (anote para o `/domain-modeling`).

## Aponte conflitos com ADRs

Se o seu texto contradiz uma ADR existente, diga isso explicitamente em vez de passar por cima dela:

> _Contradiz a ADR-0001 (título), mas vale reabrir porque…_
