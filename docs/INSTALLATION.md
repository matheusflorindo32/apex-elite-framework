# Install and check the local CLI / Instalar e verificar a CLI

For a browser-only introduction, open the [English quick start](QUICK_START.md). Para usar o projeto pelo navegador, siga o [início rápido em português](QUICK_START.pt-BR.md).

## From a checkout / A partir do repositório

Install Python 3.11 or later and [uv](https://docs.astral.sh/uv/getting-started/installation/). Open a terminal in the repository directory containing `pyproject.toml`. The first sync downloads development and build dependencies.

Instale Python 3.11 ou posterior e o uv. Na pasta que contém `pyproject.toml`, execute os comandos abaixo. A primeira sincronização baixa as dependências de desenvolvimento e construção.

```bash
uv sync --locked --dev
uv run aef --version
uv run aef validate
uv run pytest
```

## Generate a plan / Gerar um plano

```bash
uv run aef brief new --type software
uv run aef plan --type software --request "Planejar aplicativo de leitura" --format json
uv run aef checklist --type software
```

Read the plan on screen. Add `--output plan.json` to the plan command to save it. Use a fresh filename to keep earlier work. The project types are `general`, `catalog`, `scientific`, `software`, `research` and `automation`.

Leia o plano na tela. Acrescente `--output plan.json` ao comando de plano para salvá-lo. Escolha um nome novo para preservar arquivos anteriores. Ao omitir o tipo, o roteamento depende das palavras-chave do catálogo.

## Troubleshooting / Solução de problemas

- **Command missing / comando ausente.** Run `uv --version`, reopen the terminal after installing uv and use `uv run aef` inside the checkout. Confirme a instalação do uv, reabra o terminal e use a pasta do projeto.
- **Unexpected team / equipe inesperada.** Specify the type with `--type`. Escolha o tipo explicitamente.
- **Validation finding / achado de validação.** Run `uv run aef validate --format json` and inspect the reported files. Examine os caminhos indicados e corrija as fontes antes de repetir o comando.

[CLI usage / Uso](USAGE.md) · [Contribution guide / Contribuição](../CONTRIBUTING.md)
