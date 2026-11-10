# Armadilhas conferidas

Cada item foi reproduzido num projeto real, no Spring Boot 4.1 e nas versões fixadas em 16/10/2026. Numa versão nova, confira de novo antes de confiar.

**Spring e testes**

- O bean de CORS precisa se chamar `corsConfigurationSource`. Com outro nome, o Spring Security não o encontra e nenhum cabeçalho de CORS sai.
- O usuário de teste do Spring Boot escreve a senha gerada no log. Desligue-o logo no esqueleto.
- Um `src/test/resources/application.yaml` esconde o `application.yaml` principal, porque os dois têm o mesmo nome no classpath. Configuração de teste vai em `properties` do `@SpringBootTest` ou num arquivo com outro nome.
- O Maven não apaga do `target/` um arquivo que sumiu do `src/`. Configuração que "não pega": rode `./mvnw clean` antes de desconfiar do código.
- Para apontar o SMTP do Mailpit, use `@DynamicPropertySource`. Com um `DynamicPropertyRegistrar` (um bean), o `JavaMailSender` não é criado, porque a condição `spring.mail.host` é avaliada antes de os beans existirem.
- `@MockitoBean`, `@TestPropertySource` ou `@Import` numa subclasse da base de testes sobem outra aplicação Spring e deixam a suíte lenta. A base existe para que todos os testes usem o mesmo contexto.
- Com o `spring-boot-starter-mail` e `spring.mail.host` definido, o health check passa a conferir o SMTP: com o SMTP fora, o `/actuator/health` responde `503`.

**Observabilidade**

- Sem o `datasource-micrometer-opentelemetry`, os literais escritos no SQL (um e-mail, por exemplo) vão inteiros para o trace.
- O appender de logs do OpenTelemetry só existe em versão alfa, presa à versão da API OTel que o Boot fixa. Uma versão mais nova chama métodos que não existem.
- Sem um coletor ligado, o envio de métricas tenta `localhost:4318` a cada minuto e enche o log de `WARN`. Deixe o envio desligado fora do profile de observabilidade.
- A amostragem padrão de traces é 1 a cada 10. No desenvolvimento, use `1.0`.
- O `grafana/otel-lgtm` usa cerca de 1,4 GiB de memória. Ele fica atrás de um profile, e o `docker compose down` sem `--profile '*'` o deixa ligado.

**Ambiente e infraestrutura**

- A partir do PostgreSQL 18, a imagem guarda os dados em `/var/lib/postgresql/18/docker`. O volume vai em `/var/lib/postgresql`, não mais em `/var/lib/postgresql/data`.
- A porta 5432 costuma estar ocupada por outro PostgreSQL local. Publique o banco do compose em outra porta, como a 5433.
- Fixe as versões das imagens do compose e use as mesmas no Testcontainers.
- No plano Free com repositório privado, o GitHub não deixa exigir o CI verde para o merge (a proteção de branch responde 403).

**Contrato e front**

- O contrato OpenAPI só fica estável no Git com as chaves em ordem (`writer-with-order-by-keys`) e sem o campo `servers`, que muda a cada execução.
- O `openapi-typescript` 7.13 declarava aceitar só o TypeScript 5. Um `overrides` no `package.json` resolve sem desligar a verificação de todos os pacotes, como faria o `--legacy-peer-deps`.
- O `VITE_API_URL` é escrito dentro do JavaScript no build: nunca é segredo, e cada ambiente precisa do próprio build.
- Uma SPA precisa que a hospedagem devolva o `index.html` para qualquer endereço. Sem isso, um link compartilhado dá 404.
- O front em cache pode estar numa versão anterior à da API. Mudanças na API precisam continuar compatíveis com o front anterior.

