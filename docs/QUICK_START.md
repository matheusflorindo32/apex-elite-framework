# Your first APEX plan

[Português](QUICK_START.pt-BR.md) · [Project overview](../README.md)

Imagine you have 30 minutes to teach students how to judge a source. Try planning the class with the project's delivery coordinator, called @EPO. Set aside 5–10 minutes to try it. All you need is a browser and a chat assistant that accepts text.

1. **Get the instructions.** Open the [coordinator skill](../skills/elite-project-orchestrator/SKILL.md). On GitHub, use **Copy raw file** or **Download raw file** in the file toolbar. The file is plain text. For all eleven skills together, download the [knowledge file](../bundles/APEX_CHATGPT_KNOWLEDGE.md) the same way.
2. **Give your chat the context.** Start a new conversation. Attach the downloaded file or paste the coordinator instructions. Copy the following request into the same conversation.

   > @EPO Plan a 30-minute class for first-year students on checking a source. Give me one learning objective, three timed activities and one way to check learning. Answer in English. Label any assumptions.

3. **Check the result.** Add the minutes and check that the closing activity actually measures the objective. If it asks students to memorize terminology, ask for an activity where they judge a source and explain their reasoning.

**Illustrative answer.** Objective: identify the author, date and supporting evidence for one claim. Spend 5 minutes examining a claim, 15 minutes comparing two source excerpts in pairs and 10 minutes writing an individual verdict. Collect the verdict and check whether it cites one detail from each excerpt. Assumption: the teacher supplies both excerpts.

## Choose your next task

| Profile | What to try | What to verify |
| --- | --- | --- |
| Student | Paste the [synthetic thesis prompt (Português)](RESEARCHERS.md#exercício-2--delimitar-um-tcc) with the @EPO and @Research instructions. | Every milestone has an output you can show. |
| Researcher | Paste the [synthetic article abstract (Português)](RESEARCHERS.md#exercício-1--revisar-a-conclusão-de-um-artigo) with the @Scientific instructions. | Trace each criticism to the supplied text. Mark missing details as unknown. |
| Developer | Follow the [installation guide](INSTALLATION.md) and run `uv run aef plan --type software --request "Plan an accessible reading diary"`. | Run the project's checks and review the plan before implementation. |
| Teacher | Paste the [@Editorial instructions](../skills/editorial/SKILL.md) and your lesson outline. Ask for a student handout. | Compare the exercise with the objective. |

## Observe a first-time user

Ask someone new to APEX to start at the README and try the three steps above without coaching. Allow 5–10 minutes and start timing when they open the README. Count a success when they find the skill, submit the prompt and check that the activities total 30 minutes and that the final activity measures the objective. Record elapsed time, last step reached, confusion, requested help and outcome. If time runs out, record where they stopped. The range is a session budget. Actual time still needs to be observed with beginners.

## Common questions

**What if the assistant ignores @EPO?** Paste the coordinator instructions and explicitly ask it to follow them. The alias is a label in this project. Other specialties are listed in the [skill catalog](SKILLS.md).

**What if uploads are unavailable?** Copy the text of one skill into the conversation. Long knowledge files may exceed a host's context limit.

**Can it retrieve scientific references?** APEX organizes the review. Supply verified sources and check each citation yourself. [Research guide](RESEARCHERS.md)

**Will I get the same wording?** Chat responses vary. For repeatable local planning with a fixed catalog and input, use the CLI.
