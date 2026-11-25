# Skill selection guide · Catálogo de skills

Pick the row that matches your next decision. Open the skill for its activation criteria, inputs, worked prompt, expected output and stopping rule. Portuguese aliases are the same as English aliases. Copying an alias into a blank chat requires supplying its instructions first.

| What do you need? | Skill instructions | Entrega esperada |
|---|---|---|
| Prioritize several deliverables | [@Commander](../skills/commander/SKILL.md) | Mapa de dependências com responsável, prioridade e próxima decisão. |
| Plan one deliverable | [@EPO](../skills/elite-project-orchestrator/SKILL.md) | Team Plan com papéis, critérios de aceite e evidência esperada. |
| Assess methods and conclusions | [@Scientific](../skills/scientific/SKILL.md) | Parecer por afirmação com suporte, viés e limite de inferência. |
| Structure a publication | [@Editorial](../skills/editorial/SKILL.md) | Esqueleto de seções, alterações editoriais e verificações de leitura. |
| Design or review an application | [@Software](../skills/software/SKILL.md) | Decisão técnica, mudança verificável ou plano com critérios de teste. |
| Trace documentary evidence | [@Research](../skills/research/SKILL.md) | Tabela com fonte, data, trecho, interpretação e lacunas. |
| Communicate an evidenced benefit | [@Marketing](../skills/marketing/SKILL.md) | Mensagem com chamada para ação e registro das afirmações verificáveis. |
| Review a visual composition | [@Design](../skills/design/SKILL.md) | Direção visual, hierarquia e lista de verificações da peça. |
| Design a viability experiment | [@Business](../skills/business/SKILL.md) | Plano de experimento com métrica, custo e regra de decisão. |
| Map a repeatable workflow | [@Automation](../skills/automation/SKILL.md) | Fluxo com chave de deduplicação, limite de tentativas e recuperação. |
| Check evidence before acceptance | [@QA](../skills/quality-assurance/SKILL.md) | Matriz requisito, verificação, evidência, severidade e decisão. |

## Where responsibilities meet

Commander tracks decisions across projects. EPO builds the plan for one deliverable. Research traces claims to sources. Scientific judges whether the study design supports an inference. Editorial owns structure and wording, while Design checks composition and visual access. Business tests a value hypothesis before Marketing communicates the benefit. Software owns application behavior and Automation handles triggers, retries and external effects. QA records an independent decision against the acceptance criteria.

The CLI selects predefined teams for six project types. A specialist can also be selected manually from this table. Each skill has a directory-matched front matter name, a description with activation cues and an optional OpenAI interface descriptor. Host discovery and model adherence require separate validation.
