# Modelo de Qualidade

## Gates

Uma entrega é aprovada quando requisitos obrigatórios possuem evidência e não restam achados críticos ou altos. Achados médios e baixos podem ser aceitos somente com risco documentado.

## Severidade

| Nível | Definição | Decisão |
|---|---|---|
| Crítico | Pode causar dano, perda de dados, exposição grave, resultado inválido ou impedir uso. | Bloquear e corrigir imediatamente. |
| Alto | Compromete requisito central, segurança, precisão ou operação confiável. | Bloquear a entrega. |
| Médio | Afeta qualidade ou casos relevantes sem invalidar o núcleo. | Corrigir ou aceitar formalmente. |
| Baixo | Problema localizado, cosmético ou de manutenção. | Planejar correção. |
| Informativo | Observação, evidência ou oportunidade sem defeito atual. | Registrar. |

## Evidência

Rotule cada verificação como automatizada, inspeção manual ou confirmação do usuário. Sucesso de ferramenta não equivale a confirmação visual ou operacional do produto.

## Iteração

Use no máximo três ciclos de correção. Pare antes se os gates passarem. Pare com status incompleto quando não houver progresso mensurável ou o orçamento for esgotado; registre os achados remanescentes.

