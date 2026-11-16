"""Portable checks for source-distribution scope, links and module dependencies."""

import ast
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PublicSourceTests(unittest.TestCase):
    def test_public_scope_and_sensitive_text(self):
        for folder in ["reports", "configs/resubmission", "docs/archive"]:
            self.assertFalse(any(p.is_file() for p in (ROOT / folder).rglob("*")))
        forbidden = [
            "PR9" + "_REVIEW", "Owner" + " authorization", "owner" + " confirmed",
            "/scratch/" + "home/", "10.21." + "232.33",
            "\u672a\u770b\u8fc7", "\u5ba1\u7a3f", "\u62d2\u7a3f",
        ]
        for p in ROOT.rglob("*"):
            if not p.is_file() or any(x in p.parts for x in [".git", "__pycache__"]):
                continue
            if p.suffix in [".pyc", ".so"]:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            for value in forbidden:
                self.assertNotIn(value.lower(), text.lower(), str(p.relative_to(ROOT)))

    def test_local_imports_and_document_links(self):
        for p in ROOT.rglob("*.py"):
            if "__pycache__" in p.parts:
                continue
            tree = ast.parse(p.read_text(encoding="utf-8-sig"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("lib."):
                    target = ROOT / node.module.replace(".", "/")
                    self.assertTrue(target.with_suffix(".py").exists() or (target / "__init__.py").exists(), (str(p), node.module))
        for p in [ROOT / "README.md", ROOT / "README_zh.md", *list((ROOT / "docs").glob("*.md"))]:
            for link in re.findall(r"\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
                if "://" in link or link.startswith("#"):
                    continue
                self.assertTrue((p.parent / link.split("#")[0]).exists(), (str(p), link))

    def test_weight_urls_and_metadata(self):
        weights = json.loads((ROOT / "checkpoints/manifest.json").read_text())
        self.assertEqual(len(weights), 6)
        prefix = "https://github.com/Fubuyunhua/GCS-Pose/releases/download/"
        for row in weights:
            self.assertTrue(row["url"].startswith(prefix))
            self.assertRegex(row["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(row["bytes"], 0)


if __name__ == "__main__":
    unittest.main()
