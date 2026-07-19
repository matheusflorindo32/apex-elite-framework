# Arquitetura

## Visão geral

O AEF separa instruções para agentes de lógica determinística. Skills descrevem procedimentos; arquivos JSON registram aliases e equipes; o pacote Python gera e valida artefatos sem chamar modelos ou serviços externos.

```text
pedido -> classificação -> tipo de projeto -> equipe -> Team Plan
                                              |          |
                                              v          v
                                         checklists -> auditoria
```

## Componentes

- `catalog.py`: localiza a raiz, carrega JSON e Skills.
- `frontmatter.py`: interpreta o contrato mínimo `name` e `description`.
- `planning.py`: classifica pedidos e gera equipe, brief e checklist.
- `loop.py`: encerra ciclos por qualidade, orçamento ou falta de progresso.
- `validation.py`: executa gates estruturais e documentais.
- `cli.py`: expõe comandos e códigos de saída estáveis.

## Decisões

1. Biblioteca padrão no runtime: reduz superfície de dependências e permite uso offline.
2. Configuração explícita: seleção de equipe é auditável, sem “magia” ou agentes decorativos.
3. Skills concisas: detalhes reutilizáveis permanecem em templates, workflows e checklists.
4. Saídas puras por padrão: o CLI imprime em stdout; arquivos exigem `--output`.
5. Segurança por escopo: o core não publica, envia mensagens, acessa credenciais nem executa ações remotas.

## Extensão futura

Integrações com modelos devem ser opcionais, isoladas sob `integrations/` e protegidas por validação de entrada, limites, logs sem conteúdo sensível e aprovação humana para efeitos externos.

