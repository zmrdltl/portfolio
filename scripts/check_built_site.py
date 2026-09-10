#!/usr/bin/env python3

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

try:
    import yaml
except ModuleNotFoundError as error:
    raise SystemExit(
        "PyYAML is required. Install the project dependencies with "
        "`pip install -r requirements.txt`."
    ) from error


META_REFRESH_PATTERN = re.compile(
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']0;\s*url=\.\./["\']\s*/?>',
    re.IGNORECASE,
)

SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
PUBLIC_SITEMAP_RELATIVE_PAIRS = (
    ("", "en/"),
    ("engineering-principles/", "en/engineering-principles/"),
    ("experience/cluml/", "en/experience/cluml/"),
    ("experience/tmaxcloud/", "en/experience/tmaxcloud/"),
    ("opensource/gluesql/", "en/opensource/gluesql/"),
    ("projects/coupler/", "en/projects/coupler/"),
)
LEGACY_SITEMAP_RELATIVE_URLS = {
    "experience/",
    "en/experience/",
}
NOT_FOUND_LINKS = (
    ("/portfolio/", "ko"),
    ("/portfolio/en/", "en"),
)
NOT_FOUND_VIEWPORT = "width=device-width,initial-scale=1"


@dataclass(frozen=True)
class BuiltSiteSummary:
    search_documents: int
    redirects: int
    sitemap_urls: int
    not_found_links: int


class NotFoundHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_languages: list[str] = []
        self.charsets: list[str] = []
        self.viewports: list[str] = []
        self.robots: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.english_non_link_elements = 0
        self.english_heading_spans = 0
        self.heading_depth = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {
            name.casefold(): (value or "") for name, value in attrs
        }
        normalized_tag = tag.casefold()
        if normalized_tag == "h1":
            self.heading_depth += 1
        if normalized_tag == "html":
            self.html_languages.append(attributes.get("lang", ""))
        if normalized_tag == "meta":
            if "charset" in attributes:
                self.charsets.append(attributes["charset"])
            name = attributes.get("name", "").casefold()
            if name == "viewport":
                self.viewports.append(attributes.get("content", ""))
            elif name == "robots":
                self.robots.append(attributes.get("content", ""))
        if normalized_tag == "a":
            self.links.append(
                (attributes.get("href", ""), attributes.get("lang", ""))
            )
        elif (
            normalized_tag == "p"
            and attributes.get("lang", "").casefold() == "en"
        ):
            self.english_non_link_elements += 1
        elif (
            normalized_tag == "span"
            and attributes.get("lang", "").casefold() == "en"
            and self.heading_depth > 0
        ):
            self.english_heading_spans += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "h1" and self.heading_depth > 0:
            self.heading_depth -= 1

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)


def normalize_location(location: str) -> str:
    normalized = location.split("#", 1)[0].lstrip("/")
    if normalized.endswith("index.html"):
        normalized = normalized[: -len("index.html")]
    elif normalized.endswith(".html"):
        normalized = normalized[: -len(".html")] + "/"
    return normalized.rstrip("/") + ("/" if normalized else "")


def read_search_documents(path: Path) -> list[dict[str, Any]] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("docs"), list):
        return None
    return [item for item in payload["docs"] if isinstance(item, dict)]


def search_location_for_source(path_value: str) -> str | None:
    if not path_value.startswith("docs/") or not path_value.endswith(".md"):
        return None
    relative = path_value[len("docs/") :]
    if relative.endswith(".en.md"):
        relative = relative[: -len(".en.md")] + ".md"
        locale_prefix = "en/"
    else:
        locale_prefix = ""
    without_suffix = relative[: -len(".md")]
    if without_suffix == "index":
        return locale_prefix
    if without_suffix.endswith("/index"):
        without_suffix = without_suffix[: -len("index")]
    else:
        without_suffix += "/"
    return locale_prefix + without_suffix


