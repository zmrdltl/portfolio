from __future__ import annotations

from pathlib import Path
import tempfile
import textwrap
import unittest

from scripts.check_structure import validate_structure


VALID_CONFIG = """\
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
nav:
  - 소개: index.md
plugins:
  - i18n:
      docs_structure: suffix
      languages:
        - locale: ko
          name: 한국어
          build: true
          default: true
        - locale: en
          name: English
          build: true
          nav_translations:
            소개: Overview
"""


class StructureCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.docs_dir = self.root / "docs"
        self.docs_dir.mkdir()
        self.config_path = self.root / "mkdocs.yml"
        self.config_path.write_text(VALID_CONFIG, encoding="utf-8")
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n## 요약\n", encoding="utf-8"
        )
        (self.docs_dir / "index.en.md").write_text(
            "# Overview\n\n## Summary\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def validate(self) -> list[str]:
        errors, _ = validate_structure(self.docs_dir, self.config_path)
        return errors

    def test_valid_structure(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_macos_metadata_file_is_rejected(self) -> None:
        (self.docs_dir / ".DS_Store").write_bytes(b"local metadata")

        self.assertIn(
            "Forbidden static file in docs: .DS_Store.",
            self.validate(),
        )

    def test_missing_translation_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").unlink()

        self.assertTrue(
            any(
                "Missing English translation: index.en.md" in error
                for error in self.validate()
            )
        )

    def test_heading_outline_mismatch_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").write_text(
            "# Overview\n\n### Summary\n", encoding="utf-8"
        )

        self.assertTrue(
            any(
                "Heading outline mismatch" in error
                for error in self.validate()
            )
        )

    def test_shorter_nested_fence_does_not_expose_code_headings(self) -> None:
        (self.docs_dir / "index.md").write_text(
            textwrap.dedent(
                """\
                # 소개

                ````text
                ```markdown
                ## 코드 속 제목
                ```
                ````

                ## 요약
                """
            ),
            encoding="utf-8",
        )
        (self.docs_dir / "index.en.md").write_text(
            textwrap.dedent(
                """\
                # Overview

                ````text
                ```markdown
                ### Different code heading
                ```
                ````

                ## Summary
                """
            ),
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_page_missing_from_nav_is_rejected(self) -> None:
        (self.docs_dir / "extra.md").write_text(
            "# 추가\n", encoding="utf-8"
        )
        (self.docs_dir / "extra.en.md").write_text(
            "# Extra\n", encoding="utf-8"
        )

        self.assertIn("Page missing from nav: extra.md.", self.validate())

    def test_explicit_appendix_can_remain_off_nav(self) -> None:
        (self.docs_dir / "appendix.md").write_text(
            "---\nportfolio_role: appendix\n---\n\n# 부록\n",
            encoding="utf-8",
        )
        (self.docs_dir / "appendix.en.md").write_text(
            "---\nportfolio_role: appendix\n---\n\n# Appendix\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_valid_legacy_redirect_can_remain_off_nav(self) -> None:
        redirect = (
            "---\n"
            "portfolio_role: legacy_redirect\n"
            "redirect_to: ../\n"
            "search:\n"
            "  exclude: true\n"
            "---\n\n"
            '<meta http-equiv="refresh" content="0; url=../">\n\n'
            "# Home\n\n[Continue](../)\n"
        )
        (self.docs_dir / "legacy.md").write_text(redirect, encoding="utf-8")
        (self.docs_dir / "legacy.en.md").write_text(redirect, encoding="utf-8")

        self.assertEqual(self.validate(), [])

    def test_legacy_redirect_requires_search_exclusion(self) -> None:
        redirect = (
            "---\nportfolio_role: legacy_redirect\nredirect_to: ../\n---\n\n"
            '<meta http-equiv="refresh" content="0; url=../">\n\n'
            "# Home\n\n[Continue](../)\n"
        )
        (self.docs_dir / "legacy.md").write_text(redirect, encoding="utf-8")
        (self.docs_dir / "legacy.en.md").write_text(redirect, encoding="utf-8")

        self.assertIn(
            "Legacy redirect must be excluded from search: legacy.md.",
            self.validate(),
        )

    def test_duplicated_english_nav_is_rejected(self) -> None:
        self.config_path.write_text(
            textwrap.dedent(
                """\
                nav:
                  - 소개: index.md
                plugins:
                  - i18n:
                      docs_structure: suffix
                      languages:
                        - locale: ko
                          build: true
                          default: true
                        - locale: en
                          build: true
                          nav:
                            - Overview: index.md
                          nav_translations:
                            소개: Overview
                """
            ),
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "must use nav_translations" in error
                for error in self.validate()
            )
        )

    def test_disabled_english_build_is_rejected(self) -> None:
        self.config_path.write_text(
            VALID_CONFIG.replace(
                "        - locale: en\n          name: English\n          build: true",
                "        - locale: en\n          name: English\n          build: false",
            ),
            encoding="utf-8",
        )

        self.assertIn(
            "English locale build must remain enabled.", self.validate()
        )

    def test_empty_nav_translation_is_rejected(self) -> None:
        self.config_path.write_text(
            VALID_CONFIG.replace("소개: Overview", "소개: ''"),
            encoding="utf-8",
        )

        self.assertIn(
            "English nav translation must be a non-empty string: 소개.",
            self.validate(),
        )


if __name__ == "__main__":
    unittest.main()
