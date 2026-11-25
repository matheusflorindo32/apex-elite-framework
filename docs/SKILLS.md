# Skill selection guide · Catálogo de skills

Pick the row that matches your next decision. Open the skill for its activation criteria, inputs, worked prompt, expected output and stopping rule. The aliases work as labels in both languages. In a new chat, supply the skill instructions before using its alias.

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

| Ambiguous request | Start with | Add another skill when |
|---|---|---|
| “Check the conclusion and citations in this article.” | @Research when you need to find the passage backing a claim. | @Scientific when a study's design or data must justify an inference. @QA checks the revised conclusion against the original evidence and acceptance criteria. |
| “Help me finish my thesis and teaching project.” | @Commander when dates or dependencies need coordination across workstreams. | @EPO when one deliverable needs its own plan, such as narrowing the thesis to a question the available documents can answer. |
| “Revise this handout before class.” | @Editorial when structure, wording or hierarchy needs work. | @Design when composition, spacing or legibility in the intended format needs a visual review. |
| “Validate and announce the service.” | @Business when demand, costs or the viability threshold are still open. | @Marketing when evidence is available and the next task is to explain the benefit to an audience. |
| “Build a form that sends an email.” | @Software for form behavior, validation and tests. | @Automation when triggers, retries or duplicate sends affect the external workflow. |

For a single acceptance decision, give @QA the stated criteria, artifact and evidence. [Article and thesis exercises (Português)](RESEARCHERS.md) · [Quick start](QUICK_START.md)

The CLI selects predefined teams for six project types. A specialist can also be selected manually from this table. Each skill has a directory-matched front matter name, a description with activation cues and an optional OpenAI interface descriptor. Host discovery and model adherence require separate validation.
