from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PATH_PARTS = {".git", "node_modules", "third_party", "third-party", "vendor"}
SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
    "paths",
}
RUNTIME_REPLACEMENTS = (
    (r"~[/\\]\.cursor/rules/pstack-models\.mdc", "Copilot model preferences"),
    (r"(?:~[/\\]\.cursor/rules/|\.cursor/rules/)?pstack-models\.mdc", "Copilot model preferences"),
    (r"~[/\\.]cursor/skills/", "~/.copilot/skills/"),
    (r"\.cursor/skills/", ".github/skills/"),
    (r"\.cursor/worktrees/", "worktrees/"),
    (r"~[/\\.]cursor/(?:projects|plugins|worktrees)", "the active Copilot client's configuration"),
    (r"Cursor's `/loop` command", "the active Copilot client's session or automation controls"),
    (r"Cursor's `/loop`", "the active Copilot client's session or automation controls"),
    (r"Cursor's `/automate`", "the active Copilot client's automation configuration"),
    (r"Cursor's built-in babysit skill", "the host's built-in babysit workflow"),
    (r"Cursor's built-in for authoring SKILL.md files", "Copilot's skill authoring workflow"),
    (r"Cursor's built-in `create-skill` skill", "Copilot's skill authoring workflow"),
    (r"Cursor cloud agent", "Copilot agent"),
    (r"Cursor Cloud Agent", "Copilot agent"),
    (r"Cursor dashboard", "Copilot session status"),
    (r"Cursor restart", "Copilot client restart"),
    (r"Cursor", "Copilot"),
    (r"cursor-team-kit", "separately configured Copilot tools or MCP servers"),
    (r"control-ui", "the host's available browser tools"),
    (r"control-cli", "the host's available terminal tools"),
    (r"deslop", "unslop"),
    (r"create-skill", "Copilot skill authoring workflow"),
    (r"AskQuestion", "ask the user"),
    (r"subagent_type", "agent role"),
    (r"generalPurpose", "general-purpose"),
    (r"Task tool", "agent delegation tool exposed by the active Copilot client"),
    (r"the Task tool", "agent delegation tool exposed by the active Copilot client"),
    (r"Task calls", "subagent calls"),
    (r"Task call", "subagent call"),
    (r"\bTask\b", "subagent"),
    (r"`subagent_type: \"poteto-agent\"`", "the `poteto-agent` profile"),
    (r"`/deslop`", "the bundled `unslop` skill"),
    (r"`control-ui`", "the host's available browser tools"),
    (r"`control-cli`", "the host's available terminal tools"),
)


def adapt_frontmatter(text: str, directory_name: str) -> str:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    _, frontmatter, body = text.split("---", 2)
    kept: list[str] = []
    in_metadata = False
    for line in frontmatter.splitlines():
        match = re.match(r"^([a-zA-Z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            if in_metadata:
                kept.append(line)
            continue
        key = match.group(1)
        in_metadata = key == "metadata"
        if key not in SKILL_FIELDS:
            continue
        if key == "name":
            kept.append(f"name: {directory_name}")
        elif key not in {"paths", "disable-model-invocation", "user-invocable"}:
            kept.append(line)
    if directory_name == "typescript-best-practices":
        kept.append('metadata:\n  "copilot/instructions": "**/*.ts, **/*.tsx"')
    keys = {line.split(":", 1)[0] for line in kept}
    if "name" not in keys:
        kept.insert(0, f"name: {directory_name}")
    if "description" not in keys:
        raise ValueError(f"missing description for {directory_name}")
    return "---\n" + "\n".join(kept).strip() + "\n---" + body


def adapt_runtime(text: str) -> str:
    for pattern, replacement in RUNTIME_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE if pattern.lower().startswith("cursor") else 0)
    text = text.replace(
        "Write `Copilot model preferences`, an always-applied rule that sets pstack's model per role.",
        "Choose model preferences per role using options supported by the active Copilot client. This skill recommends mappings but cannot enforce per-role model routing.",
    )
    text = text.replace("`Copilot model preferences` rule", "available Copilot model preferences")
    text = text.replace("in `Copilot model preferences`", "in the available model-preference list")
    text = text.replace("the rule or that line is missing", "the preference or that line is missing")
    if text.startswith("---\nname: setup-pstack\n"):
        text = text.replace(
            "description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults.",
            "description: Recommend model preferences for P-Stack roles and a reasoning budget based on models available in the active Copilot client. Does not enforce per-role routing.",
        )
        text = text.replace(
            "The default role-to-model mapping is the rule shape shown in step 5 below. If `Copilot model preferences` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults.",
            "The default role-to-model mapping is the preference shape shown in step 5 below. If you maintain a model-preference list, read it and treat its `# budget` line and role values as the current choices. Otherwise start from those defaults.",
        )
        text = re.sub(
            r"### 5\. Write the rule\n.*?\n### 6\. Confirm",
            "### 5. Present the preferences\n\nShow the selected mapping as a recommendation, with a `# budget` line and one line per role. Use only models exposed by the active Copilot client. Do not claim that writing a rule or file will enforce per-role routing.\n\n### 6. Confirm",
            text,
            flags=re.DOTALL,
        )
        text = text.replace(
            "Tell the user the rule was written and that it applies to new sessions. Re-running this skill updates it.",
            "Tell the user which preferences were selected and that the active Copilot client may not apply them automatically.",
        )
    return text


