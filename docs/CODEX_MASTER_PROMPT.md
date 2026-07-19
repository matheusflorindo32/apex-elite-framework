# Prompt mestre para operar e evoluir o AEF

Você está dentro do repositório Apex Elite Framework.

Leia integralmente `AGENTS.md`, o `SKILL.md` do orquestrador e somente as Skills, templates e checklists aplicáveis à tarefa atual. Preserve a arquitetura local, sem dependência obrigatória de API.

## Para executar uma tarefa

1. Preencha o brief do tipo adequado.
2. Gere um Team Plan com `uv run aef plan`.
3. Selecione apenas papéis que alterem materialmente o resultado.
4. Registre justificativa, responsabilidade e critério de aprovação por papel.
5. Execute em incrementos verificáveis e reversíveis.
6. Faça revisão cruzada e aplique os checklists.
7. Corrija achados e respeite as condições de parada.
8. Entregue artefatos, evidências, limitações, riscos e próxima ação.

## Para alterar o framework

- Inspecione Git, documentação, configuração e testes antes de editar.
- Preserve compatibilidade, salvo mudança major documentada.
- Use front matter de Skill somente com `name` e `description`.
- Mantenha aliases únicos em `config/skills.json`.
- Não adicione dependência sem justificar necessidade e risco.
- Não exponha segredos nem adicione integração remota obrigatória.
- Atualize testes, documentação, exemplos, versão e changelog conforme o impacto.

## Gate obrigatório

```bash
uv sync --locked --dev
uv run aef validate
uv run pytest
uv build
git diff --check
```

Não declare conclusão com achados críticos/altos, teste falhando ou validação não executada. Diferencie claramente validação automatizada, inspeção manual e confirmação do usuário.
