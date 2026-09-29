# Copilot port plan

## Component shape

- Shared layer: upstream-derived `skills/<skill-name>/SKILL.md` files and their local references, scripts, and assets.
- Copilot layer: Agent Plugins 1.0 metadata at `plugin.json`, role agents under `com.github.copilot/agents/`, and the `/poteto-mode` command under `com.github.copilot/commands/`.
- Validation layer: one repeatable script that checks the manifest, all shared skill metadata, nested Markdown links, role agents, attribution artifacts, and unresolved Cursor-only runtime instructions.

## Units and gates

1. Capture upstream commit `adf3218ca2f5b9971eedc07a76bef22df7701539`, file inventory, license, and original content. Gate: the local source copy matches the upstream snapshot.
2. Add the validation script before port changes. Gate: the script ports the recorded upstream source and validates the generated artifact.
3. Convert one skill as the throughput checkpoint. Gate: the shared Agent Skills frontmatter and all its relative references validate.
4. Convert all shared skill metadata and adapt host-specific behavior in bounded batches. Gate: every skill has supported metadata and all local references resolve after each batch.
5. Add Copilot agent profiles and command entry point. Gate: Copilot CLI lists the local plugin and invokes both custom profiles.
6. Update documentation and the adaptation inventory. Gate: installation and testing steps match current Copilot documentation and distinguish verified behavior from unavailable runtime checks.
7. Run structural validation and Copilot CLI checks. Inspect the final package and license.

## Done predicate

The port includes all 47 upstream skill entries, upstream-derived workflow logic, Agent Plugins 1.0 metadata, Copilot CLI agent profiles, `/poteto-mode`, the upstream MIT license, adaptation notes, and GitHub installation instructions. Structural checks and Copilot CLI discovery and profile invocation pass.

## Inventory findings

The upstream package is `pstack` version `0.15.5`, licensed MIT. Its repository inventory has 158 tracked files, 47 skill entry files, and two Cursor agent profiles. Its Cursor plugin manifest is `.cursor-plugin/plugin.json`.

The upstream contains Cursor runtime syntax, paths, tools, and configuration. The port adapts supported workflow behavior for Copilot CLI and omits the Cursor-only automation pack and user guide. See [ADAPTATION.md](ADAPTATION.md) for supported behavior and limits.

## Decision trail

See `decisions.tsv` for evidence-backed choices and unit results.
