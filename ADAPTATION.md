# Porting and adaptation notes

This is a GitHub Copilot CLI compatibility port of the upstream P-Stack plugin. The source snapshot is `cursor/plugins/pstack` at commit `adf3218ca2f5b9971eedc07a76bef22df7701539` (version 0.15.5). The upstream MIT license, logo, 47 skill entry files, and their nested references, playbooks, and scripts are preserved. Skill names, descriptions, and workflow substance follow upstream; metadata and host-specific directions are adapted. This is not the official Cursor plugin.

## Component layout

- `skills/` contains shared Agent Skills 1.0 directories and references.
- `com.github.copilot/agents/` contains Copilot profiles for `poteto-agent` and `comment-sicko`, corresponding to the upstream P-Stack agent roles.
- `com.github.copilot/commands/poteto-mode.md` exposes `/poteto-mode` in Copilot CLI.
- Root `plugin.json` uses the Agent Plugins 1.0 schema. It has no legacy component path fields.

## Host adaptations

| Upstream host construct | Copilot adaptation |
| --- | --- |
| Cursor plugin manifest and agent profiles | Agent Plugins 1.0 `plugin.json` plus Copilot namespaced agent profiles. |
| Upstream delegation requests | Shared skills state delegation intent and expected results. Copilot CLI uses its task tool and named agents. Use background execution, remote environments, model routing, and read-only access only when the CLI supports them. |
| Upstream structured questions | Ask the user through the active Copilot CLI interaction feature. |
| Cursor skill and model-rule paths | Skill paths use Copilot's `.github/skills/` and `~/.copilot/skills/` conventions. Model-rule references become model preferences rather than implying a Cursor rule file exists in Copilot. |
| `/loop`, cloud agents, transcripts, and client status | Reworded as client session/automation controls, Copilot agents/session status, or workspace-scoped transcript access. A feature with no equivalent remains a documented host limitation. |
| Optional upstream tools | The bundled `unslop` skill covers prose cleanup. Use available CLI and browser tools for checks. This package does not bundle external MCP servers or browser-control services. |
| Graphite stack operations | `orchestrate` requires the Graphite CLI because its frontier commands use Graphite stack metadata. Autopilot workflows and other PR playbooks use the resolved forge and do not require Graphite. |
| Bugbot review markers | The watcher recognizes Bugbot authors and Copilot-authored automation markers case-insensitively. Ordinary Copilot comments do not count as Bugbot reviews. |
| Cursor skill frontmatter | Converted to Agent Skills `name` and `description` metadata; unsupported Cursor-only metadata is removed. |

The port retains host-neutral workflow ideas such as parallel review, validation gates, and decision trails. Copilot CLI features depend on the installed CLI version, account, and configuration. The skills do not provide remote workers, transcript stores, scheduled wake services, or external browser controls. When a required feature is unavailable, use a sequential workflow where possible or report the blocked step.

## Role and model selection

The upstream roles map to the Copilot `poteto-agent` profile for `/poteto-mode` work and `comment-sicko` for read-only comment review. The command routes through `poteto-agent` and does not substitute `general-purpose`. The `poteto-agent` profile preserves the upstream instruction to resume an existing owner when session resumption is available. Loading the profile alone cannot resume a session. Other workflows can use Copilot's built-in or configured agents when available. Review an agent's tool access and output before accepting its work.

The upstream snapshot names model slugs and assumes per-role model configuration. Copilot availability and model identifiers depend on the account, client, and current CLI configuration. Treat those upstream defaults as examples, not guaranteed valid Copilot model names. Choose a model exposed by the active Copilot client, or let Copilot select automatically. The `/setup-pstack` skill recommends per-role preferences, but those mappings are advisory and cannot make an unavailable model selectable or enforce per-role routing.

## Verification status and limits

`python scripts/port_upstream.py --validate` checks package structure and relative Markdown links. Copilot CLI 1.0.89 discovered the local plugin and its skills. Noninteractive profile invocations succeeded for both bundled agents. The `/poteto-mode` command read the workflow and returned its first non-negotiable. The comment reviewer returned its required first output. These checks verify the package in Copilot CLI; they do not cover other clients.
