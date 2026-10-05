---
name: reflect
description: Review the current conversation for durable learnings, surface evidence, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Capture the current conversation

Use the current conversation already available to the parent. For prior sessions, use only history features exposed by the active Copilot client. Copilot CLI supports `/chronicle search`; other clients may provide a session-history UI. If the client does not expose the transcript, do not guess its location or search another workspace. Pass a concise digest of the available conversation to reviewers and state when historical context was unavailable.

### 2. Spawn three reviewers in parallel

Request three reviewers together through the active host's delegation feature, using general-purpose workers where that profile is selectable. Reviewers need access to available MCP tools for context lookups (tickets, chat threads, observability traces referenced in the transcript). Use read-only access if it includes those tools; otherwise keep reviewers instructed not to write. If delegation is unavailable, work through the lenses sequentially and report that limitation.

Each reviewer and the synthesizer name a role line in the available Copilot model preferences and a default. Use that model only when the active host supports it. For `auto` or `inherit-parent`, use the host's automatic or parent model. When a preference is unavailable, use the closest supported option and note the substitution.

| Lens | Role line | Default `model` | Prompt template |
|---|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `claude-opus-5-5-max` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `gpt-5.6-sol-max` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `claude-opus-5-5-max` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `subagent` response body.

### 3. Synthesize

Request one general-purpose subagent to synthesize the findings when available, using the `reflect judgment, divergent, synthesizer` preference (default `claude-opus-5-5-max`) when model selection is supported. The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): use the active client's documented skill-authoring feature when available; otherwise follow the Agent Skills format directly.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): use the active client's documented skill-authoring feature when available, or edit the description directly and validate it.
- `new skill via Agent Skills format: <kebab-name>`: use the active client's documented creation feature when available; otherwise author the files directly. Do not assume a built-in authoring workflow exists.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
