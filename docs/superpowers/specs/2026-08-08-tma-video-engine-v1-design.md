# TMA Video Engine V1 — Design

## Status

Aprovado conceitualmente pelo usuário em 2026-08-08. Esta especificação transforma a decisão arquitetural em contrato implementável para o `apex-elite-framework`.

## Objetivo

Construir um motor permanente de produção audiovisual da TMA capaz de transformar sequências de artes, fotografias e demais assets aprovados em vídeos premium narráveis, com motion design, trilha, sound design, legendas sincronizadas e exportação multi-formato.

A primeira prova de referência será a série **Anatomia do Torniquete**, composta por capa, Partes 1–8 e CTA final.

## Decisão arquitetural

O motor será integrado ao repositório `matheusflorindo32/apex-elite-framework` em um pacote isolado `packages/tma-video-engine/`.

O AEF permanece responsável por orquestração, Skills, seleção de equipe, checklists, qualidade e governança. O pacote de vídeo será responsável por timeline, composição e renderização. Integrações externas permanecem opcionais e isoladas, em conformidade com `docs/ARCHITECTURE.md`.

A camada científica continua separada no `tropa-scientific-skills` e será acionada somente quando o conteúdo audiovisual fizer afirmações científicas, médicas ou técnicas que exijam auditoria de evidência.

## Princípios obrigatórios

1. **Fidelidade de asset vence estética.** Produtos, logos, diagramas e fotografias marcados como imutáveis não podem ser redesenhados, regenerados ou alterados semanticamente.
2. **Render determinístico.** O mesmo manifesto, assets e versão do motor devem produzir a mesma timeline e composição.
3. **Multi-formato por projeto.** Um único projeto deve gerar 9:16, 4:5, 1:1 e 16:9 sem duplicar conteúdo manualmente.
4. **Áudio em camadas.** Voz, música e SFX são tracks independentes e mixados por regras explícitas.
5. **Legendas seguras.** Captions respeitam safe areas específicas por formato.
6. **QA bloqueante.** Ausência de asset obrigatório, overflow, asset imutável inválido, logo substituída ou configuração responsiva ausente bloqueia o render final.
7. **Sem dependência de IA para render.** IA pode apoiar planejamento/direção, mas a renderização do vídeo deve funcionar localmente sem modelo generativo.
8. **Nenhuma credencial no Git.** Serviços externos opcionais usam variáveis de ambiente e adaptadores isolados.
9. **Uso humano revisável.** O projeto produz preview e evidências de QA; sucesso técnico não substitui inspeção visual final.

## Stack

- Node.js LTS
- TypeScript
- React
- Remotion
- FFmpeg para inspeção, normalização e pós-processamento quando necessário
- Vitest para testes unitários
- Zod para validação de manifestos
- ESLint/TypeScript para qualidade estática
- npm ou pnpm conforme compatibilidade definida no momento da implementação; o pacote não deve interferir no runtime Python atual do AEF

## Estrutura proposta

```text
apex-elite-framework/
├── packages/
│   └── tma-video-engine/
│       ├── package.json
│       ├── tsconfig.json
│       ├── remotion.config.ts
│       ├── src/
│       │   ├── index.ts
│       │   ├── Root.tsx
│       │   ├── compositions/
│       │   │   └── TmaProjectComposition.tsx
│       │   ├── components/
│       │   │   ├── TmaIntro.tsx
│       │   │   ├── TmaScene.tsx
│       │   │   ├── TechnicalCallout.tsx
│       │   │   ├── RedFocusLine.tsx
│       │   │   ├── MacroZoom.tsx
│       │   │   ├── CaptionTrack.tsx
│       │   │   ├── ProductPhoto.tsx
│       │   │   ├── LogoLockup.tsx
│       │   │   └── TmaOutro.tsx
│       │   ├── core/
│       │   │   ├── manifest.ts
│       │   │   ├── timeline.ts
│       │   │   ├── formats.ts
│       │   │   ├── safeAreas.ts
│       │   │   ├── assetPolicy.ts
│       │   │   └── quality.ts
│       │   ├── audio/
│       │   │   ├── mixer.ts
│       │   │   └── loudness.ts
│       │   ├── captions/
│       │   │   ├── schema.ts
│       │   │   └── layout.ts
│       │   ├── director/
│       │   │   ├── presets.ts
│       │   │   └── motion.ts
│       │   └── cli/
│       │       ├── validate.ts
│       │       ├── preview.ts
│       │       └── render.ts
│       ├── projects/
│       │   └── anatomia-torniquete/
│       │       ├── project.json
│       │       ├── captions.json
│       │       └── README.md
│       └── tests/
│           ├── manifest.test.ts
│           ├── timeline.test.ts
│           ├── formats.test.ts
│           ├── safeAreas.test.ts
│           ├── assetPolicy.test.ts
│           └── quality.test.ts
├── skills/
│   ├── video-director/
│   │   └── SKILL.md
│   └── video-quality-auditor/
│       └── SKILL.md
├── workflows/
│   └── tma-video-production.md
├── checklists/
│   └── video-premium-elite.md
└── docs/
    └── TMA_VIDEO_ENGINE.md
```

