# Working with scientific evidence · Guia de pesquisa

Use apenas material que você possa compartilhar. Um docente pode executar os exemplos com os dados fictícios abaixo. O APEX organiza perguntas, papéis e verificações. O pesquisador consulta as fontes, avalia o conteúdo e assina a conclusão. Consulte as [responsabilidades do ecossistema](ECOSYSTEM.md).

## Exercício 1 — Revisar a conclusão de um artigo

Abra uma conversa, copie o texto de [@Scientific](../skills/scientific/SKILL.md) e cole o pedido completo. O resumo é inteiramente fictício.

> @Scientific, revise este resumo fictício usando somente o material abaixo. Faça uma tabela com a conclusão avaliada, o resultado que a sustenta, o limite da inferência e a informação que falta. Reescreva a conclusão em duas frases.
>
> Método informado. Uma turma de 20 alunos que se voluntariaram para uma oficina respondeu a testes antes e depois da atividade. Resultados informados. A média anterior foi 6 e a posterior foi 7. O resumo omite grupo de comparação, perdas, dados pareados, dispersão e teste estatístico. Conclusão do artigo. “A oficina causou um ganho estatisticamente significativo de um ponto na aprendizagem.”

**Resultado ilustrativo**

| Conclusão avaliada | Evidência fornecida | Limite da inferência | Informação a solicitar |
|---|---|---|---|
| Ganho de um ponto | As médias informadas foram 6 e 7. | Diferença descritiva de um ponto entre as médias. A composição das duas avaliações é desconhecida. | Quantidade de respostas em cada avaliação, perdas e correspondência individual. |
| Ganho causado pela oficina | O resumo descreve medições antes e depois em uma turma voluntária. | Aprendizagem fora da oficina e familiaridade com o teste são explicações possíveis. | Desenho completo, condições de comparação e calendário das medições. |
| Ganho estatisticamente significativo | O resumo fornece duas médias. | A significância é indeterminada com o material fornecido. | Dispersão, observações pareadas e análise estatística. |

Conclusão revisada de exemplo. “Na turma voluntária, a média informada foi 6 antes da oficina e 7 depois. O resumo deixa indeterminadas a contribuição causal da oficina e a significância estatística da diferença.”

Para uma conferência independente do primeiro resultado, abra outra conversa, forneça [@QA](../skills/quality-assurance/SKILL.md), o resumo e a saída, e cole o pedido. Use os itens aplicáveis do [checklist científico](../checklists/scientific-qa.md).

> @QA, compare a tabela e a conclusão revisada com o resumo fictício. Registre o trecho que sustenta cada afirmação, questões pendentes de evidência e qualquer extrapolação causal ou estatística.

**Aceite e aprovação humana.** A revisão mantém 6, 7 e a diferença de um ponto, distingue explicações possíveis de fatos observados e trata causalidade e significância como indeterminadas. Registre quem revisou, a data e a decisão de aceitar ou devolver para ajuste. Para um artigo real, o autor e o revisor de domínio conferem o texto e os dados originais antes de aprovar a conclusão.

## Exercício 2 — Delimitar um TCC

Em uma nova conversa, forneça [@EPO](../skills/elite-project-orchestrator/SKILL.md) para planejar o TCC e [@Research](../skills/research/SKILL.md) para registrar a origem e o recorte dos documentos. O cenário é inteiramente fictício.

> @EPO, com apoio de @Research, transforme este tema em uma pergunta respondível, um recorte, um método descritivo inicial e seis entregas semanais. Explicite o que o acervo permite concluir e o que depende da aprovação do orientador. Use apenas a entrada fictícia.
>
> Tema inicial. “Como as bibliotecas universitárias melhoram a aprendizagem?” Tempo disponível. Seis semanas. Acervo disponível. Seis boletins mensais fictícios de uma biblioteca, de janeiro a junho de 2025, com contagem agregada de empréstimos por categoria. Os boletins registram contagens de empréstimos e omitem notas, identidade dos usuários e dados de outras bibliotecas. Neste exercício, trabalhe somente com a descrição do acervo e planeje a extração, mantendo os valores em aberto.

