# TMA Video Engine V1 — Design

## Status

Design aprovado conceitualmente pelo usuário em 2026-08-08 e consolidado aqui como contrato implementável para o `apex-elite-framework`.

## Objetivo

Construir um motor permanente de produção audiovisual da TMA capaz de transformar sequências de artes, fotografias e demais assets aprovados em vídeos premium narráveis, com motion design, trilha, sound design, legendas sincronizadas e exportação multi-formato.

A primeira prova de referência será a série **Anatomia do Torniquete**, composta por capa, Partes 1–8 e CTA final.

## Decisão arquitetural

O motor será integrado ao repositório público `matheusflorindo32/apex-elite-framework` em um pacote isolado `packages/tma-video-engine/`.

O AEF permanece responsável por orquestração, Skills, seleção de equipe, checklists, qualidade e governança. O pacote de vídeo será responsável por manifesto, timeline, composição, áudio, captions, preview e renderização.

A camada científica continua separada no `tropa-scientific-skills` e será acionada somente quando o conteúdo audiovisual fizer afirmações científicas, médicas ou técnicas que exijam auditoria de evidência.

Integrações externas permanecem opcionais e isoladas, seguindo `docs/ARCHITECTURE.md`.

## Princípios obrigatórios

1. **Fidelidade de asset vence estética.** Produtos, logos, diagramas e fotografias marcados como `immutable` não podem ser redesenhados, regenerados ou semanticamente alterados.
2. **Render determinístico.** O mesmo manifesto, assets, lockfile e versão do motor devem produzir a mesma timeline e composição.
3. **Multi-formato por projeto.** Um único projeto gera 9:16, 4:5, 1:1 e 16:9 sem duplicação manual do conteúdo.
4. **Áudio em camadas.** Voz, música e SFX são tracks independentes, mixados por regras explícitas.
5. **Legendas seguras.** Captions respeitam safe areas específicas por formato.
6. **QA bloqueante.** Ausência de asset obrigatório, checksum inválido, overflow, logo substituída, clipping de áudio ou configuração responsiva inválida bloqueia o master.
7. **Sem IA no caminho obrigatório de render.** IA pode apoiar direção ou planejamento, mas o renderer funciona localmente sem modelo generativo.
8. **Nenhuma credencial no Git.** Serviços opcionais usam variáveis de ambiente e adaptadores isolados.
9. **Inspeção humana permanece obrigatória para master final.** Sucesso técnico não equivale a aprovação visual.
10. **Assets de produção não entram no repositório público por padrão.** Materiais Rhino/TMA reais ficam em workspace local/Drive, com rastreabilidade e política de direitos.

## Stack V1

- Node.js 24 LTS
- pnpm 10
- TypeScript 5.x
- React 19
- Remotion 4.x
- FFmpeg/ffprobe para inspeção e pós-processamento
- Vitest
- Zod
- ESLint

Dependências JavaScript ficam isoladas no pacote `packages/tma-video-engine/` e não alteram o runtime Python do AEF.

## Estrutura proposta

```text
apex-elite-framework/
├── packages/
│   └── tma-video-engine/
│       ├── package.json
│       ├── pnpm-lock.yaml
│       ├── tsconfig.json
│       ├── remotion.config.ts
│       ├── .gitignore
│       ├── src/
│       │   ├── index.ts
│       │   ├── Root.tsx
│       │   ├── compositions/TmaProjectComposition.tsx
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
│       ├── examples/
│       │   └── anatomia-torniquete/
│       │       ├── project.example.json
│       │       ├── captions.example.json
│       │       └── README.md
│       ├── workspace/              # gitignored; assets reais e renders
│       └── tests/
│           ├── manifest.test.ts
│           ├── timeline.test.ts
│           ├── formats.test.ts
│           ├── safeAreas.test.ts
│           ├── assetPolicy.test.ts
│           ├── captions.test.ts
│           ├── audio.test.ts
│           └── quality.test.ts
├── skills/
│   ├── video-director/SKILL.md
│   └── video-quality-auditor/SKILL.md
├── workflows/tma-video-production.md
├── checklists/video-premium-elite.md
└── docs/TMA_VIDEO_ENGINE.md
```

