# 1.0.1-rc.1 · revisão humana

A versão Python correspondente é `1.0.1rc1`. A correção principal restaura o acesso aos recursos da CLI instalada fora do repositório. Os downloads de contexto e de skills estão em [bundles](../bundles/). O arquivo SHA256SUMS permite comparar os bytes recebidos com os da revisão aprovada.

## Avaliar e atualizar

Em um checkout da candidata, siga o [guia de instalação](INSTALLATION.md). Guarde saídas de projetos fora do clone e use um ambiente virtual novo. Execute:

```sh
uv sync --locked --dev
uv run pytest
uv run aef validate
python scripts/build_bundles.py --check
uv build --out-dir dist
uv run python scripts/check_install.py dist
```

Compare um plano gerado com os critérios do seu projeto. Usuários de contexto Markdown podem trocar o arquivo carregado em uma cópia do assistente e repetir o início rápido.

## Rollback

Retome o ambiente anterior ou abra um clone separado no commit `35de85a18ddd8d21a1899fcf0a4e11f8b9c9cd83` e rode a CLI dentro do checkout. Para assistentes, restaure a cópia anterior das instruções e do contexto. O APEX não exige migração de banco de dados.

## Decisão do mantenedor

Avalie os [testes](quality/TESTS.md), a [matriz](quality/READINESS.md), a [segurança](quality/SECURITY_AUDIT.md) e a [auditoria](quality/INDEPENDENT_AUDIT.md). A divulgação depende de revisão de links e da experiência de primeiro uso. Publicação, assinatura e tag definitiva dependem de autorização expressa.

## Indicadores para a decisão

- **Implementação dos entregáveis obrigatórios**: 19/19 (100%). Inventário: dois READMEs, início rápido, instalação, catálogo, compatibilidade, guias por perfil, FAQ nos guias rápidos, pacotes, exemplos, arquitetura, benchmark, segurança, testes, matriz, changelog, notas da candidata, auditoria e PR. Este indicador conta presença e não mede eficácia.
- **Prontidão para divulgação**: quatro de cinco verificações (80%). Kit redigido, guias bilíngues disponíveis, links externos do Markdown acessíveis e downloads consistentes. Falta observar uma pessoa iniciante usando o guia.
- **Prontidão para release**: os seis controles são versão/changelog, distribuições instaláveis, integridade, revisão de segurança, regressão multiplataforma e aprovação do mantenedor. A aprovação é obrigatória e permanece aberta.

As porcentagens contam verificações discretas. A revisão executiva deve considerar separadamente a qualidade de cada dimensão e os limites descritos na rubrica.
