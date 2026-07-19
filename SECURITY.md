# Política de Segurança

## Relato

Não abra issue pública para vulnerabilidades ainda não corrigidas. Ao publicar o repositório, configure um canal privado de security advisory e atualize este documento com o contato responsável.

Até existir canal oficial, não envie credenciais, dados pessoais, documentos sigilosos ou detalhes exploráveis. Registre somente uma descrição mínima e aguarde um meio privado confirmado pelo mantenedor.

## Escopo

O core local não chama APIs nem executa ações remotas. Vulnerabilidades relevantes incluem traversal ou sobrescrita involuntária, validação que aprove estrutura inválida, exposição de conteúdo sensível e configuração de CI com permissões excessivas.

## Princípios

- privilégio mínimo;
- entradas externas tratadas como não confiáveis;
- segredos fora do repositório e dos logs;
- aprovação humana para efeitos críticos;
- correções acompanhadas por teste de regressão;
- divulgação coordenada após mitigação.

