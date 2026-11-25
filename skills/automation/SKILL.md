---
name: automation
description: Projetar, revisar e tornar observáveis automações, integrações, pipelines e fluxos com agentes. Usar quando uma tarefa exigir idempotência, retries, aprovações humanas, condições de parada, rollback, logs ou tratamento seguro de efeitos externos.
---

# Automation

Projeta fluxos reproduzíveis, seguros e observáveis.

## Regras

- mapear gatilho, entrada, processamento, saída e erro;
- definir idempotência;
- registrar logs;
- incluir aprovações em ações sensíveis;
- evitar loops infinitos;
- definir condição de parada;
- prever rollback.

## Aplicação prática

- **Entrada.** Gatilho, permissões, dados e efeitos externos permitidos.
- **Entrega.** Fluxo com chave de deduplicação, limite de tentativas e recuperação.
- **Aceite e parada.** Descreva o resultado de repetir o mesmo evento. Suspenda ações externas quando a autorização for incerta.

Pedido de exemplo

> Planeje classificar arquivos de uma pasta de teste e lidar com entradas repetidas.