## Manifesto do projeto

Cada produção é descrita por um manifesto validado por Zod. O arquivo é declarativo e não contém código executável.

Exemplo de contrato:

```json
{
  "id": "anatomia-torniquete",
  "title": "Anatomia do Torniquete",
  "fps": 30,
  "brand": "tma",
  "defaultSceneDurationSec": 6,
  "assets": {
    "logo": {
      "src": "assets/tma-logo.png",
      "policy": "immutable"
    }
  },
  "audio": {
    "voice": "audio/voice.wav",
    "music": "audio/music.wav",
    "musicGainDb": -18,
    "duckingGainDb": -8
  },
  "scenes": [
    {
      "id": "cover",
      "asset": "scenes/00-cover.png",
      "assetPolicy": "immutable",
      "durationSec": 4,
      "motionPreset": "hero-slow-push"
    }
  ],
  "outputs": ["vertical", "portrait", "square", "landscape"]
}
```

## Tipos de asset

### `immutable`

Pode receber somente transformações não destrutivas de composição:

- crop;
- scale uniforme;
- pan;
- zoom;
- máscara;
- opacidade;
- entrada/saída da cena.

Não pode receber:

- geração ou preenchimento generativo;
- distorção de proporção;
- alteração de cor que mude identidade do produto;
- remoção ou criação de partes;
- substituição de logo;
- reconstrução de pixels ausentes.

### `decorative`

Pode receber efeitos visuais mais amplos, desde que não altere informação técnica essencial.

### `generated`

Conteúdo explicitamente sintético e não documental. Nunca pode ser confundido com fotografia real de produto ou evidência técnica.

## Formatos de saída

| Nome | Resolução | Uso principal |
|---|---:|---|
| `vertical` | 1080×1920 | Reels, Shorts, TikTok |
| `portrait` | 1080×1350 | Feed 4:5 |
| `square` | 1080×1080 | Feed, Canva, reutilização |
| `landscape` | 1920×1080 | YouTube, aula, apresentação |

Cada formato possui safe areas próprias para títulos, logo, legendas e CTA.

## Motion system TMA

A V1 deve favorecer movimento técnico e controlado.

Presets mínimos:

- `hero-slow-push`: aproximação lenta de 100% para aproximadamente 106% durante a cena;
- `macro-focus`: zoom para uma região previamente definida sem inventar detalhes;
- `callout-draw`: linha técnica vermelha desenhada progressivamente;
- `title-rise`: título com deslocamento curto e fade;
- `caption-emphasis`: ênfase por bloco de legenda sem karaoke excessivo;
- `clean-cut`: corte seco premium;
- `soft-dissolve`: dissolve curto para transições contextuais.

Transições extravagantes, glitch aleatório, shake excessivo e efeitos que prejudiquem leitura técnica ficam fora da V1.

## Componentes reutilizáveis

### `ProductPhoto`

Renderiza fotografia ou arte aprovada respeitando `assetPolicy`. Deve preservar proporção e impedir deformação acidental.

### `LogoLockup`

Renderiza o arquivo oficial de logo. Para `immutable`, falha se o asset estiver ausente ou se a dimensão/proporção esperada não puder ser preservada.

### `TechnicalCallout`

Desenha linha, marcador e rótulo sobre coordenadas declaradas. Não altera o asset base.

### `MacroZoom`

Aplica pan/zoom para uma região definida por coordenadas normalizadas.

### `CaptionTrack`

Renderiza legendas a partir de timestamps e respeita safe areas de cada formato.

