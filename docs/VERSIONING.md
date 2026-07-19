# Versionamento

O AEF segue Semantic Versioning:

- `MAJOR`: quebra de CLI, schema, configuração ou contrato de Skill;
- `MINOR`: novo tipo de projeto, comando, Skill ou saída compatível;
- `PATCH`: correção compatível, documentação ou melhoria de validação.

## Processo de release

1. Atualizar `VERSION` e a versão em `pyproject.toml`.
2. Mover alterações de “Unreleased” para a versão datada em `CHANGELOG.md`.
3. Executar validação, testes, build e `git diff --check`.
4. Conferir que wheel e source distribution possuem a mesma versão.
5. Criar tag assinada ou protegida `vX.Y.Z` somente após revisão.
6. Publicar artefatos apenas por pipeline autorizado e com proveniência.

Versões de arquivos de configuração permanecem compatíveis dentro de uma versão major. Mudanças destrutivas exigem migração documentada.

