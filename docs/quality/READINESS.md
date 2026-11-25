# Matriz de prontidão

Rubrica de cobertura da candidata. Cada linha tem quatro verificações enumeradas na ordem de leitura. Cada verificação com evidência vale 2,5 pontos. Os campos indicam os números das verificações atendidas na base e na candidata. Ausência de evidência recebe zero crédito e permanece não verificada. Todos os 15 pesos são iguais (1/15). Potencial de adoção mede condições de entrada, sem estimar usuários.

| Dimensão | Quatro verificações | Base → candidata | Nota inicial → final | Evidência e limite |
|---|---|---|---|---|
| Arquitetura | componentes documentados, config separada, recursos instaláveis, fronteiras do ecossistema | 12 → 1234 | 5 → 10 | ARCHITECTURE, ECOSYSTEM, smoke de wheel |
| Código | módulos separados, erros com código, contenção de caminhos, análise estática de tipos | 12 → 123 | 5 → 7,5 | src/aef, testes de regressão; tipagem integral pendente |
| Segurança | runtime sem dependências, CI somente leitura, actions fixadas, auditoria independente | 12 → 1234 | 5 → 10 | SECURITY_AUDIT; escopo limitado aos quatro controles |
| Documentação técnica | arquitetura, extensão, instalação, compatibilidade com fontes | 12 → 1234 | 5 → 10 | ARCHITECTURE, CREATING_SKILLS, INSTALLATION, COMPATIBILITY |
| README | autoria/licença, catálogo, entrada EN/PT, guia sem terminal nas duas línguas | 12 → 1234 | 5 → 10 | README e README.pt-BR |
| Iniciantes | roteiro sem terminal, pedido copiável, saída esperada, observação com usuários | – → 123 | 0 → 7,5 | QUICK_START em duas línguas; estudo humano pendente |
| Distribuição | entry point, wheel funcional fora do clone, sdist testado, manifesto de downloads | 1 → 1234 | 2,5 → 10 | pyproject, check_install, bundles |
| Testes | suíte automatizada, CI, instalação isolada, matriz de SO executada na candidata | 12 → 123 | 5 → 7,5 | testes locais; consultar Actions na PR |
| Compatibilidade | CLI Linux, rotas por produto, fontes por produto, teste em assistente hospedado | 1 → 123 | 2,5 → 7,5 | TESTS, COMPATIBILITY; sessões externas pendentes |
| Acessibilidade | títulos Markdown, texto alternativo do banner, alternativa textual ao diagrama, teste assistivo | 1 → 123 | 2,5 → 7,5 | READMEs; leitor de tela não testado |
| Apresentação | navegação, banner original, diagrama, renderização visual verificada nos dois temas | 1 → 123 | 2,5 → 7,5 | SVG e READMEs; inspeção em temas pendente |
| Internacionalização | conteúdo português, entrada inglesa, dois quick starts, CLI bilíngue | 1 → 123 | 2,5 → 7,5 | README/QUICK_START, CLI em português |
| Reprodutibilidade | lock, exportador, verificação de deriva, checksum | 12 → 1234 | 5 → 10 | uv.lock, scripts/build_bundles.py, SHA256SUMS |
| Governança | licença, contribuição, política de releases, modelo de PR | 123 → 1234 | 7,5 → 10 | LICENSE, CONTRIBUTING, VERSIONING e .github |
| Adoção | exemplos, caminho sem Git, downloads preparados, avaliação externa de adoção | 1 → 123 | 2,5 → 7,5 | examples, bundles, quick starts; sem telemetria ou entrevistas |

Média inicial 3.83/10 (23/60 verificações). Média da candidata 8.67/10 (52/60). Avaliações humanas de compreensão, estética e adoção permanecem abertas.
