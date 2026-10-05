from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import port_upstream
from port_upstream import adapt_frontmatter, adapt_runtime


class PortUpstreamTests(unittest.TestCase):
    def test_adapt_frontmatter_preserves_vscode_skill_extensions(self):
        source = (
            "---\n"
            "name: old-name\n"
            "description: Recall prior work.\n"
            "disable-model-invocation: true\n"
            "user-invocable: true\n"
            'argument-hint: "[topic]"\n'
            "paths: '**/*.md'\n"
            "unsupported-field: true\n"
            "---\n"
            "Instructions.\n"
        )

        adapted = adapt_frontmatter(source, "recall")

        self.assertIn("name: recall\n", adapted)
        self.assertIn("disable-model-invocation: true\n", adapted)
        self.assertIn("user-invocable: true\n", adapted)
        self.assertIn('argument-hint: "[topic]"\n', adapted)
        self.assertNotIn("paths:", adapted)
        self.assertNotIn("unsupported-field:", adapted)

    def test_adapt_runtime_does_not_rewrite_cursor_domain_names(self):
        source = "Cursor uses `Cursor's /loop`; https://api2.cursor.sh/hook"

        adapted = adapt_runtime(source)

        self.assertIn("https://api2.cursor.sh/hook", adapted)
        self.assertIn("Copilot", adapted)

    def test_port_preserves_curated_host_fallback(self):
        with TemporaryDirectory() as temp:
            root = Path(temp) / "target"
            source = Path(temp) / "source"
            fallback = "---\nname: make-bot-ui\ndescription: Existing endpoint only.\n---\nNo invented API.\n"
            (root / "skills" / "make-bot-ui").mkdir(parents=True)
            (root / "skills" / "make-bot-ui" / "SKILL.md").write_text(fallback, encoding="utf-8")

            for skill in ("make-bot-ui", "recall"):
                (source / "skills" / skill).mkdir(parents=True)
            (source / "skills" / "make-bot-ui" / "SKILL.md").write_text(
                "---\nname: Make Bot UI\ndescription: Cursor routine.\n---\nupdate_state\n",
                encoding="utf-8",
            )
            (source / "skills" / "recall" / "SKILL.md").write_text(
                "---\nname: Recall\ndescription: Recall context.\n---\nCursor guide.\n",
                encoding="utf-8",
            )
            (source / "LICENSE").write_text("license", encoding="utf-8")

            with patch.object(port_upstream, "ROOT", root):
                port_upstream.port(source, replace_existing=True)

            self.assertEqual(
                (root / "skills" / "make-bot-ui" / "SKILL.md").read_text(encoding="utf-8"),
                fallback,
            )
            self.assertIn("name: recall", (root / "skills" / "recall" / "SKILL.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
