from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from scripts.check_built_site import (
    SITEMAP_NAMESPACE,
    XHTML_NAMESPACE,
    validate_built_site,
)


SITEMAP_PAIRS = (
    ("/portfolio/", "/portfolio/en/"),
    (
        "/portfolio/engineering-principles/",
        "/portfolio/en/engineering-principles/",
    ),
    ("/portfolio/experience/cluml/", "/portfolio/en/experience/cluml/"),
    (
        "/portfolio/experience/tmaxcloud/",
        "/portfolio/en/experience/tmaxcloud/",
    ),
    ("/portfolio/opensource/gluesql/", "/portfolio/en/opensource/gluesql/"),
    ("/portfolio/projects/coupler/", "/portfolio/en/projects/coupler/"),
)


class BuiltSiteCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.site_dir = Path(self.temp_dir.name) / "site"
        self.contract_path = Path(self.temp_dir.name) / "portfolio.contract.yml"
        self.config_path = Path(self.temp_dir.name) / "mkdocs.yml"
        self.write_fixture()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_sitemap(self) -> None:
        ET.register_namespace("", SITEMAP_NAMESPACE)
        ET.register_namespace("xhtml", XHTML_NAMESPACE)
        root = ET.Element(f"{{{SITEMAP_NAMESPACE}}}urlset")
        for korean_path, english_path in SITEMAP_PAIRS:
            for loc_path in (korean_path, english_path):
                url = ET.SubElement(root, f"{{{SITEMAP_NAMESPACE}}}url")
                loc = ET.SubElement(url, f"{{{SITEMAP_NAMESPACE}}}loc")
                loc.text = f"https://example.com{loc_path}"
                for locale, href_path in (
                    ("ko", korean_path),
                    ("en", english_path),
                ):
                    ET.SubElement(
                        url,
                        f"{{{XHTML_NAMESPACE}}}link",
                        {
                            "rel": "alternate",
                            "hreflang": locale,
                            "href": f"https://example.com{href_path}",
                        },
                    )
        sitemap = self.site_dir / "sitemap.xml"
        sitemap.parent.mkdir(parents=True, exist_ok=True)
        ET.ElementTree(root).write(sitemap, encoding="utf-8", xml_declaration=True)

    def write_not_found_page(self) -> None:
        (self.site_dir / "404.html").write_text(
            """\
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="robots" content="noindex,follow">
    <title>페이지를 찾을 수 없습니다 · Page not found</title>
  </head>
  <body>
    <h1>페이지를 찾을 수 없습니다 · <span lang="en">Page not found</span></h1>
    <p>요청한 페이지가 없거나 이동했습니다.</p>
    <p lang="en">The page does not exist or has moved.</p>
    <a href="/portfolio/" lang="ko">한국어 홈</a>
    <a href="/portfolio/en/" lang="en">English home</a>
  </body>
</html>
""",
            encoding="utf-8",
        )

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
        self.config_path.write_text(
            "site_url: https://example.com/portfolio/\n",
            encoding="utf-8",
        )
        self.write_sitemap()
        self.write_not_found_page()

    def validate(self) -> list[str]:
        findings, _ = validate_built_site(
            self.site_dir,
            self.contract_path,
            self.config_path,
        )
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

    def test_legacy_redirect_in_sitemap_fails(self) -> None:
        path = self.site_dir / "sitemap.xml"
        tree = ET.parse(path)
        url = ET.SubElement(tree.getroot(), f"{{{SITEMAP_NAMESPACE}}}url")
        loc = ET.SubElement(url, f"{{{SITEMAP_NAMESPACE}}}loc")
        loc.text = "https://example.com/portfolio/experience/"
        tree.write(path, encoding="utf-8", xml_declaration=True)

        self.assertTrue(
            any("Legacy redirect leaked into sitemap" in item for item in self.validate())
        )

    def test_missing_public_sitemap_url_fails(self) -> None:
        path = self.site_dir / "sitemap.xml"
        tree = ET.parse(path)
        root = tree.getroot()
        for url in root.findall(f"{{{SITEMAP_NAMESPACE}}}url"):
            loc = url.find(f"{{{SITEMAP_NAMESPACE}}}loc")
            if loc is not None and loc.text and loc.text.endswith(
                "/portfolio/engineering-principles/"
            ):
                root.remove(url)
                break
        tree.write(path, encoding="utf-8", xml_declaration=True)

        self.assertTrue(
            any("must appear exactly once" in item for item in self.validate())
        )

    def test_incorrect_sitemap_alternates_fail(self) -> None:
        path = self.site_dir / "sitemap.xml"
        tree = ET.parse(path)
        for url in tree.getroot().findall(f"{{{SITEMAP_NAMESPACE}}}url"):
            loc = url.find(f"{{{SITEMAP_NAMESPACE}}}loc")
            if loc is None or not loc.text or not loc.text.endswith(
                "/portfolio/en/projects/coupler/"
            ):
                continue
            for link in url.findall(f"{{{XHTML_NAMESPACE}}}link"):
                if link.get("hreflang") == "ko":
                    link.set(
                        "href",
                        "https://example.com/portfolio/experience/cluml/",
                    )
        tree.write(path, encoding="utf-8", xml_declaration=True)

        self.assertTrue(
            any("incorrect ko/en alternates" in item for item in self.validate())
        )

    def test_invalid_not_found_metadata_fails(self) -> None:
        (self.site_dir / "404.html").write_text(
            """\
<html lang="en"><head>
<meta charset="iso-8859-1">
<meta name="viewport" content="width=980">
<meta name="robots" content="index,follow">
</head><body><p>Page not found.</p></body></html>
""",
            encoding="utf-8",
        )

        findings = self.validate()
        for expected in (
            "lang=ko",
            "UTF-8",
            "viewport",
            "noindex,follow",
            "lang=en",
            "h1",
        ):
            self.assertTrue(any(expected in item for item in findings))

    def test_not_found_link_contract_fails(self) -> None:
        path = self.site_dir / "404.html"
        text = path.read_text(encoding="utf-8").replace(
            'href="/portfolio/en/"',
            'href="/portfolio/projects/coupler/"',
        )
        path.write_text(text, encoding="utf-8")

        findings = self.validate()
        self.assertTrue(any("links must be exactly" in item for item in findings))
        self.assertTrue(any("Coupler link" in item for item in findings))

    def test_wrong_origin_sitemap_url_fails(self) -> None:
        path = self.site_dir / "sitemap.xml"
        tree = ET.parse(path)
        for url in tree.getroot().findall(f"{{{SITEMAP_NAMESPACE}}}url"):
            loc = url.find(f"{{{SITEMAP_NAMESPACE}}}loc")
            if loc is not None and loc.text == (
                "https://example.com/portfolio/en/projects/coupler/"
            ):
                loc.text = "https://wrong.example/portfolio/en/projects/coupler/"
                break
        tree.write(path, encoding="utf-8", xml_declaration=True)

        findings = self.validate()
        self.assertTrue(any("unexpected URLs" in item for item in findings))
        self.assertTrue(any("must appear exactly once" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
