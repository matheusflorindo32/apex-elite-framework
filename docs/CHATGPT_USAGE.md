# Uso do Apex Elite Framework no ChatGPT

Este documento transforma os aliases do framework em comandos conversacionais simples para uso no ChatGPT.

## Comandos principais

### `@Commander`

Use em projetos longos, com várias fases, arquivos, entregas ou decisões.

Exemplo:

```text
@Commander
Coordene este projeto. Registre decisões, riscos, pendências, prioridades e acione o @EPO para cada entrega.
```

### `@EPO`

Use para uma tarefa específica que exija análise, seleção de equipe, execução, revisão cruzada e auditoria.

Exemplo:

```text
@EPO
Analise este trabalho, selecione somente os especialistas seniores necessários, execute, revise e entregue com QA final.
```

## Skills especializadas

- `@Scientific` — metodologia, evidências, estatística, referências e revisão científica.
- `@Editorial` — arquitetura editorial, tipografia, diagramação, paginação e PDF.
- `@Software` — arquitetura, implementação, testes, segurança e documentação.
- `@Research` — pesquisa documental, técnica, competitiva ou acadêmica.
- `@Marketing` — posicionamento, copy, proposta de valor e conversão.
- `@Design` — direção de arte, identidade, fotografia, UX visual e consistência.
- `@Business` — viabilidade, operação, receita, custos e escalabilidade.
- `@Automation` — fluxos, gatilhos, logs, aprovações, idempotência e condição de parada.
- `@QA` — revisão adversarial, auditoria, severidade e critérios de aceite.

## Regra de funcionamento

Ao receber um alias, o assistente deve:

1. identificar o objetivo real e o entregável;
2. ler as regras correspondentes no repositório;
3. escolher somente especialistas que alterem materialmente a qualidade;
4. registrar função, justificativa, responsabilidade e critério de aprovação;
5. criar plano, riscos e critérios de aceite;
6. executar ou preparar a execução;
7. realizar revisão cruzada;
8. aplicar `@QA`;
9. declarar limitações e pendências reais;
10. não afirmar validação sem evidência.

## Prompt universal recomendado

```text
@EPO

Analise profundamente o material e o objetivo desta tarefa. Selecione automaticamente somente as Skills e os especialistas seniores que realmente agreguem valor. Defina responsabilidades, riscos, critérios de aceite e plano de execução. Execute por etapas, faça revisão cruzada, aplique QA adversarial e só entregue após auditoria final. Diferencie fatos, inferências e recomendações. Não invente dados, fontes, validações ou resultados. Preserve sempre a orientação mais recente do projeto.
```

## Prompt para projetos longos

```text
@Commander

Assuma a coordenação deste projeto. Consolide objetivo, escopo, decisões confirmadas, arquivos, entregáveis, dependências, riscos, backlog e critérios de conclusão. Acione o @EPO para cada tarefa relevante e mantenha um registro claro do que foi feito, do que está pendente e da próxima ação prioritária.
```

## Exemplo: catálogo comercial

```text
@EPO @Editorial @Design @Marketing @QA

Analise os arquivos e produza um catálogo comercial premium. Os produtos carro-chefe devem aparecer primeiro, os produtos avulsos vêm antes dos kits, não inserir preços no catálogo principal e manter foco comercial. Verifique nomes, códigos, especificações, imagens, sumário, contatos, QR Codes, resolução, cortes, margens, versão digital e versão para impressão.
```

## Limites importantes

Os aliases são uma convenção documental e conversacional. Eles não aparecem automaticamente como menus visuais do ChatGPT. Em ambientes com Skills nativas do Codex, use os nomes registrados com `$`, por exemplo `$elite-project-orchestrator` e `$commander`.

O framework organiza e valida o trabalho, mas não substitui revisão humana em saúde, segurança pública, decisões institucionais, jurídicas, financeiras ou científicas de alto risco.
