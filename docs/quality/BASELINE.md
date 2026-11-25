# CP00 · inventário de partida

Em 25/11/2026, a referência da main era `35de85a18ddd8d21a1899fcf0a4e11f8b9c9cd83`. Havia 85 arquivos rastreados, sete commits na main, oito branches remotas e nenhuma tag ou release. A branch desta iniciativa estava disponível e foi criada a partir desse commit. O conector GitHub confirmou visibilidade pública. A licença e a autoria constam em LICENSE e pyproject.toml.

## Como reproduzir o inventário

Use `git ls-tree -r --name-only 35de85a` para a lista exata de arquivos e `git log --oneline 35de85a` para o histórico. Os incrementos anteriores introduziram scaffold, núcleo, documentação, CI, exportador e kit visual. O projeto já tinha AGENTS.md, guias de contribuição, segurança e versionamento, 11 skills, seis tipos de projeto, seis checklists, seis templates, cinco exemplos, dois workflows de planejamento, um schema, um exportador e um pacote Python com CLI. A base trazia política Dependabot, lock de desenvolvimento e uma workflow de qualidade para Linux. O README estava em português. A base exportada era gerada sob demanda.

As consultas REST a pulls, issues, releases e actions/runs retornaram cinco PRs abertas (#1–3 Dependabot, #4 guia ChatGPT, #5 fronteira do motor de vídeo), zero issues independentes e 21 execuções históricas de Actions. Nenhuma dessas PRs foi incorporada nesta frente. As branches de design visual, vídeo, documentação ChatGPT e fundação foram preservadas.

## Responsabilidades e evidência

| Revisão | Decisão e motivo | Evidência de aceitação |
|---|---|---|
| Engenharia e packaging | Conferir o uso fora do clone | Build e instalação limpa com CLI em outro diretório |
| Distribuição | Delimitar fontes públicas | Regeneração byte a byte e manifesto |
| Skills e metodologia | Evitar atribuir pesquisa bibliográfica ao orquestrador | Matriz e casos com limites de evidência |
| UX e redação bilíngue | Dar entrada sem terminal | Instruções navegáveis nas duas línguas |
| Compatibilidade | Separar interfaces documentadas e integrações testadas | Fontes oficiais e estado por plataforma |
| Segurança e auditoria independente | Rever mudanças e adjudicar achados | Severidade, regressão e pendências explícitas |

Os 25 testes existentes passaram. A instalação limpa do wheel falhou ao listar skills fora do checkout (saída 2). Esse defeito é o controle negativo para o novo teste de distribuição.
