#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import dataclass
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


HEADING_PATTERN = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class ContractSummary:
    checked_pages: int
    representative_items: int


@dataclass(frozen=True)
class RepresentativeRecord:
    link: str
    lines: tuple[str, ...]


def read_contract(contract_path: Path) -> dict[str, Any]:
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, yaml.YAMLError):
        return {}

    return contract if isinstance(contract, dict) else {}


def normalize_link(link: str) -> str:
    return link.split("#", 1)[0]


def extract_section_lines(path: Path, heading: str) -> tuple[list[str], str | None]:
    lines = path.read_text(encoding="utf-8").splitlines()
    section_lines: list[str] = []
    in_section = False
    section_level: int | None = None

    for line in lines:
        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            if in_section and section_level is not None and level <= section_level:
                break
            if title == heading:
                in_section = True
                section_level = level
                continue

        if in_section:
            section_lines.append(line)

    if not in_section:
        return [], f"Missing homepage representative heading: {path}:{heading}"

    return section_lines, None


def extract_representative_records(
    path: Path,
    heading: str,
) -> tuple[list[RepresentativeRecord], list[str]]:
    section_lines, error = extract_section_lines(path, heading)
    if error:
        return [], [error]

    records: list[RepresentativeRecord] = []
    current_link: str | None = None
    current_lines: list[str] = []
    errors: list[str] = []

    def flush() -> None:
        nonlocal current_link, current_lines
        if current_link is not None:
            records.append(
                RepresentativeRecord(current_link, tuple(current_lines))
            )
        current_link = None
        current_lines = []

    for line in section_lines:
        heading_match = HEADING_PATTERN.match(line)
        if heading_match and len(heading_match.group(1)) == 3:
            flush()
            link_match = MARKDOWN_LINK_PATTERN.search(heading_match.group(2))
            if link_match is None:
                errors.append(f"{path}: Representative heading has no link: {line}")
                continue
            current_link = normalize_link(link_match.group(1))
            continue
        if current_link is not None:
            current_lines.append(line)

    flush()
    return records, errors


def extract_field_values(lines: tuple[str, ...], label: str) -> list[str]:
    pattern = re.compile(
        rf"^\s*\*\*{re.escape(label)}:\*\*\s*(.+?)\s*$",
        re.IGNORECASE,
    )
    return [match.group(1) for line in lines if (match := pattern.match(line))]


def missing_terms(value: str, required_terms: list[str]) -> list[str]:
    normalized = value.casefold()
    return [term for term in required_terms if term.casefold() not in normalized]


def validate_page_records(
    page_path: Path,
    page: dict[str, Any],
    required_links: list[str],
    exact_items: int,
) -> tuple[list[str], int]:
    errors: list[str] = []
    heading = page.get("representative_heading")
    labels = page.get("field_labels")
    record_contracts = page.get("records")
    if not isinstance(heading, str) or not isinstance(labels, dict) or not isinstance(
        record_contracts, dict
    ):
        return [
            f"{page_path}: Homepage page must define representative_heading, "
            "field_labels, and records."
        ], 0

    required_fields = ("type_period", "role", "change", "proof", "technologies")
    if any(not isinstance(labels.get(field), str) for field in required_fields):
        return [f"{page_path}: field_labels must define {list(required_fields)}."], 0

    records, record_errors = extract_representative_records(page_path, heading)
    errors.extend(record_errors)
    links = [record.link for record in records]
    if len(records) != exact_items:
        errors.append(
            f"{page_path}: Representative Work must have exactly {exact_items} "
            f"records, found {len(records)}."
        )
    if links != required_links:
        errors.append(
            f"{page_path}: Representative links must be {required_links}, found {links}."
        )

    record_by_link = {record.link: record for record in records}
    for link in required_links:
        record = record_by_link.get(link)
        contract = record_contracts.get(link)
        if record is None:
            continue
        if not isinstance(contract, dict):
            errors.append(f"{page_path}: Missing record contract for {link}.")
            continue

        for field in required_fields:
            label = labels[field]
            values = extract_field_values(record.lines, label)
            if len(values) != 1:
                errors.append(
                    f"{page_path}: {link} must have exactly one `{label}` field; "
                    f"found {len(values)}."
                )
                continue

            value = values[0]
            if field == "technologies":
                tags = INLINE_CODE_PATTERN.findall(value)
                expected_tags = contract.get("technologies")
                if not isinstance(expected_tags, list) or not all(
                    isinstance(tag, str) for tag in expected_tags
                ):
                    errors.append(
                        f"{page_path}: {link} technologies contract must be a list."
                    )
                    continue
                if not 2 <= len(tags) <= 3:
                    errors.append(
                        f"{page_path}: {link} must expose 2-3 technology tags; "
                        f"found {tags}."
                    )
                if tags != expected_tags:
                    errors.append(
                        f"{page_path}: {link} technology tags must be "
                        f"{expected_tags}, found {tags}."
                    )
                visible_without_tags = INLINE_CODE_PATTERN.sub("", value)
                if visible_without_tags.replace("·", "").strip():
                    errors.append(
                        f"{page_path}: {link} technology field must contain only tags."
                    )
                continue

            required_terms = contract.get(field)
            if not isinstance(required_terms, list) or not all(
                isinstance(term, str) for term in required_terms
            ):
                errors.append(
                    f"{page_path}: {link} `{field}` contract must be a list of terms."
                )
                continue
            missing = missing_terms(value, required_terms)
            if missing:
                errors.append(
                    f"{page_path}: {link} `{label}` is missing {missing}."
                )

    forbidden_headings = page.get("forbidden_headings", [])
    if not isinstance(forbidden_headings, list) or not all(
        isinstance(item, str) for item in forbidden_headings
    ):
        errors.append(f"{page_path}: forbidden_headings must be a list of strings.")
    else:
        page_headings = {
            match.group(2).strip().casefold()
            for line in page_path.read_text(encoding="utf-8").splitlines()
            if (match := HEADING_PATTERN.match(line))
        }
        for forbidden in forbidden_headings:
            if forbidden.casefold() in page_headings:
                errors.append(
                    f"{page_path}: Forbidden duplicate-summary heading: {forbidden}."
                )

    return errors, len(records)


