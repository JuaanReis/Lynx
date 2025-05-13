# LYNX - Web Security Suite 2025

**LYNX** é uma ferramenta de varredura e exploração de vulnerabilidades web feita para quem precisa de algo leve, rápido e funcional.
Voltada para entusiastas, estudantes e profissionais de segurança, ela foca no essencial: encontrar falhas comuns como XSS, caminhos expostos e senhas fracas — sem depender de soluções pesadas ou complicadas.

## Por que esse projeto existe?

A ideia do LYNX surgiu da necessidade de ferramentas que fossem diretas ao ponto. A maioria dos scanners ou são lentos, ou exigem configuração demais. O LYNX tenta resolver isso oferecendo um conjunto de utilitários simples, com foco em velocidade, clareza e controle manual.

O projeto começou com funções básicas de XSS e brute force, mas é planejado para ser modular, permitindo a adição de novos modos de ataque com o tempo.

## O que ele faz (por enquanto)?

- **XSS Scanner**
  Detecta e testa possíveis pontos vulneráveis a Cross-Site Scripting (refletido e armazenado).

- **Path Scanner**
  Faz varredura de diretórios e arquivos comuns expostos no servidor.

- **Brute Force**
  Testa credenciais em formulários de login simples usando listas de usuário/senha.

Essas funções são implementadas com base em técnicas clássicas usadas em testes manuais e automatizados, voltadas para aprendizado, labs e análises rápidas.

## Características

- **Menu interativo e feedback visual com progresso**
- **Código modular, fácil de modificar e expandir**
- **Escrito em Python com integração parcial em C para ganho de desempenho**

## 🤝 Quer ajudar?

Esse projeto ainda tá só começando e **toda ajuda é bem-vinda**.
Se você manja de Python, C, segurança web, design de interface ou só quer contribuir com ideias, **chega junto!**

Pode abrir issues, mandar sugestões, corrigir bugs ou criar novos módulos.
Tem um manual explicando como usar a ferramenta em [manual.md](docs/manual.md) — dá uma olhada lá antes de começar.

Bora fazer o LYNX crescer juntos!

## ⚠️ Importante

O LYNX é um projeto **não oficial**, feito para **fins educacionais e testes autorizados**.
**Não use em sistemas que você não tem permissão para testar.**
O autor **não se responsabiliza por qualquer uso indevido.**

## 📥 Clonar este repositório

```bash
git clone https://github.com/JuaanReis/Lynx.git
