#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Any

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


@dataclass(frozen=True)
class BuiltSiteSummary:
    search_documents: int
    redirects: int


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


def validate_built_site(
    site_dir: Path, contract_path: Path | None = None
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

    return errors, BuiltSiteSummary(total_documents, len(redirect_paths))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated redirects and search indexes."
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, summary = validate_built_site(args.site_dir, args.contract)
    if errors:
        print("Built site check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Built site check passed: "
        f"{summary.redirects} redirects, "
        f"{summary.search_documents} search documents checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
