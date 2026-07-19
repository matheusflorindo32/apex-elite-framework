# Controle de Loop

## Objetivo

Permitir ciclos de melhoria sem repetição infinita.

## Condições de parada

O loop termina quando:

- todos os critérios de aceite obrigatórios estão atendidos;
- não há defeitos críticos ou altos;
- pendências médias e baixas estão registradas;
- a melhoria estimada do próximo ciclo é marginal;
- o limite de ciclos foi atingido.

## Limites padrão

- planejamento: até 2 ciclos;
- produção: até 3 ciclos;
- QA/correção: até 3 ciclos;
- auditoria final: 1 ciclo independente.

## Regra

Nunca repetir uma rodada sem listar exatamente o que mudou e qual erro foi corrigido.
