# Exemplo — Automação com aprovação humana

## Pedido

Usar `@EPO` para planejar uma automação que classifique documentos recebidos, gere rascunhos e solicite aprovação humana antes de enviar qualquer comunicação externa.

## Equipe esperada

- Arquiteto de automação para estados, idempotência e parada.
- Engenheiro de integração para contratos, validação e testes.
- QA de automação para falhas, permissões e efeitos duplicados.

## Entrega esperada

Diagrama do fluxo, matriz de permissões, contrato de entradas e saídas, política de retry, logs, aprovação humana, rollback e testes de falha.

## Critérios de aceite

- nenhuma mensagem é enviada sem aprovação;
- execução repetida não duplica efeitos;
- retries possuem limite e backoff;
- condição de parada e circuit breaker são explícitos;
- logs não armazenam documentos ou segredos indevidamente;
- falhas são observáveis e recuperáveis.

