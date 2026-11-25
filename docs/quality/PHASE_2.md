# Segunda fase · decisão sobre a candidata

**Referência inicial** — PR #6, branch feature/apex-elite-international-readiness, commit `9842cd48f560894ea17d4b86d81e1a9874d9b43c`. A revisão começou com 119 arquivos rastreados e uma árvore limpa. O único comentário técnico na PR tratava da ordenação dos caminhos no Windows. O ajuste já estava na base desta fase. A matriz anterior terminou com oito sucessos e um cancelamento em macOS/Python 3.13. O status, o SHA final, o inventário das alterações e os resultados da candidata entregue estão na [PR #6](https://github.com/matheusflorindo32/apex-elite-framework/pull/6).

| Jornada | Evidência reproduzível | Critério que permanece aberto |
|---|---|---|
| Iniciante | Abra o início rápido no seu idioma, copie o pedido fictício e compare a resposta com os critérios de aceite. O roteiro registra conclusão, dúvidas e ajuda recebida. | Uma pessoa concluir o roteiro em uma sessão observada. |
| Pesquisa | Refaça os exercícios do [guia científico](../RESEARCHERS.md). No primeiro, a diferença entre as médias 6 e 7 é descritiva. As duas médias são insuficientes para estabelecer significância ou causalidade. No segundo, a unidade disponível é a contagem de empréstimos por categoria e mês. O planejamento preserva ausências e limites da fonte. | Respostas do chat são ilustrativas. O autor e o orientador avaliam a aplicação real. |
| Desenvolvimento | Execute os comandos abaixo. O verificador instala cada distribuição em ambiente próprio, com espaços e acentos no caminho. O teste gera e valida o plano e verifica a recuperação após erro. | O ensaio de rollback usa a versão anterior em ambiente separado, dentro de seu checkout. |
| Assistentes | Baixe os arquivos de [distribuição](../DISTRIBUTION.md). Abra o Markdown fora do clone e extraia os dois ZIPs em pastas separadas. Compare com os checksums e siga os guias internos. | Descoberta no cliente e execução por modelo exigem evidência própria. O codex-cli 0.172.0-alpha.2 estava instalado; a inicialização do app-server para testar skills/list encontrou estado SQLite/configuração somente leitura. Nenhum modelo foi chamado nesse ensaio. |

## Reprodução em um checkout da mesma revisão

```sh
uv sync --locked --dev
uv run pytest
uv run aef validate
uv run python scripts/build_bundles.py --check
uv build --out-dir dist
uv run python scripts/check_install.py dist
```

Use um diretório dist vazio para testar a candidata desejada. O build isolado do sdist pode precisar de cache de compilação ou rede. O uso da CLI instalada requer somente recursos locais. Em Linux, duas gerações em pastas distintas também podem ser comparadas com os comandos abaixo, a partir da raiz do checkout.

```sh
a=$(mktemp -d)
b=$(mktemp -d)
python scripts/build_bundles.py --output-dir "$a"
python scripts/build_bundles.py --output-dir "$b"
diff -qr "$a" "$b"
(cd "$a" && sha256sum -c SHA256SUMS)
```

## Achados e revisão

1. **Implementação.** O Markdown da base mantinha links relativos ao clone. Os ZIPs precisavam de um ponto de entrada utilizável após a extração. A revisão de packaging identificou configurações inválidas que provocavam traceback ou permitiam gerar planos inconsistentes. Os testes da segunda fase cobrem os artefatos isolados e o contrato de erro da CLI.
2. **Revisão cruzada.** A frente de documentação conferiu 137 referências locais e âncoras nos seis documentos alterados, além das 11 associações entre alias e diretório. A coordenação conferiu os limites dos dois exercícios científicos e o vínculo dos três catálogos públicos com o registro interno. A frente de packaging fez a verificação independente dos exercícios e da distribuição.
3. **Adjudicação.** Os resultados de suíte, arquivos recebidos pelo GitHub e jobs da revisão final estão na PR. A autorização para publicação continua com o mantenedor. Use a [rubrica histórica e seus critérios](READINESS.md) para interpretar a nota.

**Limites visuais.** Nesta revisão, o navegador recebeu a página de erro “Unicorn” do GitHub tanto ao abrir o README quanto ao recarregá-lo. O banner tem viewBox, título, descrição e fundo próprio. Os READMEs oferecem texto alternativo e descrição textual do diagrama. A revisão de conteúdo e links não valida o layout real em tela estreita, temas ou leitor de tela.

**Recursos.** Git, API do GitHub, Python, pytest, uv, arquivos ZIP e SHA-256 forneceram os inventários e resultados. Foram reaproveitados os relatórios e testes anteriores. A coordenação separou três frentes de escrita, com raciocínio baixo para documentação e médio para distribuição e packaging. A plataforma não forneceu medição financeira. O repositório científico relacionado ficou fora da área de edição.

No ensaio de atualização, o revisor também instalou as versões 1.0.0, 1.0.1rc1 e novamente 1.0.0 no mesmo ambiente virtual offline. A execução com 1.0.0 usou o checkout da base histórica. O plano de software manteve os mesmos bytes nos três pontos. Seis comandos da CLI instalada também passaram com um audit hook do Python bloqueando sockets e subprocessos. Essa verificação se limita ao interpretador.

A execução 45641956008 terminou com oito jobs aprovados e um cancelado. O GitHub informou que o job macOS/Python 3.13 ficou 15 minutos sem conseguir runner ARM, sem executar etapas. A mesma falha de infraestrutura ocorreu na revisão anterior. A matriz passou a usar macOS Intel padrão para Python 3.13 e manteve o runner macOS padrão para 3.11 e 3.12. Consulte o resultado no HEAD da PR. A combinação ARM/3.13 permanece sem comprovação.

Na execução 45644999888, macOS Intel/3.13 e macOS ARM/3.11 passaram. O GitHub cancelou o job ARM/3.12 sem atribuir runner. Para a decisão sobre a PR, a matriz automática agora verifica os três Pythons no runner padrão macos-15-intel. Uma execução manual da workflow Quality permite selecionar macos-latest para testar ARM quando houver capacidade. Os sistemas e arquiteturas aparecem nos nomes dos jobs.