def validate_content_coverage(entries: Any) -> tuple[list[str], int]:
    if not isinstance(entries, list):
        return ["Contract content_coverage must be a list."], 0

    errors: list[str] = []
    checked = 0
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("Each content_coverage entry must be a mapping.")
            continue
        path_value = entry.get("path")
        required_terms = entry.get("required_terms")
        forbidden_headings = entry.get("forbidden_headings", [])
        if (
            not isinstance(path_value, str)
            or not isinstance(required_terms, list)
            or not all(isinstance(term, str) for term in required_terms)
            or not isinstance(forbidden_headings, list)
            or not all(isinstance(item, str) for item in forbidden_headings)
        ):
            errors.append(
                "Content coverage entries must define path, required_terms, "
                "and optional forbidden_headings as strings."
            )
            continue

        path = Path(path_value)
        if not path.exists():
            errors.append(f"Content coverage page does not exist: {path}.")
            continue
        checked += 1
        text = path.read_text(encoding="utf-8")
        missing = missing_terms(text, required_terms)
        if missing:
            errors.append(f"{path}: Required content coverage is missing {missing}.")

        headings = {
            match.group(2).strip().casefold()
            for line in text.splitlines()
            if (match := HEADING_PATTERN.match(line))
        }
        for forbidden in forbidden_headings:
            if forbidden.casefold() in headings:
                errors.append(f"{path}: Forbidden standalone heading: {forbidden}.")

    return errors, checked


def validate_contract(contract_path: Path) -> tuple[list[str], ContractSummary]:
    contract = read_contract(contract_path)
    if not contract:
        return [f"Unable to read portfolio contract: {contract_path}."], ContractSummary(0, 0)

    homepage = contract.get("homepage")
    if not isinstance(homepage, dict):
        return ["Contract must define `homepage`."], ContractSummary(0, 0)

    representative_work = homepage.get("representative_work")
    pages = homepage.get("pages")
    if not isinstance(representative_work, dict) or not isinstance(pages, list):
        return [
            "Contract must define homepage.pages and homepage.representative_work."
        ], ContractSummary(0, 0)

    required_links = representative_work.get("required_links")
    exact_items = representative_work.get("exact_items")
    if not isinstance(required_links, list) or not all(
        isinstance(link, str) for link in required_links
    ):
        required_links = []
    if not isinstance(exact_items, int) or exact_items < 1:
        exact_items = 0

    errors: list[str] = []
    if not required_links:
        errors.append("Contract required_links must be a non-empty list of strings.")
    if exact_items < 1:
        errors.append("Contract exact_items must be a positive integer.")

    total_items = 0
    checked_pages = 0
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("path"), str):
            errors.append("Each homepage page contract entry must define a path.")
            continue
        page_path = Path(page["path"])
        if not page_path.exists():
            errors.append(f"Homepage page does not exist: {page_path}.")
            continue
        page_errors, item_count = validate_page_records(
            page_path, page, required_links, exact_items
        )
        errors.extend(page_errors)
        total_items += item_count
        checked_pages += 1

    coverage_errors, coverage_pages = validate_content_coverage(
        contract.get("content_coverage", [])
    )
    errors.extend(coverage_errors)
    return errors, ContractSummary(checked_pages + coverage_pages, total_items)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate portfolio pages against the release contract."
    )
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path("portfolio.contract.yml"),
        help="Portfolio contract path (default: portfolio.contract.yml).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, summary = validate_contract(args.contract)
    if errors:
        print("Portfolio contract check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Portfolio contract check passed: "
        f"{summary.checked_pages} pages, "
        f"{summary.representative_items} representative items checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
