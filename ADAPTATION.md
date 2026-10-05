# Porting and adaptation notes

This package adapts the upstream P-Stack plugin for GitHub Copilot Chat in VS Code and VS Code Insiders, and for GitHub Copilot CLI. The source snapshot is `cursor/plugins/pstack` at commit `adf3218ca2f5b9971eedc07a76bef22df7701539` (version 0.15.5). The upstream MIT license, logo, 47 skill entry files, and their nested references, playbooks, and scripts are included. Common workflow intent follows upstream; host-specific workflows are adapted, documented as unavailable, or given a fallback. This is not the official Cursor plugin.

## Component layout

- `skills/` contains shared Agent Skills 1.0 directories and references.
- `com.github.copilot/agents/` contains Copilot profiles for `poteto-agent` and `comment-sicko`, corresponding to the upstream P-Stack agent roles.
- `com.github.copilot/commands/poteto-mode.md` exposes `/poteto-mode` in Copilot Chat for VS Code and VS Code Insiders, and in Copilot CLI.
- Root `plugin.json` uses the Agent Plugins 1.0 schema. It has no legacy component path fields.

## Host adaptations

| Upstream host construct | Copilot adaptation |
| --- | --- |
| Cursor plugin manifest and agent profiles | Agent Plugins 1.0 `plugin.json` plus Copilot namespaced agent profiles. |
| Upstream delegation requests | Shared skills state delegation intent and expected results. Copilot agent and delegation features vary by client and version. Use only the named-agent, subagent, background execution, remote environment, model routing, and read-only controls the active client actually exposes. |
| Upstream structured questions | Ask the user through the active Copilot client's interaction features. |
| Cursor skill and model-rule paths | Skill paths use Copilot's `.github/skills/` and `~/.copilot/skills/` conventions. Model-rule references become model preferences rather than implying a Cursor rule file exists in Copilot. |
| Cursor webhook routines and secret requests | Copilot does not provide Cursor's `update_state` routine creation or `SendToUser` secret-request flow. `make-bot-ui` now integrates only with an existing, user-provided webhook service and does not invent a Copilot endpoint. |
| `/loop`, cloud agents, transcripts, and client status | Use only session, agent, and automation controls exposed by the active client. Copilot CLI documents `/chronicle` and local session history; other clients have their own session UI and may not expose raw transcripts. No scheduled wake service or transcript file layout is assumed. |
| Optional upstream tools | The bundled `unslop` skill covers prose cleanup. Use the terminal, browser, and other tools exposed by the active Copilot client. This package does not bundle external MCP servers or browser-control services. |
| Graphite stack operations | `orchestrate` requires the Graphite CLI because its frontier commands use Graphite stack metadata. Autopilot workflows and other PR playbooks use the resolved forge and do not require Graphite. |
| Bugbot review markers | The watcher recognizes Bugbot authors and Copilot-authored automation markers case-insensitively. Ordinary Copilot comments do not count as Bugbot reviews. |
| Skill frontmatter | Portable Agent Skills fields are validated against the open standard. VS Code's documented `argument-hint`, `user-invocable`, and `disable-model-invocation` extensions are allowed where used; do not assume every Copilot client honors them. |

The package retains host-neutral workflow ideas such as parallel review, validation gates, and decision trails. Copilot features depend on the client, version, account, and configuration. The plugin does not bundle remote workers, scheduled wake services, or external browser controls. Some Copilot clients provide session history, but raw transcript access is not portable. When a required feature is unavailable, use a sequential workflow where possible or report the blocked step. JetBrains supports Agent Skills in preview, but this repository has not verified the Agent Plugins package, its agents, or its commands in JetBrains.

## Role and model selection

The upstream roles map to the Copilot `poteto-agent` profile for `/poteto-mode` work and `comment-sicko` for read-only comment review. The command routes through `poteto-agent` and does not substitute `general-purpose`. The `poteto-agent` profile preserves the upstream instruction to resume an existing owner when session resumption is available. Loading the profile alone cannot resume a session. Other workflows can use Copilot's built-in or configured agents when available. Review an agent's tool access and output before accepting its work.

The upstream snapshot names model slugs and assumes per-role model configuration. Copilot availability and model identifiers depend on the account, client, and configuration. Treat those upstream defaults as examples, not guaranteed valid Copilot model names. Choose a model exposed by the active Copilot client, or let Copilot select automatically. The `/setup-pstack` skill recommends per-role preferences, but those mappings are advisory and cannot make an unavailable model selectable or enforce per-role routing.

## Verification status and limits

`python scripts/port_upstream.py --validate` checks package structure and relative Markdown links. Copilot CLI 1.0.89 discovered the local plugin and its skills. Noninteractive profile invocations succeeded for both bundled agents. The `/poteto-mode` command read the workflow and returned its first non-negotiable. The comment reviewer returned its required first output. The user has also confirmed that the plugin works in Copilot Chat in VS Code. VS Code and Insiders use the documented Agent Plugins 1.0 package format; Insiders has not been separately recorded as tested. JetBrains support for Agent Skills is in preview, and this package's JetBrains plugin installation and Copilot-specific components are unverified.
