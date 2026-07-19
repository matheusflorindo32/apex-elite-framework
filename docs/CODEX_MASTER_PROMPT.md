# PROMPT MESTRE PARA O CODEX

Você está dentro do repositório **Apex Elite Framework**.

Sua missão é transformar este scaffold em um framework funcional, profissional, versionado, testável e reutilizável para orquestração de projetos com múltiplas skills.

## Objetivo principal

Concluir a implementação de um sistema em que o usuário possa iniciar uma tarefa com:

`@Commander` para projetos longos e múltiplas frentes;

ou:

`@EPO` para uma tarefa específica.

O sistema deve analisar o pedido, escolher as skills necessárias, produzir um plano estruturado, executar ou preparar a execução, fazer revisão cruzada e aplicar QA.

## Regras obrigatórias

1. Leia integralmente `AGENTS.md`, todas as skills, templates, workflows, checklists e schemas.
2. Não apague conteúdo útil sem justificar.
3. Preserve o português do Brasil como idioma padrão.
4. Torne os arquivos compatíveis com uso em Codex e facilmente adaptáveis a Claude, Gemini e ChatGPT.
5. Não crie uma lista decorativa de agentes. Cada papel precisa de responsabilidade e critério de aprovação.
6. Implemente controle de loop com condição de parada.
7. Crie validação automática da estrutura do repositório.
8. Crie testes para:
   - front matter das skills;
   - aliases únicos;
   - links internos;
   - arquivos obrigatórios;
   - schema JSON;
   - exemplos.
9. Adicione exemplos completos:
   - catálogo comercial premium;
   - revisão científica;
   - projeto de software;
   - pesquisa documental;
   - automação.
10. Crie um CLI local simples, sem dependência de API, que:
   - liste skills;
   - valide o framework;
   - gere um novo project brief;
   - gere um plano inicial baseado em um tipo de projeto escolhido;
   - mostre os checklists aplicáveis.
11. Preferir Python 3.11+ com `uv` e `pyproject.toml`.
12. Não exigir chave de API para validar ou usar a versão documental.
13. Caso adicione integração opcional com OpenAI Agents SDK, isole-a em `integrations/openai_agents/`, documente `OPENAI_API_KEY` apenas como variável de ambiente e não coloque segredos.
14. Adicione CI para validação e testes.
15. Adicione `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`, `.gitignore` e documentação de versionamento.
16. Crie `docs/ARCHITECTURE.md`, `docs/USAGE.md`, `docs/CREATING_SKILLS.md` e `docs/QUALITY_MODEL.md`.
17. Acrescente um modelo de severidade de erros: crítico, alto, médio, baixo e informativo.
18. Crie relatório de auditoria em Markdown e JSON.
19. Rode os testes e registre os resultados.
20. Não declare conclusão se houver falhas.

## Estrutura funcional desejada

- Loader de skills.
- Validador de front matter.
- Catálogo de skills.
- Seletor simples por tipo de projeto e palavras-chave.
- Gerador de Team Plan.
- Gerador de Project Brief.
- Mecanismo de checklist.
- Controle de iterações.
- Relatório de auditoria.
- CLI.
- Testes.
- Documentação.
- Exemplos.

## Comandos desejados

Planeje comandos equivalentes a:

```bash
uv run aef skills list
uv run aef validate
uv run aef brief new --type catalog
uv run aef plan --type catalog --output plan.md
uv run aef checklist --type catalog
uv run pytest
```

## Critérios de aceite

O trabalho só está concluído quando:

- todos os testes passam;
- `aef validate` retorna sucesso;
- a documentação permite uso sem contexto externo;
- há pelo menos cinco exemplos;
- o framework detecta aliases duplicados e arquivos inválidos;
- o plano gerado contém equipe, justificativas, fases, riscos e critérios de aceite;
- o controle de loop possui condição de parada;
- não existem links internos quebrados;
- o repositório pode ser iniciado com comandos reproduzíveis;
- a entrega final lista arquivos criados, testes executados, resultados e pendências.

## Sequência de trabalho

1. Inspecione o scaffold.
2. Produza um plano curto.
3. Implemente o núcleo documental e o CLI.
4. Adicione validação.
5. Adicione testes.
6. Adicione exemplos.
7. Adicione documentação.
8. Execute QA.
9. Corrija falhas.
10. Entregue relatório final.

Comece agora. Não peça confirmação para decisões reversíveis. Para decisões irreversíveis, destrutivas, de publicação ou que envolvam credenciais, pare e solicite aprovação.