### `TmaIntro` e `TmaOutro`

Padronizam abertura, assinatura visual e CTA sem exigir remontagem manual em cada projeto.

## Timeline

A timeline é derivada do manifesto.

Regras:

1. duração de cena explícita vence o default do projeto;
2. se houver narração temporizada, a cena não pode terminar antes do trecho de voz correspondente;
3. duração final inclui transições sem duplicar frames de forma imprevisível;
4. o cálculo é testável sem iniciar o renderer;
5. a mesma timeline alimenta todos os formatos.

## Áudio

A V1 aceita áudio pré-produzido em WAV ou MP3.

Tracks:

- `voice` — prioridade máxima;
- `music` — trilha de fundo;
- `sfx` — impactos, whooshes discretos e acentos de callout.

Regras mínimas:

- ducking de música durante fala;
- fade-in e fade-out configuráveis;
- ausência de clipping no master;
- voz compreensível em reprodução móvel;
- render deve funcionar sem música ou sem voz quando o manifesto declarar essas faixas como opcionais.

Integração automática com TTS fica fora do núcleo V1. Um adaptador futuro pode gerar a faixa de voz antes da renderização, sem acoplar o core a um fornecedor.

## Legendas

Entrada primária: `captions.json` com blocos temporizados.

Exemplo:

```json
[
  {
    "startMs": 0,
    "endMs": 2200,
    "text": "Conhecer o equipamento é o primeiro passo."
  }
]
```

Regras:

- no máximo duas linhas por bloco no preset padrão;
- largura máxima limitada pela safe area;
- fonte e contraste definidos por tokens TMA;
- nenhuma legenda pode cobrir CTA, logo ou região crítica declarada da imagem;
- overflow bloqueia o gate de qualidade.

## Direção criativa

O `video-director` será uma Skill AEF responsável por converter objetivo, público, duração e assets em decisões de narrativa e motion.

A Skill não renderiza vídeo. Ela define:

- estrutura narrativa;
- ritmo;
- duração aproximada por cena;
- presets de movimento;
- intensidade de SFX;
- prioridade visual;
- CTA;
- riscos de excesso de informação.

O motor consome somente parâmetros explícitos validados no manifesto.

## QA audiovisual

O `video-quality-auditor` aplica o modelo de qualidade já usado pelo AEF.

### Achados críticos

- asset médico/técnico `immutable` substituído, deformado ou semanticamente alterado;
- logo oficial ausente quando obrigatória;
- arquivo de projeto inválido impedindo render;
- output com frames corrompidos ou áudio ausente quando obrigatório.

### Achados altos

- texto ou legenda fora da área segura;
- overflow de texto;
- produto cortado em região declarada como essencial;
- relação de aspecto incorreta;
- narração truncada;
- clipping de áudio;
- cena sem asset obrigatório.

### Achados médios

- contraste insuficiente;
- transição inconsistente;
- ritmo muito acelerado para leitura;
- SFX excessivo;
- redução visível de qualidade sem invalidar conteúdo.

### Achados baixos

- microalinhamentos;
- ajustes cosméticos;
- inconsistências pequenas de espaçamento.

Nenhum achado crítico ou alto pode permanecer no master aprovado.

## Preview e evidência

A CLI do pacote terá três comandos conceituais:

```bash
npm run validate -- --project projects/anatomia-torniquete/project.json
npm run preview -- --project projects/anatomia-torniquete/project.json
npm run render -- --project projects/anatomia-torniquete/project.json --format vertical
```

`validate` não renderiza o vídeo; valida schema, assets, políticas, safe areas e coerência temporal quando possível.

`preview` abre o Remotion Studio para inspeção humana.

`render` produz o master de um formato específico ou todos os formatos declarados.

## Integração com o AEF

O AEF ganhará um tipo de projeto `video` somente se a implementação puder preservar compatibilidade com os tipos atuais.

Equipe padrão recomendada:

- `@Commander` / orquestração quando o projeto for longo;
- `@Design` / direção visual;
- `@VideoDirector` / narrativa e motion;
- `@QA` / gate geral;
- `@VideoQA` / auditoria audiovisual;
- `@Scientific` opcional quando houver afirmações científicas ou médicas.

Os aliases novos devem seguir `docs/CREATING_SKILLS.md`: alias único, função clara e critérios de aprovação explícitos.