def replace_file(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def is_packaged_file(path: Path) -> bool:
    return not (IGNORED_PATH_PARTS & set(path.relative_to(ROOT).parts))


def port(source: Path, replace_existing: bool = False) -> None:
    skills_source = source / "skills"
    if not skills_source.is_dir():
        raise ValueError(f"source has no skills directory: {skills_source}")
    if not (source / "LICENSE").is_file():
        raise ValueError(f"source has no LICENSE: {source}")
    if not replace_existing and any((ROOT / path).exists() for path in ("skills", "plugin.json", "LICENSE")):
        raise ValueError("port target already contains generated plugin files")
    if replace_existing:
        shutil.rmtree(ROOT / "skills", ignore_errors=True)
        for path in (ROOT / "LICENSE", ROOT / "assets" / "logo.png"):
            path.unlink(missing_ok=True)

    shutil.copytree(skills_source, ROOT / "skills")
    shutil.copy2(source / "LICENSE", ROOT / "LICENSE")
    logo = source / "assets" / "logo.png"
    if logo.is_file():
        (ROOT / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copy2(logo, ROOT / "assets" / "logo.png")

    count = 0
    for path in sorted((ROOT / "skills").rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".mdc", ".sh", ".ts", ".tsx", ".js", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            text = adapt_frontmatter(text, path.relative_to(ROOT / "skills").parts[0])
            count += 1
        replace_file(path, adapt_runtime(text))
    print(f"Ported {count} upstream skills from {source}")


def validate() -> int:
    errors: list[str] = []
    manifest_path = ROOT / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("plugin.json does not declare Agent Plugins 1.0")
        if manifest.get("name") != "pstack":
            errors.append("plugin.json name must be pstack")
        allowed_manifest_fields = {
            "$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"
        }
        unknown_fields = set(manifest) - allowed_manifest_fields
        if unknown_fields:
            errors.append(f"plugin.json has unsupported Agent Plugins 1.0 fields {sorted(unknown_fields)}")
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"plugin.json is invalid: {error}")

    marketplace_path = ROOT / ".github" / "plugin" / "marketplace.json"
    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        if not isinstance(marketplace.get("owner", {}).get("name"), str) or not marketplace["owner"]["name"].strip():
            errors.append("marketplace.json must identify its owner")
        plugins = marketplace.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1:
            errors.append("marketplace.json must list exactly the P-Stack plugin")
        else:
            entry = plugins[0]
            if entry.get("name") != "pstack" or entry.get("source") != ".":
                errors.append("marketplace.json must point to the root P-Stack plugin")
            if entry.get("version") != manifest.get("version"):
                errors.append("marketplace plugin version does not match plugin.json")
    except (OSError, json.JSONDecodeError, TypeError, AttributeError) as error:
        errors.append(f"marketplace.json is invalid: {error}")

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(skill_files) != 47:
        errors.append(f"expected 47 upstream skill entries, found {len(skill_files)}")
    for path in skill_files:
        try:
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                errors.append(f"{path.relative_to(ROOT)} has no frontmatter")
                continue
            _, frontmatter, body = text.split("---", 2)
            fields = {
                match.group(1)
                for line in frontmatter.splitlines()
                if (match := re.match(r"^([a-zA-Z0-9_-]+):", line))
            }
            unsupported = fields - SKILL_FIELDS
            if unsupported:
                errors.append(f"{path.relative_to(ROOT)} has unsupported fields {sorted(unsupported)}")
            if f"name: {path.parent.name}" not in frontmatter:
                errors.append(f"{path.relative_to(ROOT)} name does not match its directory")
            if not re.search(r"(?m)^description:\s*\S", frontmatter):
                errors.append(f"{path.relative_to(ROOT)} has no description")
            for target in re.findall(r"\]\(([^)]+)\)", body):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                relative_target = target.split("#", 1)[0]
                if relative_target == "url":
                    continue
                resolved = (path.parent / relative_target).resolve()
                if relative_target and not resolved.exists():
                    errors.append(f"{path.relative_to(ROOT)} links to missing path {target}")
        except (OSError, ValueError) as error:
            errors.append(f"{path.relative_to(ROOT)} could not be checked: {error}")

    agents = sorted((ROOT / "com.github.copilot" / "agents").glob("*.agent.md"))
    if len(agents) < 2:
        errors.append("Copilot agent profiles are missing")
    for path in agents:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n") or not re.search(r"(?m)^description:\s*\S", text):
            errors.append(f"{path.relative_to(ROOT)} has invalid agent metadata")

    command_path = ROOT / "com.github.copilot" / "commands" / "poteto-mode.md"
    if not command_path.is_file():
        errors.append("Copilot /poteto-mode command is missing")
    else:
        command_text = command_path.read_text(encoding="utf-8")
        if "`poteto-agent` profile" not in command_text:
            errors.append("Copilot /poteto-mode command does not route through poteto-agent")
        if "do not start a sibling or substitute `general-purpose`" not in command_text:
            errors.append("Copilot /poteto-mode command does not preserve the upstream routing contract")
    if not (ROOT / "LICENSE").is_file():
        errors.append("upstream LICENSE is missing")
    if not (ROOT / "assets" / "logo.png").is_file():
        errors.append("upstream logo is missing")
    if not (ROOT / "ADAPTATION.md").is_file():
        errors.append("ADAPTATION.md is missing")

    host_only = re.compile(r"(?i)cursor-team-kit|subagent_type\s*:|AskQuestion|~[/\\.]cursor|\.cursor/(?:skills|rules)|pstack-models\.mdc|~/Copilot model selection")
    text_files = [
        path for path in (ROOT / "skills").rglob("*")
        if path.is_file() and is_packaged_file(path) and path.suffix.lower() in {".md", ".mdc", ".sh", ".tsx", ".ts", ".js", ".json"}
    ] + agents + [ROOT / "README.md"]
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        if host_only.search(text):
            errors.append(f"{path.relative_to(ROOT)} contains an unadapted Cursor runtime reference")
        if path.suffix.lower() not in {".md", ".mdc"}:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative_target = target.split("#", 1)[0]
            if relative_target == "url":
                continue
            if relative_target and not (path.parent / relative_target).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)} links to missing path {target}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {len(skill_files)} skills, {len(agents)} agents, and the /poteto-mode command")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()
    if args.validate:
        return validate()
    if args.source is None:
        parser.error("provide --source <upstream-pstack-directory> or --validate")
    port(args.source.resolve(), replace_existing=args.replace_existing)
    return 0


if __name__ == "__main__":
    sys.exit(main())
