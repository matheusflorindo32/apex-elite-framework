# Contribuindo

## Fluxo

1. Crie uma branch focada.
2. Preserve compatibilidade com Python 3.11+.
3. Evite dependências quando a biblioteca padrão for suficiente.
4. Atualize documentação, exemplos e `CHANGELOG.md` quando o comportamento mudar.
5. Execute:

```bash
uv sync --dev
uv run aef validate
uv run pytest
git diff --check
```

## Commits e revisão

Use Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`). Uma Pull Request deve explicar motivação, riscos, validações e limitações. Não inclua segredos, dados pessoais ou exemplos apresentados como fatos reais.

## Skills

Siga [docs/CREATING_SKILLS.md](docs/CREATING_SKILLS.md). Toda Skill precisa de front matter mínimo, diretório com o mesmo nome, registro único em `config/skills.json` e `agents/openai.yaml` coerente.