def validate_search_term_contract(
    documents: list[dict[str, Any]], contract_path: Path
) -> list[str]:
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, yaml.YAMLError):
        return [f"Unable to read search-term contract: {contract_path}."]
    entries = contract.get("content_coverage") if isinstance(contract, dict) else None
    if not isinstance(entries, list):
        return [f"Search-term contract has no content_coverage list: {contract_path}."]

    errors: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict) or "search_terms" not in entry:
            continue
        path_value = entry.get("path")
        terms = entry.get("search_terms")
        if not isinstance(path_value, str) or not isinstance(terms, list) or not all(
            isinstance(term, str) for term in terms
        ):
            errors.append(f"Invalid search_terms contract entry: {entry!r}.")
            continue
        location = search_location_for_source(path_value)
        if location is None:
            errors.append(f"Cannot map source page to search location: {path_value}.")
            continue
        corpus_parts: list[str] = []
        for document in documents:
            document_location = normalize_location(str(document.get("location", "")))
            if document_location != location:
                continue
            corpus_parts.append(str(document.get("title", "")))
            corpus_parts.append(str(document.get("text", "")))
        corpus = " ".join(corpus_parts).casefold()
        missing = [term for term in terms if term.casefold() not in corpus]
        if missing:
            errors.append(
                f"Generated search index lost required terms for {location}: {missing}."
            )
    return errors


def read_site_url(config_path: Path) -> tuple[str | None, list[str]]:
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, yaml.YAMLError):
        return None, [f"Unable to read MkDocs config: {config_path}."]
    site_url = config.get("site_url") if isinstance(config, dict) else None
    if not isinstance(site_url, str):
        return None, [f"MkDocs config has no string site_url: {config_path}."]
    parsed = urlsplit(site_url)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or parsed.query
        or parsed.fragment
        or not site_url.endswith("/")
    ):
        return None, [
            "MkDocs site_url must be an absolute HTTP(S) URL ending in / "
            "without a query or fragment."
        ]
    return site_url, []


def validate_sitemap(path: Path, site_url: str) -> tuple[list[str], int]:
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError:
        return [f"Missing generated sitemap: {path}."], 0
    except ET.ParseError as error:
        return [f"Unable to parse generated sitemap: {path}: {error}."], 0

    namespaces = {"sitemap": SITEMAP_NAMESPACE, "xhtml": XHTML_NAMESPACE}
    records: list[tuple[str, list[tuple[str, str]]]] = []
    errors: list[str] = []
    for url_element in root.findall("sitemap:url", namespaces):
        loc_elements = url_element.findall("sitemap:loc", namespaces)
        if len(loc_elements) != 1 or not loc_elements[0].text:
            errors.append("Each sitemap URL must contain exactly one non-empty loc.")
            continue
        loc_url = loc_elements[0].text.strip()
        alternates = [
            (
                link.get("hreflang", ""),
                link.get("href", ""),
            )
            for link in url_element.findall("xhtml:link", namespaces)
            if link.get("rel") == "alternate"
        ]
        records.append((loc_url, alternates))

    counts = Counter(loc_url for loc_url, _ in records)
    alternates_by_url = {
        loc_url: alternates
        for loc_url, alternates in records
        if counts[loc_url] == 1
    }

    expected_pairs = tuple(
        (urljoin(site_url, korean), urljoin(site_url, english))
        for korean, english in PUBLIC_SITEMAP_RELATIVE_PAIRS
    )
    expected_urls = {
        loc_url for pair in expected_pairs for loc_url in pair
    }
    unexpected_urls = sorted(set(counts) - expected_urls)
    if unexpected_urls:
        errors.append(f"Sitemap contains unexpected URLs: {unexpected_urls}.")

    for legacy_relative_url in sorted(LEGACY_SITEMAP_RELATIVE_URLS):
        legacy_url = urljoin(site_url, legacy_relative_url)
        if counts[legacy_url]:
            errors.append(f"Legacy redirect leaked into sitemap: {legacy_url}.")

    for korean_url, english_url in expected_pairs:
        expected_alternates = Counter(
            (("ko", korean_url), ("en", english_url))
        )
        for loc_url in (korean_url, english_url):
            if counts[loc_url] != 1:
                errors.append(
                    "Public sitemap URL must appear exactly once: "
                    f"{loc_url} (found {counts[loc_url]})."
                )
                continue
            actual_alternates = Counter(alternates_by_url[loc_url])
            if actual_alternates != expected_alternates:
                errors.append(
                    f"Public sitemap URL has incorrect ko/en alternates: {loc_url}."
                )

    return errors, len(records)


