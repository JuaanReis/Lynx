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
- **Brute Force**
- **Path Scanner**

## Usando o Bash da Raiz

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