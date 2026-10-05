# Copilot port plan

## Component shape

- Shared layer: upstream-derived `skills/<skill-name>/SKILL.md` files and their local references, scripts, and assets.
- Copilot layer: Agent Plugins 1.0 metadata at `plugin.json`, role agents under `com.github.copilot/agents/`, and the `/poteto-mode` command under `com.github.copilot/commands/`. VS Code Copilot Chat and Copilot CLI consume the package; IDE-specific capabilities vary.
- Validation layer: repeatable checks for the manifest, standard Agent Skills metadata plus documented VS Code extensions, Markdown links, role agents, attribution artifacts, and known Cursor-only runtime syntax.

## Units and gates

1. Capture upstream commit `adf3218ca2f5b9971eedc07a76bef22df7701539`, file inventory, license, and original content. Gate: the local source copy matches the upstream snapshot.
2. Add the validation script before port changes. Gate: the script ports the recorded upstream source and validates the generated artifact.
3. Convert one skill as the throughput checkpoint. Gate: the shared Agent Skills frontmatter and all its relative references validate.
4. Convert all shared skill metadata and adapt host-specific behavior in bounded batches. Gate: every skill has supported metadata and all local references resolve after each batch.
5. Add Copilot agent profiles and command entry point. Gate: Copilot CLI discovers the local plugin and invokes both custom profiles; VS Code Copilot Chat discovers the package and exposes its skills, agents, and command.
6. Update documentation and the adaptation inventory. Gate: installation and testing steps match current Copilot documentation and distinguish verified behavior from unavailable runtime checks.
7. Run structural validation and Copilot CLI checks. Verify the package in VS Code Copilot Chat and record any client-specific gaps. Inspect the final package and license.

## Done predicate

The port includes all 47 upstream skill entries, adapted workflow intent with host limitations and fallbacks, Agent Plugins 1.0 metadata, Copilot agent profiles, `/poteto-mode`, the upstream MIT license, adaptation notes, and installation instructions for VS Code Copilot Chat and Copilot CLI. Structural checks and CLI discovery and profile invocation pass. The user confirmed the plugin works in VS Code Copilot Chat. JetBrains plugin-package support is not claimed; its Agent Skills feature is in preview.

## Inventory findings

The upstream package is `pstack` version `0.15.5`, licensed MIT. Its repository inventory has 158 tracked files, 47 skill entry files, and two Cursor agent profiles. Its Cursor plugin manifest is `.cursor-plugin/plugin.json`.

The upstream contains Cursor runtime syntax, paths, tools, and configuration. The port adapts supported workflow behavior for VS Code Copilot Chat and Copilot CLI and omits the Cursor-only automation pack and user guide. See [ADAPTATION.md](ADAPTATION.md) for supported behavior and limits.

## Compatibility audit

The audit found and corrected several implicit host assumptions beyond literal Cursor paths. `make-bot-ui` no longer fabricates a Copilot webhook URL or relies on Cursor-only routine and secret-request APIs; it requires an existing provider endpoint. Skills that previously assumed a workspace transcript directory now use only session history exposed by the active client. The worktree audit no longer treats transcript recency as evidence that a worktree is or is not in use. Personal skill paths now use `~/.copilot/skills/`.

Copilot CLI documents `/chronicle` and session storage under `~/.copilot/session-state/`. VS Code supports the `argument-hint`, `user-invocable`, and `disable-model-invocation` skill extensions. CLI behavior for those VS Code-only fields is not claimed. Model selection, delegation, session resumption, and automation remain conditional on the active client's exposed capabilities.

## Decision trail

See `decisions.tsv` for evidence-backed choices and unit results.
