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

## Install the candidate wheel / Instalar a wheel candidata

Build the artifacts with `uv build` from the candidate checkout. Open a separate working directory, then create a virtual environment there. Replace the example wheel path with the path to the file built in `dist`.

Gere os artefatos com `uv build` no repositório da candidata. Abra uma pasta de trabalho separada e crie nela um ambiente virtual. Substitua o caminho de exemplo pelo caminho da wheel gerada em `dist`.

On Linux and macOS / No Linux e macOS

```bash
uv venv ambiente-aef
source ambiente-aef/bin/activate
uv pip install "/path/to/dist/apex_elite_framework-1.0.1rc1-py3-none-any.whl"
```

On Windows PowerShell / No PowerShell do Windows

```powershell
uv venv ambiente-aef
. .\ambiente-aef\Scripts\Activate.ps1
uv pip install "C:\path\to\dist\apex_elite_framework-1.0.1rc1-py3-none-any.whl"
```

In the activated environment / No ambiente ativado

```bash
aef --version
aef skills list
aef plan --type software --request "Planejar aplicativo de leitura" --format json --output plano.json
aef validate
```

The installed CLI uses local resources and runs offline. An installation from the source distribution (`.tar.gz`) also needs the build requirements to be available through uv. Keep project outputs outside the environments. To try a new build, install it in a separate environment and compare a generated plan. To roll back, reactivate the previous environment. For the 1.0.0 baseline, use its checkout as described in the [candidate release notes](RELEASE_CANDIDATE.md).

A CLI instalada usa recursos locais e funciona sem rede. A instalação pela distribuição de código-fonte (`.tar.gz`) também requer que o uv tenha acesso às dependências de build. Guarde os arquivos de projeto fora dos ambientes. Para testar outra build, instale-a em um ambiente separado e compare um plano gerado. Para voltar à versão anterior, reative o ambiente anterior. Para a base 1.0.0, use o respectivo repositório conforme as [notas da candidata](RELEASE_CANDIDATE.md).

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
- **Invalid input or configuration / entrada ou configuração inválida.** An input error exits with code `2`. Check the project type, root or output path in the error message and retry. If a custom root has validation findings, inspect them with `aef --root "path/to/root" validate --format json`. Um erro de entrada retorna código `2`. Confira o tipo de projeto, o diretório ou o caminho de saída indicado e repita o comando. Use o mesmo comando de validação para inspecionar os achados de uma raiz personalizada.

[CLI usage / Uso](USAGE.md) · [Contribution guide / Contribuição](../CONTRIBUTING.md)