## Manifesto do projeto

Cada produção é descrita por JSON validado por Zod. O manifesto é declarativo e não contém código executável.

Exemplo:

```json
{
  "id": "anatomia-torniquete",
  "title": "Anatomia do Torniquete",
  "fps": 30,
  "brand": "tma",
  "defaultSceneDurationSec": 6,
  "assets": {
    "logo": {
      "src": "workspace/anatomia-torniquete/assets/tma-logo.png",
      "policy": "immutable",
      "sha256": "<hash-calculado-localmente>"
    }
  },
  "audio": {
    "voice": "workspace/anatomia-torniquete/audio/voice.wav",
    "music": "workspace/anatomia-torniquete/audio/music.wav",
    "musicGainDb": -18,
    "duckingGainDb": -8,
    "targetLufs": -14,
    "maxTruePeakDbtp": -1
  },
  "scenes": [
    {
      "id": "cover",
      "asset": "workspace/anatomia-torniquete/scenes/00-cover.png",
      "assetPolicy": "immutable",
      "sha256": "<hash-calculado-localmente>",
      "durationSec": 4,
      "motionPreset": "hero-slow-push"
    }
  ],
  "outputs": ["vertical", "portrait", "square", "landscape"]
}
```

Os valores `sha256` são calculados pelo comando de ingestão/validação local; não são inventados nem preenchidos manualmente em produção.

## Políticas de asset

### `immutable`

Exige checksum SHA-256 e permite somente transformações não destrutivas de composição:

- crop;
- scale uniforme;
- pan;
- zoom;
- máscara;
- opacidade;
- entrada/saída da cena.

É proibido:

- gerar ou preencher pixels;
- distorcer proporção;
- alterar cor de forma que mude identidade de produto/branding;
- remover ou criar partes;
- substituir logo;
- reconstruir componente;
- aplicar filtros que comprometam leitura técnica.

### `decorative`

Aceita efeitos mais amplos, desde que nenhuma informação técnica dependa deles.

### `generated`

Conteúdo explicitamente sintético. Nunca pode ser apresentado como fotografia documental real ou evidência técnica.

## Formatos de saída e safe areas

| Nome | Resolução | Safe area padrão (L/R/T/B) | Uso |
|---|---:|---:|---|
| `vertical` | 1080×1920 | 7.5% / 7.5% / 8% / 20% | Reels, Shorts, TikTok |
| `portrait` | 1080×1350 | 6% / 6% / 6% / 12% | Feed 4:5 |
| `square` | 1080×1080 | 6% / 6% / 6% / 10% | Feed, Canva |
| `landscape` | 1920×1080 | 5% / 5% / 5% / 8% | YouTube, aula |

Safe areas são defaults do motor e podem ser mais restritivas por projeto. Um projeto nunca pode relaxar uma área abaixo de 4% em qualquer lado.

## Motion system TMA

Presets mínimos:

- `hero-slow-push`: zoom linear/suavizado de 100% para 106% ao longo da cena;
- `macro-focus`: pan/zoom para região declarada por coordenadas normalizadas;
- `callout-draw`: linha técnica vermelha desenhada progressivamente;
- `title-rise`: deslocamento vertical curto + fade;
- `caption-emphasis`: ênfase por bloco sem karaoke agressivo;
- `clean-cut`: corte seco;
- `soft-dissolve`: dissolve de 6 a 12 frames.

Ficam fora da V1: glitch aleatório, shake excessivo, transições chamativas sem função narrativa e qualquer efeito que prejudique leitura técnica.

## Componentes reutilizáveis

### `ProductPhoto`

Renderiza fotografia ou arte aprovada respeitando `assetPolicy`, preservando proporção.

### `LogoLockup`

Renderiza o logo oficial e valida checksum/proporção quando `immutable`.

### `TechnicalCallout`

Desenha linha, marcador e rótulo sobre coordenadas declaradas sem alterar o bitmap base.

### `MacroZoom`

Aplica pan/zoom não destrutivo para região definida por coordenadas normalizadas.

### `CaptionTrack`

Renderiza blocos temporizados dentro da safe area do formato.

