# Seu primeiro plano com o APEX

[English](QUICK_START.md) · [Visão geral](../README.pt-BR.md)

Imagine que você dispõe de 30 minutos para ensinar uma turma a avaliar uma fonte. Experimente planejar a aula com o coordenador de entregas, chamado @EPO. Reserve de 5 a 10 minutos para tentar. Basta um navegador e um assistente de conversa que aceite texto.

1. **Obtenha as instruções.** Abra a [skill do coordenador](../skills/elite-project-orchestrator/SKILL.md). Na barra do arquivo no GitHub, use **Copy raw file** para copiar ou **Download raw file** para baixar. O arquivo contém texto simples. Para obter as onze skills juntas, baixe o [arquivo de conhecimento](../bundles/APEX_CHATGPT_KNOWLEDGE.md) da mesma maneira.
2. **Dê contexto ao assistente.** Abra uma conversa. Anexe o arquivo ou cole o texto da skill. Copie o pedido a seguir para a mesma conversa.

   > @EPO Planeje uma aula de 30 minutos para calouros sobre como conferir uma fonte. Quero um objetivo de aprendizagem, três atividades com duração e uma forma de verificar o aprendizado. Explicite as suposições.

3. **Confira o resultado.** Some os minutos e confira se a atividade final mede o objetivo. Se a tarefa exigir apenas memorizar termos, peça uma atividade em que cada aluno avalie uma fonte e explique seu raciocínio.

**Exemplo ilustrativo de resposta.** Objetivo: identificar autoria, data e evidência de uma afirmação. Reserve 5 minutos para ler uma afirmação, 15 para comparar dois trechos em duplas e 10 para cada aluno redigir seu parecer. Recolha os pareceres e confira se citam um detalhe de cada trecho. Suposição: o professor fornece ambos os textos.

## Escolha sua próxima tarefa

| Perfil | O que experimentar | O que conferir |
| --- | --- | --- |
| Estudante | Cole o [pedido do TCC fictício](RESEARCHERS.md#exercício-2--delimitar-um-tcc) com as instruções de @EPO e @Research. | Cada marco produz algo que pode ser apresentado. |
| Pesquisador | Cole o [resumo fictício do artigo](RESEARCHERS.md#exercício-1--revisar-a-conclusão-de-um-artigo) com as instruções de @Scientific. | Vincule cada crítica ao texto fornecido. Registre detalhes ausentes como desconhecidos. |
| Desenvolvedor | Siga a [instalação](INSTALLATION.md) e execute `uv run aef plan --type software --request "Planejar um diário de leitura acessível"`. | Execute os testes do projeto e revise o plano antes da implementação. |
| Professor | Cole as [instruções de @Editorial](../skills/editorial/SKILL.md) e o plano de aula acima. Peça uma folha de atividade. | Compare o exercício com o objetivo. |

## Observe o primeiro uso

Peça a alguém que ainda não conhece o APEX para começar pelo README e tentar os três passos acima sem orientação. Reserve de 5 a 10 minutos e comece a contar quando a pessoa abrir o README. Considere que houve sucesso quando ela localizar a skill, enviar o pedido e verificar que as atividades somam 30 minutos e que a última mede o objetivo. Registre tempo decorrido, etapa alcançada, ponto de dúvida, ajuda solicitada e resultado. Se o tempo acabar, registre o ponto de parada. A faixa é um orçamento de observação. O tempo real ainda depende de testes com iniciantes.

## Dúvidas frequentes

**O assistente ignorou @EPO.** Cole as instruções do coordenador e peça explicitamente que o assistente as siga. O alias é um apelido definido no projeto. As demais especialidades estão no [catálogo](SKILLS.md).

**Não consigo anexar arquivos.** Cole o texto de uma única skill na conversa. O arquivo completo pode exceder o limite de contexto de alguns serviços.

**O APEX recupera referências científicas?** O APEX organiza a revisão. Forneça fontes verificadas e confira cada citação. [Guia de pesquisa](RESEARCHERS.md)

**A resposta será sempre igual?** O texto produzido pelo assistente varia. Para planejamento local reproduzível com catálogo e entrada fixos, use a CLI.
