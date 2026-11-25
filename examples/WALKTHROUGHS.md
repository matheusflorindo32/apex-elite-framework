# Eight CLI walkthroughs

Each command below was run against the local CLI. The reported type and aliases are observations from its JSON. The subsequent activity and acceptance check are illustrative and require a person or a separately configured assistant. These commands explicitly select a project type. They exercise plan generation, independently of automatic keyword routing.

## Researcher reviewing a paper

```sh
aef plan --type scientific --request "Revise um artigo sobre uma oficina com amostra voluntária." --format json
```

Observed team for `scientific` (exit 0): @Editorial, @QA, @Research, @Scientific.

Compare each inference with the study design. Flag missing comparisons. A methodology reviewer signs off on causal language.

## Student planning a TCC

```sh
aef plan --type scientific --request "Planeje um TCC sobre leitura em sala, do protocolo à revisão." --format json
```

Observed team for `scientific` (exit 0): @Editorial, @QA, @Research, @Scientific.

Define the question, review feasibility with the supervisor and allocate milestones. The supervisor checks access to data before collection.

## Teacher preparing a lesson

```sh
aef plan --type general --request "Planeje uma aula de 45 minutos sobre frações." --format json
```

Observed team for `general` (exit 0): @EPO, @QA.

Prepare objectives, a timed exercise and an exit question. Activities fit 45 minutes and the exit question tests the objective.

## Developer planning an app

```sh
aef plan --type software --request "Planeje um aplicativo de agenda local." --format json
```

Observed team for `software` (exit 0): @Automation, @Business, @QA, @Software.

Review requirements, data retention and a backup test. Restoring a sample backup must recover the saved events.

## Entrepreneur testing a business

```sh
aef plan --type research --request "Compare fontes públicas sobre demanda por um curso." --format json
```

Observed team for `research` (exit 0): @Business, @QA, @Research.

Use the business reviewer to turn market evidence into a low-cost interview experiment. Record an adoption hypothesis and a measurable threshold.

## User organizing an automation

```sh
aef plan --type automation --request "Planeje uma automação para classificar arquivos de exemplo." --format json
```

Observed team for `automation` (exit 0): @Automation, @QA, @Software.

Map trigger, duplicate event handling and recovery. A repeated event has one recorded effect in a controlled trial.

## Designer preparing visual material

```sh
aef plan --type catalog --request "Planeje um catálogo digital para uma feira de livros." --format json
```

Observed team for `catalog` (exit 0): @Design, @Editorial, @Marketing, @QA.

Review hierarchy, mobile legibility and image permissions before export. Check reading order and image proportions in the exported sample.

## Beginner configuring an assistant

```sh
aef plan --type general --request "Planeje configurar meu assistente com as instruções do framework." --format json
```

Observed team for `general` (exit 0): @EPO, @QA.

Load one skill file and ask for its deliverable using a fictional request. The reader identifies the skill, input, output and remaining manual check.
