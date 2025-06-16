# Como Usar o LYNX - Web Security Suite 2025

Este README é voltado para explicar como **utilizar o LYNX**, uma ferramenta de exploração de vulnerabilidades web.

## Pré-requisitos

1. **Python 3.x** instalado.
2. **Dependências**:
   - Se necessário, instale as dependências com o comando:
     ```bash
     pip install -r requirements.txt
     ```

## Estrutura do Projeto

A ferramenta contém scripts principais e um **bash** na pasta raiz, que serve para gerenciar os diferentes módulos da ferramenta.
Os módulos atuais incluem:

- **XSS Scanner**
- **Path Scanner**
- **Smap: scanner de informações**

## Usando o menu interativo

No diretório raiz do projeto, existe um arquivo bash chamado `lynx.sh` que facilita a execução de qualquer módulo. Para ver as opções de uso e as flags de cada módulo, basta rodar o seguinte comando:

```bash
./lynx
```

E depois roda:

```
--help
```

ou:

```
-h
```

## Usando pela linha de comando direta
Rodando pela raiz coloque
```
python3 dev.py (--Nome do modulo) (Comando para a ferramenta escolhido)
```
**Ex: python3 dev.py --path -u www.exemple.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug**

## Usos na pratica
  - XSS
    - Configurações gerais
      - (-T ou --type) tipo de ataque sendo armazenado ou refletido (Ex: -Tr tipo refletido ou -Ta para tipo armazenado)
      - (-l ou --limit) limite de payloads que a ferramenta vai usar (Ex: -l1000 ou --limit1000)
      - (-t ou --thread) quantidade de thread usado para o uso do ataque (Ex: -t30 ou --thread30)
      - (-d ou --debug) acionado para mais informações do ataque assim como quais payloads foram refletidos e em qual parametro (não requerido)

      - XSS refletido
        - (-u ou --url) Alvo do ataque (Ex: -u www.example.com/login?uid=10 ou --url www.exemple.com/login?uid=10) a url deve ter um parametro como visto acima (uid)

      - XSS armazenado
        - (-p ou --post) url na qual o payload será testado (Ex: -p www.example.com ou --post www.example.com)
        - (-v ou --view) url na qual o payload sera visível (Ex: -v www.example2.com ou --view www.example2.com)

    **Ex: -Tr -u www.exemple.com -l200 -t20 --debug**

  - Path
    - (-u ou --url) url alvo do ataque (Ex: -u www.example.com ou --url www.example.com)
    - (-w ou --wordlist) arquivo de payloads usados para o ataque (Ex: -w path.txt ou --wordlist path.txt  default=path.txt)
    - (-l) numero de payloads usados (Ex: -l 5000) max=5000 default=5000
    - (-t) numero de threads (Ex: -t20) default=10
    - (-s ou --status) numero status code que retorna true (Ex: -s 200 ou --status 200) default=200
    - (-d ou --delay) delay entre requisições (-d 0.3 0.5 ou --delay 0.3 0.5) defult=0.3 0.5
    - (-m ou --mode) modo de output (Ex: -m normal ou --mode normal) default=normal, option=[normal, debug]

    **Ex: -u www.exemple.com -w path.txt -l5000 -t60 -s 200 300 301 -d 0.2 0.4 -m debug**

  -Smap
    - (-u ou --url) alvo do ataque (-u www.example ou --url www.example.com)
    *Só isso, facil assim*
    **--url www.exemple.com**