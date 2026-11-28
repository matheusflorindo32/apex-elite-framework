# Consumir um handoff Tropa Scientific Skills v1

O APEX recebe o envelope e os dois artefatos locais de um canal autorizado.
Confirme o SHA Git completo da revisão aprovada por um canal independente.
O envelope traz somente metadados e digests. Forneça os caminhos dos arquivos
localmente e preserve os bytes, inclusive quebras de linha.

```sh
aef handoff consume --envelope handoff-apex.json --plan plan.json --acceptance-criteria acceptance-criteria.json --expected-revision SHA_GIT_COMPLETO
```

O consumidor aceita um envelope UTF-8 de até 8 KiB e dois arquivos JSON de
até 1 MiB cada. O envelope precisa identificar a origem Tropa, o destino
APEX, o estado `prepared` e a versão 1. O APEX verifica o SHA-256 de cada
artefato, valida `plan.json` pelo schema de Team Plan existente e exige que
o array de critérios corresponda a `acceptance_criteria` em conteúdo e ordem.

A saída JSON contém `verified`, a revisão, os dois digests e o Team Plan
validado. O plano em stdout pode conter dados do operador. Use fixtures
sintéticas em logs e exemplos públicos. Erros de leitura ou validação
retornam 2 e escrevem apenas o diagnóstico em stderr.

A verificação comprova consistência entre versão esperada, envelope e
arquivos recebidos. O operador continua responsável pela autenticidade da
origem, pelo acesso autorizado aos arquivos e pelo aceite humano do plano.
A CLI é offline, lê os caminhos fornecidos e mantém os arquivos de entrada.