def validate_not_found_page(path: Path) -> tuple[list[str], int]:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return [f"Unable to read UTF-8 404 page: {path}."], 0

    parser = NotFoundHTMLParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as error:
        return [f"Unable to parse 404 page: {path}: {error}."], 0

    errors: list[str] = []
    if [language.casefold() for language in parser.html_languages] != ["ko"]:
        errors.append("404 page must contain exactly one html element with lang=ko.")
    if [charset.casefold() for charset in parser.charsets] != ["utf-8"]:
        errors.append("404 page must declare exactly one UTF-8 charset meta element.")
    if parser.viewports != [NOT_FOUND_VIEWPORT]:
        errors.append(
            "404 page viewport must be exactly "
            f"{NOT_FOUND_VIEWPORT!r}."
        )
    normalized_robots = [
        value.casefold().replace(" ", "") for value in parser.robots
    ]
    if normalized_robots != ["noindex,follow"]:
        errors.append("404 page robots directive must be exactly noindex,follow.")
    if Counter(parser.links) != Counter(NOT_FOUND_LINKS):
        errors.append(
            "404 page links must be exactly the Korean and English portfolio homes "
            "with matching lang attributes."
        )
    if any("coupler" in href.casefold() for href, _ in parser.links):
        errors.append("404 page must not contain a context-dependent Coupler link.")
    if parser.english_non_link_elements < 1:
        errors.append("404 page English explanation must have a lang=en annotation.")
    if parser.english_heading_spans < 1:
        errors.append("404 page h1 must contain an English span with lang=en.")

    return errors, len(parser.links)


def validate_built_site(
    site_dir: Path,
    contract_path: Path | None = None,
    config_path: Path | None = None,
) -> tuple[list[str], BuiltSiteSummary]:
    errors: list[str] = []
    redirect_paths = (
        site_dir / "experience" / "index.html",
        site_dir / "en" / "experience" / "index.html",
    )
    for path in redirect_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            errors.append(f"Missing built legacy redirect: {path}.")
            continue
        if META_REFRESH_PATTERN.search(text) is None:
            errors.append(f"Built legacy redirect is not a one-hop relative redirect: {path}.")

    index_contracts = (
        (
            site_dir / "search" / "search_index.json",
            "experience/",
            {
                "experience/cluml/",
                "experience/tmaxcloud/",
                "opensource/gluesql/",
                "projects/coupler/",
            },
        ),
        (
            site_dir / "search" / "search_index.json",
            "en/experience/",
            {
                "en/experience/cluml/",
                "en/experience/tmaxcloud/",
                "en/opensource/gluesql/",
                "en/projects/coupler/",
            },
        ),
    )

    total_documents = 0
    for index_path, redirect_location, expected_locations in index_contracts:
        documents = read_search_documents(index_path)
        if documents is None:
            errors.append(f"Unable to read generated search index: {index_path}.")
            continue
        if index_path == site_dir / "search" / "search_index.json":
            total_documents = len(documents)
        locations = {
            normalize_location(str(document.get("location", "")))
            for document in documents
        }
        normalized_redirect = normalize_location(redirect_location)
        if normalized_redirect in locations:
            errors.append(
                f"Legacy redirect leaked into generated search index: "
                f"{index_path}:{redirect_location}."
            )
        missing = sorted(expected_locations - locations)
        if missing:
            errors.append(
                f"Generated search index is missing representative detail pages: "
                f"{index_path}:{missing}."
            )

    if contract_path is not None:
        documents = read_search_documents(site_dir / "search" / "search_index.json")
        if documents is not None:
            errors.extend(validate_search_term_contract(documents, contract_path))

    sitemap_urls = 0
    if config_path is None:
        errors.append("MkDocs config is required for exact sitemap URL validation.")
    else:
        site_url, config_errors = read_site_url(config_path)
        errors.extend(config_errors)
        if site_url is not None:
            sitemap_errors, sitemap_urls = validate_sitemap(
                site_dir / "sitemap.xml", site_url
            )
            errors.extend(sitemap_errors)
    not_found_errors, not_found_links = validate_not_found_page(
        site_dir / "404.html"
    )
    errors.extend(not_found_errors)

    return errors, BuiltSiteSummary(
        total_documents,
        len(redirect_paths),
        sitemap_urls,
        not_found_links,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated redirects, search, sitemap, and 404 output."
    )
    parser.add_argument(
        "--site-dir",
        type=Path,
        default=Path("site"),
        help="Built MkDocs site directory (default: site).",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("portfolio.contract.yml"),
        help="Portfolio contract with search_terms (default: portfolio.contract.yml).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("mkdocs.yml"),
        help="MkDocs config with site_url (default: mkdocs.yml).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, summary = validate_built_site(
        args.site_dir,
        args.contract,
        args.config,
    )
    if errors:
        print("Built site check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Built site check passed: "
        f"{summary.redirects} redirects, "
        f"{summary.search_documents} search documents, "
        f"{summary.sitemap_urls} sitemap URLs, "
        f"{summary.not_found_links} 404 links checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
