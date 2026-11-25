# Seu primeiro plano com o APEX

[English](QUICK_START.md) · [Visão geral](../README.pt-BR.md)

Imagine que você dispõe de 30 minutos para ensinar uma turma a avaliar uma fonte. Experimente planejar a aula com o coordenador de entregas, chamado @EPO. Basta um navegador e um assistente de conversa que aceite texto.

1. **Obtenha as instruções.** Abra a [skill do coordenador](../skills/elite-project-orchestrator/SKILL.md). Na barra do arquivo no GitHub, use **Copy raw file** para copiar ou **Download raw file** para baixar. O arquivo contém texto simples. Para obter as onze skills juntas, baixe o [arquivo de conhecimento](../bundles/APEX_CHATGPT_KNOWLEDGE.md) da mesma maneira.
2. **Dê contexto ao assistente.** Abra uma conversa. Anexe o arquivo ou cole o texto da skill. Copie o pedido a seguir para a mesma conversa.

   > @EPO Planeje uma aula de 30 minutos para calouros sobre como conferir uma fonte. Quero um objetivo de aprendizagem, três atividades com duração e uma forma de verificar o aprendizado. Explicite as suposições.

3. **Confira o resultado.** Some os minutos e confira se a atividade final mede o objetivo. Se a tarefa exigir apenas memorizar termos, peça uma atividade em que cada aluno avalie uma fonte e explique seu raciocínio.

**Exemplo ilustrativo de resposta.** Objetivo: identificar autoria, data e evidência de uma afirmação. Reserve 5 minutos para ler uma afirmação, 15 para comparar dois trechos em duplas e 10 para cada aluno redigir seu parecer. Recolha os pareceres e confira se citam um detalhe de cada trecho. Suposição: o professor fornece ambos os textos.

## Escolha sua próxima tarefa

| Perfil | O que experimentar | O que conferir |
| --- | --- | --- |
| Estudante | Peça ao @EPO para dividir um projeto de TCC em pergunta, marcos e revisão com o orientador. | Cada marco produz algo que pode ser apresentado. |
| Pesquisador | Peça ao @Scientific para revisar um resumo público e identificar lacunas no método. | Vincule cada crítica ao texto fornecido. Registre detalhes ausentes como desconhecidos. |
| Desenvolvedor | Gere um plano de equipe pelo [guia de instalação](INSTALLATION.md). | Execute os testes do projeto e revise o plano antes da implementação. |
| Professor | Peça ao @Editorial para transformar o plano de aula em uma atividade para a turma. | Compare o exercício com o objetivo. |

## Dúvidas frequentes

**O assistente ignorou @EPO.** Cole as instruções do coordenador e peça explicitamente que o assistente as siga. O alias é um apelido definido no projeto. As demais especialidades estão no [catálogo](SKILLS.md).

**Não consigo anexar arquivos.** Cole o texto de uma única skill na conversa. O arquivo completo pode exceder o limite de contexto de alguns serviços.

**O APEX recupera referências científicas?** O APEX organiza a revisão. Forneça fontes verificadas e confira cada citação. [Guia de pesquisa](RESEARCHERS.md)

**A resposta será sempre igual?** O texto produzido pelo assistente varia. Para planejamento local reproduzível com catálogo e entrada fixos, use a CLI. O tempo até o primeiro uso bem-sucedido ainda precisa ser observado com iniciantes.
