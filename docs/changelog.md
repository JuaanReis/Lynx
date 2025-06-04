***LYNX - v1.0.2***

## Atualização

  - Novidades
    - Adição de proxy Tor
    - Header para disfarçar requisições
    - Novos payloads
    - Modo de execução (dev)
    - Bloqueio de hosts sensiveis

  - Remoções
    - Remoção de proxy do scanner de paths
    - Informações do sistema no menu
    - Pasta de IA

  - Correções
    - Modularização da ferramenta de XSS
    - Verificação de resposta do scanner de PATHS
    - Correção de verificação de portas do SMAP
    - Logs com extenção log

  - Em breve
    - Novos modulos (RCE, SQLi, Command injection)
    - Melhoria da UX e UI
    - Modulos em C
    - Modo DEV para facilitar a adição de novos modulos
    - Melhoria da estabilidade di LYNX
    - Reports em JSON
    - Integração de IA

# SMAP

  - Informações gerais do site
    - Headers, Cookies, CORS
    - Tecnologias do backend
    - Titulo, dominio
    - Verificação do certificado SSL
    - Portas
    - Formularios (tipos, valores, metodos)
    - Links (Internos e externos)
    - Checkagem de parametro

# XSS

  - Injeção de script em parametro

    - XSS refletido
      - Resultado local
      - Feito somente na pagina
      - Feito em parametros
      - Requisição com metodo GET
      - Verifica se o resultado esta em contexto perigoso

    - XSS armazenado
      - Resultado no servidor
      - Feito em formularios com metodo POST

# PATHS

  - Verificação de caminhos em uma URL
    - Injeta uma nova PATH na URL e verifica o resultado
    - Evita falsos positivos verificando o HTML