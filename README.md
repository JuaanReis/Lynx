# LYNX - Web Security Suite 2025

**LYNX** é uma ferramenta de varredura e exploração de vulnerabilidades web feita para quem precisa de algo leve, rápido e funcional.
Voltada para entusiastas, estudantes e profissionais de segurança, ela foca no essencial: encontrar falhas comuns como XSS, caminhos expostos e senhas fracas — sem depender de soluções pesadas ou complicadas.

## Por que esse projeto existe?

A ideia do LYNX surgiu da necessidade de ferramentas que fossem diretas ao ponto. A maioria dos scanners exigem configuração demais. O LYNX tenta resolver isso oferecendo um conjunto de utilitários simples, com foco em clareza e controle manual.

O projeto começou com funções básicas de XSS e scan de headers, mas é planejado para ser modular, permitindo a adição de novos modos de ataque com o tempo.

## O que ele faz (por enquanto)?

- **XSS Scanner**
  Detecta e testa possíveis pontos vulneráveis a Cross-Site Scripting (refletido e armazenado).

- **Path Scanner**
  Faz varredura de diretórios e arquivos comuns expostos no servidor.

<<<<<<< HEAD
- **Scanner de informações (Smap)**
  Pega informações de um site com uma URL, pegando headers, Cors, informações de cookies, portas, formulários, informações de backend 
=======
- **Smap**
  Puxa dados completo de um site através da URL assim como:
    - Headers
    - IP (v4 e v6)
    - Cookies
    - Formularios
    - Links
    - Portas abertas
    - Tecnologia do backend
>>>>>>> ad1f80f (mudança na arvore de arquivos)

Essas funções são implementadas com base em técnicas clássicas usadas em testes manuais e automatizados, voltadas para aprendizado, labs e análises rápidas.

## Características

- **Menu interativo e feedback visual com progresso**
- **Código modular, fácil de modificar e expandir**

## Quer ajudar?

Esse projeto ainda tá só começando e **toda ajuda é bem-vinda**.
Se você manja de Python, C, segurança web, design de interface ou só quer contribuir com ideias, **chega junto!**

Pode abrir issues, mandar sugestões, corrigir bugs ou criar novos módulos.
Tem um manual explicando como usar a ferramenta em [manual.md](docs/manual.md) — dá uma olhada lá antes de começar.

Bora fazer o LYNX crescer juntos!

## Importante

O LYNX é um projeto **não oficial**, feito para **fins educacionais e testes autorizados**.
**Não use em sistemas que você não tem permissão para testar.**
O autor **não se responsabiliza por qualquer uso indevido.**

## Clonar este repositório

```bash
git clone https://github.com/JuaanReis/Lynx.git
