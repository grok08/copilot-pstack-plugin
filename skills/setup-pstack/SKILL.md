---
name: setup-pstack
description: Recommend model preferences for P-Stack roles and a reasoning budget based on models available in the active Copilot client. Does not enforce per-role routing. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Choose model preferences per role using options supported by the active Copilot client. This skill recommends mappings but cannot enforce per-role model routing.

## Steps

### 1. Detect available models

Read the model list exposed by the active Copilot client, such as its model picker or a documented CLI model-list command. Use that list to validate model slugs. A delegation control's accepted model argument is not a complete inventory. If no model list is available, use only `inherit-parent` or `auto` until the user provides confirmed model slugs. Never invent or infer a real slug. These aliases remain valid even when no models are listed.

### 2. Load current state

The default role-to-model mapping is the preference shape shown in step 5 below. If you maintain a model-preference list, read it and treat its `# budget` line and role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer ask the user over free text. Offer these four options with these exact labels, and name the current budget when the rule records one.

- `unlimited — keep max`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by family, list, or alias (`inherit-parent`, `auto`). `unlimited` leaves every effort as in that table. `large`, `medium`, and `small` set the effort token of every real slug, panel entries included, to `xhigh`, `high`, or `medium`. The effort token is the last token, or the one before a trailing `fast`, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. If the result is not a detected slug, use the same family's detected slug with the highest effort at or below the target, else mark the role as needing a choice. `inherit-parent` and `auto` do not change. So `small` turns `claude-opus-5-5-max` into `claude-opus-5-5-medium`, and `grok-4.7-xhigh-fast` into `grok-4.7-medium-fast`.

**(c) Show the roles and confirm.** Show every role with its model, marking any real slug not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` (both mean: this role runs on the parent chat model, which is how Auto users stay on Auto) as the options. Prefer ask the user over free text. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real slug written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen real slug is not available, stop and ask again.

### 5. Present the preferences

Show the selected mapping as a recommendation, with a `# budget` line and one line per role. Use only models exposed by the active Copilot client. Do not claim that writing a rule or file will enforce per-role routing.

### 6. Confirm

Tell the user which preferences were selected and that the active Copilot client may not apply them automatically.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill` (resolves wherever pstack is installed: workspace, user, or plugin). On no, move on without pushing.
