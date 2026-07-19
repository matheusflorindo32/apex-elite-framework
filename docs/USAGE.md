# Uso

## Preparação

```bash
uv sync --dev
```

## Comandos

`uv run aef skills list` lista alias, nome nativo e descrição.

`uv run aef validate` retorna código `0` quando não há achados críticos ou altos. Use `--format json` para integração com CI.

`uv run aef brief new --type software --output brief.md` copia o template adequado e inclui o tipo no cabeçalho.

`uv run aef plan --type catalog --request "..." --output plan.md` gera equipe, justificativas, fases, riscos, critérios e condições de parada. Use `--format json` para saída estruturada.

`uv run aef checklist --type scientific` combina o checklist especializado com o universal.

`uv run aef audit --format markdown --output docs/audit.md` grava o relatório corrente.

## Fluxo recomendado

1. Gere o brief e preencha apenas dados verificados.
2. Gere o plano e revise a seleção de equipe.
3. Execute em incrementos com evidência.
4. Aplique checklists e corrija achados.
5. Gere auditoria Markdown e JSON.
6. Registre limitações e revisão humana necessária.

## Códigos de saída

- `0`: comando concluído ou auditoria aprovada;
- `1`: auditoria reprovada por achado crítico/alto;
- `2`: entrada, configuração ou raiz inválida.

