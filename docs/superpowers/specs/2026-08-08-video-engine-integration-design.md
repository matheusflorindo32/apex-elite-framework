# Generic Video Engine Integration — Design

## Status

Approved architectural direction for the public `apex-elite-framework`: the AEF remains a generic orchestrator and does **not** contain brand-specific video engine implementation, proprietary assets, partner media, or production masters.

## Goal

Add a generic audiovisual project contract to AEF so external/private video engines can be orchestrated through Skills, workflows, checklists, and QA without coupling the public framework to a specific brand, renderer, or asset library.

## Public/private boundary

### Public AEF may contain

- generic project type `video`;
- generic Skills such as `video-director` and `video-quality-auditor`;
- generic audiovisual QA criteria;
- generic contracts for manifests, safe areas, captions, asset policies, and render evidence;
- generic integration interface under `integrations/video-engine/`;
- documentation describing how an external engine registers capabilities and returns evidence.

### Public AEF must not contain

- brand-specific motion packages;
- proprietary logos or media;
- partner/product image libraries;
- private production manifests containing asset locations;
- production masters, voice tracks, music stems, or licensed media;
- credentials, tokens, or private storage references;
- implementation details that are unnecessary for the generic integration contract.

## External engine contract

A private engine may expose a local CLI or adapter implementing these conceptual operations:

```text
validate(project)
preview(project)
render(project, format|all)
audit(output)
```

The AEF integration does not perform rendering itself. It prepares plans, checks prerequisites, invokes the approved adapter when available, and records evidence returned by the adapter.

## Generic asset policies

The public contract recognizes three policy classes:

- `immutable`: source media may only receive non-destructive composition transforms such as proportional scale, crop, pan, zoom, mask, opacity, and scene entrance/exit;
- `decorative`: broader visual effects are allowed when they do not carry factual or technical meaning;
- `generated`: explicitly synthetic material that must not be represented as documentary evidence or an original source asset.

Checksum verification is recommended for `immutable` assets, but storage locations and hashes for private productions remain outside the public repository.

## Generic output profiles

The public interface recognizes common output profiles without prescribing a specific renderer:

| Profile | Resolution | Typical use |
|---|---:|---|
| `vertical` | 1080x1920 | Reels / Shorts |
| `portrait` | 1080x1350 | 4:5 feed |
| `square` | 1080x1080 | square social / editing |
| `landscape` | 1920x1080 | YouTube / lessons |

Projects may define stricter safe areas than the defaults supplied by their private engine.

## Skills

### `video-director`

Produces an explicit audiovisual direction brief containing narrative structure, pacing, scene duration targets, motion intensity, caption strategy, sound design guidance, CTA strategy, and risks of information overload. It does not modify assets or render media.

### `video-quality-auditor`

Applies AEF severity rules to audiovisual evidence. Critical/high findings include missing mandatory media, invalid immutable-asset evidence, unreadable or overflowing captions, wrong aspect ratio, truncated narration, corrupted frames, or audio clipping when those checks are available from the external engine.

## Integration boundary

Suggested public structure:

```text
apex-elite-framework/
├── skills/
│   ├── video-director/SKILL.md
│   └── video-quality-auditor/SKILL.md
├── workflows/video-production.md
├── checklists/video-quality.md
├── integrations/video-engine/
│   ├── README.md
│   └── contract.json
└── docs/VIDEO_ENGINE_INTEGRATION.md
```

Brand-specific engines live in separate private repositories and depend on this contract conceptually, not by copying proprietary assets into AEF.

## Quality and security

1. The AEF must preserve its existing Python runtime and existing project types.
2. Any external engine integration is optional and isolated.
3. No credential is committed to Git.
4. Public documentation uses synthetic/example paths only.
5. Human review remains required for final audiovisual approval.
6. High-risk technical/medical content may additionally invoke domain-specific scientific/evidence Skills.
7. Publishing to social platforms is outside this integration contract.

## Acceptance criteria

- AEF can classify a request as `video` without breaking existing project types.
- A generic video team can be selected using documented aliases.
- A generic checklist and workflow exist.
- An external/private engine can implement the documented adapter contract without exposing its internal code or assets publicly.
- No brand-specific production asset or private path is present in the public repository.
