---
name: recall
description: Reconstruct recent working context from Copilot session history, live repository state, GitHub work items, and available project records, then return a tight current-state brief. Use for "recall my work on X", "catch me up", "what have I been working on", "where did I leave off", or before resuming work in a new session.
user-invocable: true
disable-model-invocation: true
argument-hint: "[topic or time window]"
---

# Recall

Before you start or resume work, rebuild the user's recent working context and return a tight capsule of where the work stands now and what to do next.

Keep the result tight and on-topic. Read only the context needed to answer the request, then stop.

## Context sources

Copilot provides session history for previous Copilot CLI and GitHub Copilot app sessions. Copilot stores complete locally run session records under `~/.copilot/session-state/` and maintains a session store that powers session-history queries and `/chronicle`. Prefer those native session-history capabilities over hard-coded transcript paths or file-name assumptions.

Use four evidence layers:

1. **Session history.** What the user and Copilot discussed, decided, attempted, changed, and left unfinished.
2. **Live repository state.** The current branch, worktree, files, tests, commits, and local changes.
3. **GitHub work state.** Pull requests, issues, reviews, and other artifacts surfaced by the work.
4. **Project records.** Documentation, issue trackers, chat, incident records, error tracking, and other connected sources that are actually available in the current environment.

Do not claim access to a source that is not available.

## Workflow

### 1. Classify the request

Determine whether this is recall or another task.

- Resuming one specific prior session is **session pickup**, not recall.
- Turning repeated behavior into a durable instruction is **automate-me**, not recall.
- Asking how a subsystem works is **how** or **teach**, not recall.
- Recall reconstructs recent working context across sessions and current state.

If the user already supplied a complete state capsule containing the relevant paths, branch, changes, and next step, use it and skip unnecessary mining.

### 2. Lock the scope

Before searching, determine:

- **Workspace:** default to the active repository or workspace.
- **Topic:** use the named feature, file, subsystem, bug, branch, or project.
- **Time window:** "recent" means the last 7 days unless the user specifies another range.

State the scope briefly before doing the work.

Never silently turn "all my work" into a smaller window. If the user says "all", search all available relevant session history and state any platform limits.

Never inspect another repository's session history unless the user asks for it.

### 3. Mine Copilot session history first

Use Copilot's native session-history capability.

Prefer:

- `/chronicle search <topic>` for direct topic search.
- A natural-language question about previous sessions when semantic reconstruction is needed.
- Session resume/history features when a specific prior session must be inspected.

Search with the topic plus repository name, branch, file name, or other identifiers when available. Copilot session-history search is not limited to the current repository, so filter the candidates back to the requested workspace before using them.

When the system exposes multiple matching sessions, process them in chronological order using their actual session timestamps. Do not infer recency from session IDs.

Skip the current session and obvious noise such as subagent, evaluation, and test-only sessions when they do not contribute to the requested work.

For one or two matching sessions, inspect them directly. For many sessions, split the candidate set across fresh subagents if subagent delegation is available.

Each investigator returns the same schema for every relevant session:

```text
Session: <session id>
Date: <timestamp>
Topic: <topic>
Goal: <user goal>
Decisions: <important decisions>
Open threads: <unfinished work>
Struggles/corrections: <failed attempts and corrections>
Artifacts: <PRs, issues, branches, files>
Evidence: <session id and relevant excerpt or locator>
```

Keep raw session content inside the investigators. Return only findings to the main thread.

Do not invent a filesystem layout such as `~/.copilot/projects/.../agent-transcripts/...`. Copilot's current documented storage model is `~/.copilot/session-state/` plus the local session store.

### 4. Sweep project records for a named target

Whenever the topic names a feature, file, subsystem, area, bug, PR, or issue, inspect the other available records that could change the current state.

If a `why` skill exists in the environment, delegate the historical/context sweep to it, but change the question from:

> Why was this built this way?

to:

> What is the current state, what was tried, what failed or was reverted, and what problems are still being reported?

Reuse the source-specific investigators and tools provided by that skill when they are available.

Otherwise, use the available GitHub, repository, issue-tracker, chat, documentation, and incident/error-tracking tools directly.

Run independent source investigations in parallel when that reduces latency and the environment supports parallel delegation.

Treat a null result as a finding. If a source is unavailable, say so rather than silently treating it as empty.

For pure activity recall with no named target, such as "what did I do this week", session history plus live state are normally sufficient unless the user asks for external records.

### 5. Verify against live state

Use the current repository as the authority for what exists now.

Check, as relevant:

```text
 git status
 git branch --show-current
 git log --oneline -n <small number>
```

Then verify surfaced PRs and issues with the available GitHub tools or `gh`.

Do not trust a previous session's claim that a change shipped if the current repository or GitHub state says otherwise.

When the answer depends on exactly what an agent did, which files it read, which commands it ran, or which error it saw, inspect the full relevant session rather than relying only on a short summary.

### 6. Reconcile contradictions

Prefer evidence in this order:

```text
Current repository/GitHub state
        ↓
Recent session evidence
        ↓
Older session evidence
        ↓
Unverified claims
```

When two sources disagree, report the conflict briefly and prefer the newer verified state.

Do not hide uncertainty.

### 7. Write the recall brief

Group the answer by work thread and use the output contract below.

Stay on the named topic. Keep adjacent work out unless it blocks the requested work.

## Output contract

Lead with the capsule, then thread status, then problems, then the next move.

**Capsule.** At most 5 bullets. State what the work is and where it stands overall.

**Threads.** One line per relevant thread, prefixed with exactly one status tag:

- `[merged #N]`
- `[open PR #N]`
- `[in flight <branch>]`
- `[verified, uncommitted]`
- `[reverted #N]`
- `[planned, not started]`

A thread without a status tag is incomplete.

**Problems.** At most 5 recurring problems. Include user-reported symptoms, failed attempts, fixes that shipped and were reverted, and unresolved errors that affect the next attempt.

**Next move.** State one concrete, highest-value next action.

## Evidence and privacy

Cite session findings with the session ID or the strongest session-history locator available.

Cite repository findings with file paths, commit IDs, or command output when useful.

Cite GitHub findings with PR numbers, issue IDs, or links when available.

Cite external source findings with the source's own stable identifier or link.

Never fabricate a citation, permalink, session ID, PR, issue, or error-tracker reference.

Sanitize private context before producing public output. Do not expose secrets, credentials, private tokens, or irrelevant personal information from previous sessions.

## Efficiency rules

- Search narrowly before reading deeply.
- Prefer native session search over raw session-file mining.
- Read only relevant session regions.
- Use fresh subagents for independent history slices when there are many candidates and delegation is available.
- Keep bulky transcripts out of the main context.
- Do not reread the entire repository when a small set of files and Git state can answer the question.
- Stop once the current state and next move are well supported.

## Failure handling

If session history is unavailable, say so and reconstruct from live repository state and available project records.

If GitHub access is unavailable, report that limitation and do not present stale PR or issue information as current.

If a source connector or MCP is unavailable, skip it and state the omission.

If the evidence is insufficient to identify where the work stopped, say what is known, what is unknown, and what single check would resolve the uncertainty.

## Reply style

Write the brief using the project's available concise technical-writing or unslop skill when present.

Use short declarative sentences.

Make actors and actions explicit.

Separate observed facts from inference.

Do not add a generic introduction or conclusion.

The final answer must answer three questions quickly:

1. What did I work on?
2. Where does it stand now?
3. What should I do next?

**Reply:** the brief, following the contract above.