**Resultado ilustrativo**

| Decisão | Exemplo de saída |
|---|---|
| Pergunta | Como se distribuem os empréstimos por categoria e por mês nos boletins dessa biblioteca entre janeiro e junho de 2025? |
| Recorte | Uma biblioteca, os seis boletins mensais e as categorias definidas em cada documento. A unidade de registro é a contagem de empréstimos por categoria e mês. |
| Método | Registrar boletim, página, mês, categoria e contagem. Conferir se as categorias são comparáveis, marcar dados ausentes e descrever as categorias e meses comparáveis em uma tabela. |
| Limite | O acervo permite descrever empréstimos registrados. Medidas de aprendizagem, número de pessoas únicas e generalizações para outras bibliotecas ficam indeterminados. |

| Semana | Entrega verificável |
|---|---|
| 1 | Pergunta e recorte discutidos com o orientador. |
| 2 | Inventário dos seis boletins e ficha de extração. |
| 3 | Piloto de extração em um boletim e regra para categorias divergentes. |
| 4 | Planilha de extração com páginas e lacunas registradas. |
| 5 | Tabela descritiva conferida com os boletins e trecho sobre limitações. |
| 6 | Versão para revisão do orientador com trilha das fontes. |

**Aceite e aprovação humana.** A pergunta cabe no acervo, os seis marcos têm entregas conferíveis e a saída mantém as contagens em aberto. O orientador confirma acesso ao acervo real, comparabilidade das categorias, método, prazo e regras institucionais antes da coleta. Registre responsável, data, decisão e pendências. Se faltar acesso ou comparabilidade, ajuste o recorte antes de avançar.

Os dois exercícios podem ser feitos no chat com as entradas acima. Em um checkout, o comando `uv run aef plan --type scientific` gera um plano para revisão humana. Consulte `docs/QUICK_START.pt-BR.md` e `docs/SKILLS.md` no repositório.

## Escolha uma tarefa

| Tarefa | Pedido copiável | Critério de revisão humana |
|---|---|---|
| Artigo e conclusões | @Scientific, relacione cada conclusão do resumo fictício ao resultado que a sustenta. | Toda inferência tem trecho e limite. |
| TCC | @EPO, delimite uma pergunta a partir do acervo fictício do exercício de TCC. | Orientador confirma viabilidade e escopo. |
| Dissertação | @Commander, organize protocolo, coleta e capítulos em um cronograma com dependências. | Cada etapa tem condição de início e responsável. |
| Avaliação metodológica | @Scientific, identifique vieses de seleção e mensuração no exemplo da oficina. | Separe riscos possíveis de problemas demonstrados. |
| Revisão bibliográfica | @Research, elabore termos, critérios de inclusão e formulário de extração para estudos de oficinas. | Bibliotecário ou pesquisador testa a estratégia e registra bases e datas. |
| Referências | @Research, confira se cada trecho fornecido sustenta a alegação correspondente. | Registre página, passagem e referências inacessíveis. |
| Lacunas | @Scientific, a partir da tabela de estudos fornecida, identifique perguntas ainda sem resposta nesse recorte. | Delimite cada lacuna ao corpus disponível. |
| Planejamento experimental | @Scientific, planeje comparar duas sequências didáticas, especificando desfecho e fatores de confusão. | Pesquisador avalia ética, alocação e adequação da análise antes da coleta. |
| Apresentação | @Design, organize objetivo, resultado e limite em três slides acessíveis. | O limite continua legível na projeção. |
| Revisão editorial | @Editorial, reduza o resumo mantendo números e grau de incerteza. | Autor compara original e revisão linha a linha. |
| Controle de qualidade | @QA, aplique o checklist científico e enumere os itens sem evidência. | Cada aprovação aponta para evidência verificável. |

Use o [modelo de revisão](../templates/scientific-review.md) e a [lista de verificação](../checklists/scientific-qa.md). Registre a assistência de IA conforme as regras da instituição ou periódico. A verificação de referências exige acesso às fontes originais.
