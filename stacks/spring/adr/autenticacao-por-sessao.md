# Autenticação por sessão com cookie, não JWT

> Reavalie no início do projeto: ela vale para um sistema com login próprio. Se vários sistemas precisarem da mesma identidade, ou se login com Google ou 2FA forem obrigatórios desde o começo, considere um provedor OIDC.

O login (e-mail e senha) cria uma sessão no servidor, guardada no banco via Spring Session JDBC. O navegador recebe só um cookie `HttpOnly`, `Secure` e `SameSite=Strict` emitido pelo host da API. Escolhemos sessão em vez de JWT porque a revogação é imediata (logout, bloqueio de um usuário, mudança de papel), porque é o comportamento nativo do Spring Security e porque é o padrão mais seguro para apps de navegador (o padrão BFF). O custo foi medido: cerca de 600 bytes por sessão e uma consulta desprezível perto de uma query ao banco.

O login e a dependência do Spring Session entram juntos, no primeiro card de login. Até lá, a configuração de segurança fecha tudo por padrão, responde 401 e mantém o CSRF ligado.

## Considered Options

- **JWT em cookie `HttpOnly`, endurecido** (access token curto + refresh token rotativo no banco): seguro, mas exige construir à mão login, renovação, rotação e revogação.
- **OAuth/OIDC com Keycloak ou SaaS, com o Spring como BFF:** traz recursos prontos (login com Google, 2FA, recuperação de senha), mas acrescenta um servidor ou fornecedor.
- **JWT acessível ao JavaScript** (`localStorage` ou memória): exposto a XSS.

## Consequences

Para que trocar de mecanismo no futuro (JWT, login com Google, Keycloak) continue barato:

- O código de negócio descobre quem está logado só por um componente próprio, que lê `Authentication#getName()`. Ele nunca usa `@AuthenticationPrincipal UserDetails` nem lê o token diretamente.
- Os papéis ficam no banco, não só na credencial.
- O usuário tem um id interno como chave primária. O e-mail é só o login, e identidades externas (ex.: Google) ficam numa tabela própria ligada ao usuário.
- As senhas usam `DelegatingPasswordEncoder`, que grava o hash com o prefixo do algoritmo.
- O front obtém "quem sou eu" por `GET /api/me` e concentra login e logout num único módulo. Ele nunca lê o conteúdo da credencial.
- A proteção CSRF continua obrigatória, porque o cookie vai automaticamente em toda requisição.
- Se as sessões começarem a pesar no banco, o armazenamento troca para Spring Session Redis sem mudar o login.
