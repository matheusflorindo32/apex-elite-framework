# Apex Elite Framework

Framework local, modular e sem dependência de API para planejar, revisar e auditar projetos complexos com Skills especializadas e critérios verificáveis.

## O que está pronto

- catálogo validável com 11 Skills e aliases como `@Commander`, `@EPO` e `@QA`;
- seleção determinística de equipe para catálogo, ciência, software, pesquisa e automação;
- CLI `aef` para listar Skills, gerar briefs, planos, checklists e auditorias;
- controle de iteração com orçamento e condição de parada;
- auditoria em Markdown e JSON;
- cinco exemplos completos, templates, checklists e documentação;
- kit prático de referências visuais para prompts, com seleção por tipo de projeto;
- testes automatizados e GitHub Actions;
- licença Apache-2.0.

## Instalação local

Requer Python 3.11+ e [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync --dev
uv run aef validate
uv run pytest
```

Nenhuma chave de API é necessária. O AEF grava arquivos somente quando `--output` é informado.

## Uso rápido

```bash
uv run aef skills list
uv run aef brief new --type catalog --output brief.md
uv run aef plan --type catalog --request "Criar catálogo comercial" --output plan.md
uv run aef checklist --type catalog
uv run aef audit --format json --output audit.json
```

Tipos disponíveis: `general`, `catalog`, `scientific`, `software`, `research` e `automation`. Sem `--type`, o comando `plan` pode classificar o pedido por palavras-chave e usa `general` quando não há sinal suficiente.

Em conversas, os aliases documentais continuam simples:

```text
@EPO Analise esta entrega, selecione a equipe necessária e aplique QA.
@Commander Coordene este projeto, registre decisões e acione o @EPO por entrega.
```

Em ambientes com Skills nativas do Codex, use `$elite-project-orchestrator` ou `$commander`.

## Uso no ChatGPT

O repositório inclui instruções próprias para um GPT personalizado e um exportador determinístico de conhecimento:

```bash
uv run python scripts/export_chatgpt_knowledge.py --output apex-chatgpt-knowledge.md
```

No editor de GPTs do ChatGPT, use `chatgpt/INSTRUCTIONS.md` no campo de instruções e carregue o arquivo gerado como conhecimento. Depois de salvar o GPT com o nome `APEX EPO`, ele pode ser chamado no ChatGPT Web digitando `@` e selecionando o GPT. Os aliases internos `@EPO`, `@Commander` e especialistas são interpretados pelas instruções do AEF.

## Direção visual e prompts

Para sites, carrosséis, apresentações, infográficos, thumbnails, identidade visual e materiais científicos, use o [Kit Prático de Referências Visuais para Prompts](docs/VISUAL_PROMPT_KIT.md). Ele inclui:

- seletor de ferramentas por tipo de projeto;
- Prompt-Mestre Premium Elite;
- comandos curtos como `/SITE`, `/CARROSSEL`, `/CIENTÍFICO` e `/AUDITORIA`;
- regras de acessibilidade, consistência e prevenção de cópia;
- combinações recomendadas para projetos científicos, táticos, premium e redes sociais.

## Arquitetura

- `src/aef/`: CLI, catálogo, planejamento, loop e validação;
- `config/`: aliases, tipos de projeto, equipes e critérios;
- `skills/`: instruções modulares com metadados nativos;
- `templates/`, `checklists/` e `workflows/`: recursos reutilizáveis;
- `schemas/`: contratos de saída;
- `tests/`: testes unitários, estruturais e de CLI;
- `docs/`: arquitetura, uso, criação de Skills, modelo de qualidade e direção visual.

Leia [Arquitetura](docs/ARCHITECTURE.md), [Uso](docs/USAGE.md), [Criação de Skills](docs/CREATING_SKILLS.md), [Modelo de qualidade](docs/QUALITY_MODEL.md), [Kit Visual](docs/VISUAL_PROMPT_KIT.md) e [Versionamento](docs/VERSIONING.md).

## Garantias e limites

O CLI prepara e valida planos; ele não executa ações externas nem substitui julgamento profissional. Seleção por palavras-chave é deliberadamente simples, transparente e local. Projetos de alto risco exigem revisão humana e ferramentas específicas do domínio.

## Licença

Apache License 2.0. Consulte [LICENSE](LICENSE).

Falhas de segurança devem seguir [SECURITY.md](SECURITY.md), sem exposição pública prematura.
