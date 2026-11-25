# International engineering benchmark

On 2026-11-25 we retrieved each public repository, default-branch commit, README, license metadata and root license filenames from GitHub. Each source below points to the inspected revision. Maintenance signals describe archive state and recent repository activity. They do not measure reliability, scientific validity or production adoption.

| Reference and inspected documentation | License at repository level | Maintenance signal (last push, UTC) | Principle applied to APEX review |
|---|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills/blob/83021e2be457a9b6679148719c1f6074f0ad975e/README.md) | Apache-2.0 | Open, 2026-11-04 | Publish a portable SKILL.md with a clear activation description. |
| [openai/openai-agents-python](https://raw.githubusercontent.com/openai/openai-agents-python/4e162c79a4a951c6fc8b698d5c8279c1963c099b/README.md) | MIT | Open, 2026-11-25 | Separate orchestration responsibilities and document handoffs. |
| [langchain-ai/langgraph](https://raw.githubusercontent.com/langchain-ai/langgraph/f96105368f9e9385d4c9e38bffaa457aba17f095/README.md) | MIT | Open, 2026-11-25 | State explicit stop and review conditions before repeating a step. |
| [microsoft/autogen](https://github.com/microsoft/autogen/blob/8390985108cb1e3881f5f7297765758d8ad2540c/README.md) | MIT (code), CC-BY-4.0 (documentation) | Archived, 2026-11-12 | Explain project lifecycle and migration paths to readers. |
| [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai/blob/a30f0264d760c5904d688f01115c63fe757c2ca9/README.md) | MIT | Open, 2026-11-25 | Describe expected outputs as structured data and validate them. |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk/blob/77001c96f9507be0f4d009b83210a384a5e08bda/README.md) | MIT | Open, 2026-11-17 | Treat a protocol adapter as a separately tested integration. |
| [astral-sh/uv](https://github.com/astral-sh/uv/blob/e3e7c1eacb980339352a5ad69affcd3b6c206c92/README.md) | Apache-2.0 OR MIT | Open, 2026-11-24 | Document locked development dependencies and clean installation. |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/blob/c21d13b3cc2894680229ba9959a53281acb9200e/README.md) | MIT | Open, 2026-11-23 | Expose specialty selection, prerequisites and evidence requirements. |
| [huggingface/hub-docs](https://github.com/huggingface/hub-docs/blob/e3687a9b163f24acb44ef8dd1f4293cb7431826c/README.md) | Apache-2.0 | Open, 2026-11-25 | Provide task-oriented entry points and an authoritative source for each guide. |
| [ollama/ollama](https://github.com/ollama/ollama/blob/924cc286cc592f49c481fa84e15fa60dbc75989e/README.md) | MIT | Open, 2026-11-24 | Distinguish local execution from hosted model access. |

## Decisions

- Keep the skill directory and its human-readable description as the unit of discovery. APEX aliases belong to its catalog. Host discovery and invocation require separate verification.
- Keep routing, specialist output and review distinct. A plan can identify a reviewer without claiming that an independent reviewer actually ran.
- Distribute inspectable Markdown and use checksums for provenance. Keep external scientific tools, MCP servers and hosted runtimes outside the core dependency chain.
- Use a clean environment outside the source tree to exercise the installed distribution. A successful test run from a checkout alone cannot demonstrate package-data completeness.

These references informed design criteria. Their licenses cover their respective repositories and may differ for bundled assets, datasets and individual skills. This comparison imports no upstream implementation or media.