### `TmaIntro` e `TmaOutro`

Padronizam abertura, assinatura visual e CTA.

## Timeline

Regras determinísticas:

1. duração de cena explícita vence `defaultSceneDurationSec`;
2. cena com narração temporizada não pode terminar antes do bloco de voz associado;
3. transições têm duração explícita em frames;
4. duração final é calculável em função pura, sem iniciar renderer;
5. a mesma timeline semântica alimenta os quatro formatos;
6. arredondamento de tempo para frames usa `Math.round(seconds * fps)` e fica coberto por testes.

## Áudio

Tracks:

- `voice` — prioridade máxima;
- `music` — trilha de fundo;
- `sfx` — impactos e acentos discretos.

Defaults V1:

- target integrado do master: **-14 LUFS ± 1 LU**;
- true peak máximo: **-1 dBTP**;
- ducking padrão da música sob voz: **8 dB**;
- fade-in/out padrão de música: **500 ms**;
- clipping detectado bloqueia o master.

O projeto pode omitir música ou voz quando essas tracks forem explicitamente opcionais.

TTS automático fica fora do core V1. Futuro adaptador pode produzir WAV/MP3 antes do render sem acoplar fornecedor ao motor.

## Legendas

Entrada primária: `captions.json`.

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

- `startMs >= 0`;
- `endMs > startMs`;
- blocos não podem se sobrepor no preset padrão;
- máximo de duas linhas por bloco;
- largura máxima limitada pela safe area;
- nenhum bloco pode cobrir logo, CTA ou região crítica declarada;
- overflow bloqueia QA.

## Direção criativa

A nova Skill `video-director` converte objetivo, público, duração e assets em decisões explícitas de:

- estrutura narrativa;
- ritmo;
- duração aproximada por cena;
- preset de movimento;
- intensidade de SFX;
- prioridade visual;
- CTA;
- risco de excesso de informação.

A Skill não renderiza e não altera assets. O motor consome somente manifesto validado.

## QA audiovisual

A Skill `video-quality-auditor` segue o modelo de severidade do AEF.

### Crítico — bloqueia

- asset técnico/médico `immutable` com checksum divergente;
- logo oficial ausente/substituído quando obrigatório;
- manifesto inválido impedindo render;
- frames corrompidos;
- áudio obrigatório ausente.

### Alto — bloqueia

- texto/legenda fora de safe area;
- overflow;
- produto cortado em região essencial declarada;
- aspect ratio incorreto;
- narração truncada;
- clipping;
- true peak acima de -1 dBTP no master;
- cena sem asset obrigatório.

### Médio

- contraste insuficiente;
- transição inconsistente;
- ritmo excessivamente rápido para leitura;
- SFX exagerado;
- perda visual perceptível sem invalidar conteúdo.

### Baixo

- microalinhamento;
- espaçamento localizado;
- refinamento cosmético.

Nenhum achado crítico ou alto pode permanecer no master aprovado.

## CLI V1

Comandos públicos do pacote:

```bash
pnpm tma-video validate --project workspace/anatomia-torniquete/project.json
pnpm tma-video preview --project workspace/anatomia-torniquete/project.json
pnpm tma-video render --project workspace/anatomia-torniquete/project.json --format vertical
pnpm tma-video render --project workspace/anatomia-torniquete/project.json --all
```

### `validate`

Valida schema, existência de assets, SHA-256, políticas, captions, safe areas declaradas e coerência temporal sem render completo.

### `preview`

Abre Remotion Studio para inspeção humana.

### `render`

Produz um formato ou todos os formatos e executa inspeção de mídia pós-render com ffprobe/FFmpeg.

## Integração com AEF

A V1 adiciona o tipo de projeto `video` preservando os tipos existentes e seus testes.

Equipe padrão:

- `@Commander` quando o projeto for longo;
- `@Design` para direção visual;
- `@VideoDirector` para narrativa/motion;
- `@QA` para gate geral;
- `@VideoQA` para auditoria audiovisual;
- `@Scientific` somente quando houver afirmações científicas/médicas relevantes.

