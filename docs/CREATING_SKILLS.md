# Criando Skills

## Contrato

Crie `skills/<nome>/SKILL.md`, onde `<nome>` usa apenas letras minúsculas, números e hífens. O front matter contém somente:

```yaml
---
name: nome-da-skill
description: O que a Skill faz e em quais pedidos deve ser usada.
---
```

Mantenha o corpo curto, imperativo e orientado a decisões. Mova detalhes grandes para recursos referenciados diretamente. Não duplique conteúdo entre a Skill e os recursos.

## Registro

1. Adicione nome, alias único e papel a `config/skills.json`.
2. Selecione a Skill em um tipo de projeto somente quando ela mudar materialmente o resultado.
3. Gere `agents/openai.yaml` com os scripts oficiais do criador de Skills do ambiente.
4. Execute o validador oficial da Skill e `uv run aef validate`.
5. Adicione um caso de teste quando alterar regras de seleção ou validação.

## Critérios

- nome do diretório igual ao campo `name`;
- descrição contém função e gatilhos;
- alias único iniciado por `@`;
- responsabilidades e critério de aprovação explícitos nos planos;
- nenhuma credencial, dado sensível ou instrução de ação irreversível sem aprovação.

