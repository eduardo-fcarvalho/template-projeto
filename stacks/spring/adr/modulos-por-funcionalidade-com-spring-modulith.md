# Módulos por funcionalidade, com camadas DDD internas verificadas pelo Spring Modulith

> Quanto maior o sistema, mais ela vale.

O backend é organizado em um pacote por conceito do domínio (ex.: `cliente`, `pedido`), com os mesmos nomes do `GLOSSARY.md`. Dentro de cada módulo há subpacotes no estilo DDD (`domain`, `application`, `infrastructure`, `web`). O pacote raiz de cada módulo é a sua API pública, e os subpacotes são internos. Como o Java não tem visibilidade de subpacote, quem garante essas fronteiras é um teste do Spring Modulith (`ApplicationModules.of(...).verify()`, num teste próprio), que roda no build e no CI.

## Considered Options

- **Por camada** (`controller/`, `service/`, `repository/`): obriga tudo a ser `public`, então um módulo consegue alterar os dados de outro pulando as regras dele (verificado com `javac` em 14/10/2026). Além disso, cada mudança se espalha por várias pastas.
- **Por funcionalidade, com módulos planos** (`package-private`): o compilador garante as fronteiras sem precisar de ferramenta, mas os módulos maiores ficariam sem organização interna.

## Consequences

- Um módulo só usa classes do pacote raiz de outro módulo. Importar algo de `outro.domain` ou `outro.infrastructure` faz o build falhar.
- Módulos novos entram como um novo pacote raiz, seguindo a mesma estrutura.
- Se um módulo um dia precisar virar um serviço separado, as fronteiras já estão prontas.