Aliases novos obedecem `docs/CREATING_SKILLS.md`: alias único iniciado por `@`, função/gatilhos claros, responsabilidade e critério de aprovação explícitos.

## Workflow de produção

```text
brief
  ↓
seleção de assets aprovados
  ↓
ingestão local + SHA-256
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
ffprobe/FFmpeg + QA dos masters
  ↓
aprovação humana
```

Publicação em redes sociais fica fora da V1.

## Caso de referência: Anatomia do Torniquete

Ordem canônica:

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

Os PNGs/fotos reais ficam em `workspace/anatomia-torniquete/` ou são montados a partir de Drive localmente. Eles não são commitados no repositório público sem licença/autorização explícita.

O exemplo versionado contém somente manifesto de exemplo, captions de exemplo e instruções de ingestão.

## Critérios de aceite V1

A V1 está concluída somente quando:

1. manifesto é validado por Zod;
2. projeto de 10 cenas gera timeline determinística;
3. `immutable` exige e verifica SHA-256;
4. quatro resoluções são registradas e renderizáveis;
5. safe areas têm defaults exatos e validação;
6. captions temporizadas passam no fixture sem overflow;
7. voice/music/SFX coexistem em composição;
8. inspeção pós-render confirma master em -14 LUFS ±1 e true peak ≤ -1 dBTP no fixture de áudio;
9. caso local `anatomia-torniquete` abre em preview com assets de produção montados fora do Git;
10. ao menos um master de referência é renderizado localmente com sucesso;
11. testes unitários cobrem manifest, timeline, formats, safe areas, asset policy, captions, audio e quality;
12. documentação cobre instalação, ingestão, validate, preview, render e criação de projeto;
13. Skills `video-director` e `video-quality-auditor` passam no validador AEF;
14. tipo `video` entra na seleção do AEF sem regressão dos tipos atuais;
15. `uv run aef validate` e suíte Python existente continuam verdes;
16. nenhuma credencial, foto Rhino ou asset TMA privado é adicionado ao Git;
17. inspeção humana do master de referência não possui achados críticos/altos.

## Fora de escopo da V1

- geração de vídeo por IA;
- image-to-video de produto técnico;
- alteração generativa de fotografias;
- clonagem de voz;
- integração obrigatória com ElevenLabs, OpenAI, HeyGen ou fornecedor específico;
- publicação automática em Instagram, YouTube ou TikTok;
- editor visual próprio;
- render distribuído em nuvem;
- banco de dados;
- autenticação;
- colaboração multiusuário;
- substituição do Canva.

## Segurança, direitos e licenças

- Assets externos mantêm seus próprios direitos e licenças.
- O repositório público não armazena material cuja redistribuição não esteja autorizada.
- A licença e modalidade de uso do Remotion devem ser verificadas antes de implantação comercial em escala.
- Fotos de produto usadas tecnicamente permanecem rastreáveis à origem aprovada.
- Conteúdo `generated` é rotulado e nunca apresentado como fotografia documental.
- Workspaces de produção são gitignored.

## Evolução pós-V1

1. adaptadores de TTS;
2. transcrição/alinhamento automático;
3. presets TMA por tipo de conteúdo;
4. ingestão assistida a partir do Google Drive;
5. export de projeto para revisão no Canva;
6. render de preview em CI;
7. render em nuvem opcional;
8. catálogo interno de músicas/SFX licenciados.

## Decisões finais vinculantes

- Repositório: `apex-elite-framework`.
- Pacote isolado: `packages/tma-video-engine/`.
- Node: 24 LTS.
- Package manager: pnpm 10.
- Renderer: Remotion 4.x.
- Core determinístico e local.
- `immutable` exige SHA-256.
- Primeiro caso: `anatomia-torniquete`.
- Saídas: 1080×1920, 1080×1350, 1080×1080 e 1920×1080.
- Áudio master: -14 LUFS ±1; true peak ≤ -1 dBTP.
- Narração: arquivo fornecido ao projeto; TTS desacoplado.
- Legendas: timestamps estruturados.
- QA: críticos e altos bloqueiam.
- Assets reais de produção: fora do Git público por padrão.
- Publicação automática: fora da V1.
