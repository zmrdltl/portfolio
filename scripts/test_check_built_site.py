from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from scripts.check_built_site import validate_built_site


class BuiltSiteCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.site_dir = Path(self.temp_dir.name) / "site"
        self.contract_path = Path(self.temp_dir.name) / "portfolio.contract.yml"
        self.write_fixture()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_fixture(self) -> None:
        locations = [
            "experience/cluml/",
            "experience/tmaxcloud/",
            "opensource/gluesql/",
            "projects/coupler/",
        ]
        for locale_prefix in ("", "en/"):
            redirect = self.site_dir / locale_prefix / "experience" / "index.html"
            redirect.parent.mkdir(parents=True, exist_ok=True)
            redirect.write_text(
                '<html><head><meta http-equiv="refresh" content="0; url=../">'
                "</head></html>",
                encoding="utf-8",
            )
        search = self.site_dir / "search" / "search_index.json"
        search.parent.mkdir(parents=True, exist_ok=True)
        search.write_text(
            json.dumps(
                {
                    "docs": [
                        {"location": locale_prefix + location, "title": location}
                        for locale_prefix in ("", "en/")
                        for location in locations
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.contract_path.write_text(
            """\
content_coverage:
  - path: docs/experience/cluml.md
    search_terms: [experience/cluml]
  - path: docs/experience/cluml.en.md
    search_terms: [experience/cluml]
""",
            encoding="utf-8",
        )

    def validate(self) -> list[str]:
        findings, _ = validate_built_site(self.site_dir, self.contract_path)
        return findings

    def test_expected_built_site_passes(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_legacy_redirect_in_search_fails(self) -> None:
        path = self.site_dir / "search" / "search_index.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["docs"].append({"location": "experience/", "title": "경력"})
        path.write_text(json.dumps(payload), encoding="utf-8")

        self.assertTrue(any("leaked" in item for item in self.validate()))

    def test_cross_language_redirect_fails(self) -> None:
        path = self.site_dir / "en" / "experience" / "index.html"
        path.write_text(
            '<meta http-equiv="refresh" content="0; url=../../">', encoding="utf-8"
        )

        self.assertTrue(any("one-hop relative" in item for item in self.validate()))

    def test_missing_required_search_term_fails(self) -> None:
        self.contract_path.write_text(
            """\
content_coverage:
  - path: docs/experience/cluml.md
    search_terms: [missing-keyword]
""",
            encoding="utf-8",
        )

        self.assertTrue(any("lost required terms" in item for item in self.validate()))


if __name__ == "__main__":
    unittest.main()
