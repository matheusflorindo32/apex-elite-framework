# Compatibility by delivery method

Official documentation was retrieved on 2026-11-25. Every host below is **untested with this APEX candidate**. “Native skills” describes a discovery mechanism documented by the host. Availability depends on client version, account, policy and selected agent. The local Python CLI performs planning independently of these products.

| Host | Documented or proposed route | Procedure for an evaluation | Evidence |
|---|---|---|---|
| ChatGPT | Upload or paste | Attach the knowledge Markdown if the interface accepts it, or paste a single workflow. | [Official documentation](https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt) |
| GPTs | Upload and instructions | Put behavior in Instructions and attach the knowledge document in the builder. | [Official documentation](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts) |
| Codex | Native skills | Use the Codex setup guide and verify that the client lists the installed skill. | [Official documentation](https://learn.chatgpt.com/docs/build-skills) |
| Claude | Upload or paste | Attach the knowledge Markdown or paste the relevant section into a conversation. | [Official documentation](https://support.claude.com/en/articles/8241126-upload-files-to-claude) |
| Claude Code | Native skills | Install a skill directory using the documented project or user skill location. | [Official documentation](https://code.claude.com/docs/en/skills) |
| Gemini | Upload or paste | Use a supported attachment or paste the small workflow directly. | [Official documentation](https://support.google.com/gemini/answer/14903178) |
| Gemini CLI | Native skills | Follow the CLI discovery instructions for an individual skill directory. | [Official documentation](https://geminicli.com/docs/cli/skills/) |
| GitHub Copilot | Native skills in supported agents | Use a documented repository skills location. Confirm the selected Copilot surface supports skills. | [Official documentation](https://docs.github.com/en/copilot/concepts/customizations/agent-skills) |
| Cursor | Native skills | Follow the editor’s documented skills discovery convention. | [Official documentation](https://cursor.com/docs/skills) |
| VS Code | Native skills in agent-enabled chat | Check the installed agent and its skill discovery configuration. | [Official documentation](https://code.visualstudio.com/docs/agent-customization/agent-skills) |
| Ollama | Local instructions, experimental | Use a small excerpt in the prompt or SYSTEM instruction. Select an installed model. | [Official documentation](https://docs.ollama.com/modelfile) |
| LM Studio | Local chat instructions, experimental | Paste a small workflow into a chat with a loaded model. | [Official documentation](https://lmstudio.ai/docs/app/basics/chat) |
| PocketPal AI | Local mobile instructions, experimental | Paste one workflow into chat. Device memory and model context constrain input size. | [Official documentation](https://github.com/a-ghorbani/pocketpal-ai) |
| Standard | Other Agent Skills hosts, experimental | Check the host’s supported specification version, resource paths and discovery rules. | [Official documentation](https://agentskills.io/specification) |

## What the artifacts establish

A skill contains a directory and a SKILL.md with name and description. The portable knowledge document supplies context to a model. Aliases such as `@EPO` identify catalog roles. An assistant can interpret one after receiving the catalog. A host-specific command, tool registration or API invocation requires separate evidence.

APEX provides no supported host API adapter or MCP server in this release. Local-model suggestions are experimental. Their evaluation requires a model that fits the available device, an adequate context window and a user review of the response.

## Reproducible host check

1. Record the product, exact client version, model, date, delivery method and enablement settings. Use public example data.
2. For native discovery, install one skill per the official guide and confirm that the client displays its registered name and description. For upload, confirm the attachment is readable by asking for a named checklist item.
3. Ask for a one-page lesson plan with one learning objective and one assessment. Record the selected role, output, acceptance criteria and any missing context.
4. Record discovery and task completion separately. Attach a sanitized transcript before upgrading a host to verified. A fluent answer alone cannot demonstrate native discovery.