## Workflow de produção

```text
brief
  ↓
seleção de assets aprovados
  ↓
classificação immutable/decorative/generated
  ↓
roteiro e direção
  ↓
manifesto validado
  ↓
preview no Remotion Studio
  ↓
QA técnico + inspeção humana
  ↓
render multi-formato
  ↓
QA de masters
  ↓
aprovação/publicação externa
```

Publicação em redes sociais não faz parte da V1.

## Caso de referência: Anatomia do Torniquete

A sequência canônica é:

1. Capa — Anatomia do Torniquete
2. Parte 1 — Marcador integrado
3. Parte 2 — Fita de segurança e marcação de tempo
4. Parte 3 — Fita principal de fixação / hook-and-loop (velcro)
5. Parte 4 — Haste de torção / Windlass Rod
6. Parte 5 — Clipe/trava de retenção / Windlass Clip
7. Parte 6 — Banda interna de alta resistência / High-Strength Internal Band
8. Parte 7 — Fivela de passagem única / Single Routing Buckle
9. Parte 8 — Resumo dos sete componentes
10. CTA — próximo módulo: aplicação do torniquete passo a passo

O projeto deve aceitar as artes aprovadas como assets `immutable`, usar movimentos de câmera não destrutivos e produzir os quatro formatos declarados.

## Critérios de aceite V1

A V1 está concluída somente quando:

1. o manifesto do projeto é validado por schema;
2. um projeto de dez cenas gera timeline determinística;
3. assets `immutable` são protegidos por política testável;
4. as quatro resoluções são registradas e renderizáveis;
5. safe areas diferem por formato e são verificadas;
6. legendas temporizadas são renderizadas sem overflow no fixture de referência;
7. voz, música e SFX podem coexistir no projeto;
8. o master não apresenta clipping detectável no fixture de áudio;
9. o caso `anatomia-torniquete` abre em preview;
10. ao menos um master de referência é renderizado com sucesso em teste de integração/local;
11. testes unitários cobrem manifest, timeline, formatos, safe areas, asset policy e quality gates;
12. documentação explica instalação, validação, preview, render e criação de novo projeto;
13. duas Skills AEF (`video-director` e `video-quality-auditor`) passam pelo validador existente;
14. nenhum teste atual do AEF regride;
15. nenhuma credencial ou asset privado é adicionado ao repositório.

## Fora de escopo da V1

- geração de vídeo por IA;
- alteração generativa de fotografias de produto;
- clonagem de voz;
- integração obrigatória com ElevenLabs, OpenAI, HeyGen ou outro fornecedor;
- publicação automática em Instagram, YouTube ou TikTok;
- editor visual próprio da TMA;
- render distribuído em nuvem;
- banco de dados;
- autenticação de usuários;
- colaboração multiusuário;
- substituição do Canva.

## Segurança, direitos e licenças

- Assets externos mantêm seus próprios direitos e licenças.
- O repositório não deve armazenar conteúdo cuja redistribuição não esteja autorizada.
- O Remotion deve ter sua licença e modalidade de uso verificadas antes de implantação comercial em escala.
- Fotos de produto usadas como referência técnica devem permanecer rastreáveis à origem aprovada do projeto.
- O motor não deve sugerir que conteúdo gerado é fotografia documental real.

## Evolução pós-V1

Ordem recomendada, sem compromisso de implementação na V1:

1. adaptadores de TTS;
2. transcrição e alinhamento automático;
3. biblioteca de presets TMA por tipo de conteúdo;
4. ingestão assistida de assets do Drive;
5. export de projeto para revisão no Canva;
6. pipeline CI para renders de baixa resolução e QA;
7. render em nuvem opcional;
8. catálogo interno de músicas/SFX licenciados.

## Decisões finais

- Repositório: `apex-elite-framework`.
- Unidade de isolamento: `packages/tma-video-engine/`.
- Renderer: Remotion.
- Core determinístico e local.
- Assets técnicos e logos suportam política `immutable`.
- Primeiro projeto: `anatomia-torniquete`.
- Saídas V1: 9:16, 4:5, 1:1 e 16:9.
- Narração: faixa de áudio fornecida ao projeto; TTS automático fica desacoplado.
- Legendas: timestamps estruturados.
- QA: bloqueia críticos e altos conforme o modelo AEF.
- Publicação automática: fora da V1.
