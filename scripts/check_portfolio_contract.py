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


@dataclass(frozen=True)
class ContractSummary:
    checked_pages: int
    representative_items: int


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


def extract_representative_links(path: Path, heading: str) -> tuple[list[str], list[str]]:
    section_lines, error = extract_section_lines(path, heading)
    if error:
        return [], [error]

    errors: list[str] = []
    links: list[str] = []
    for offset, line in enumerate(section_lines, start=1):
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue

        link_match = MARKDOWN_LINK_PATTERN.search(stripped)
        if not link_match:
            errors.append(f"{path}:{offset}: Representative item has no link.")
            continue

        links.append(normalize_link(link_match.group(1)))

    return links, errors


def validate_contract(
    contract_path: Path,
) -> tuple[list[str], ContractSummary]:
    contract = read_contract(contract_path)
    if not contract:
        return [f"Unable to read portfolio contract: {contract_path}."], ContractSummary(0, 0)

    homepage = contract.get("homepage")
    if not isinstance(homepage, dict):
        return ["Contract must define `homepage`."], ContractSummary(0, 0)

    representative_work = homepage.get("representative_work")
    if not isinstance(representative_work, dict):
        return ["Contract must define `homepage.representative_work`."], ContractSummary(0, 0)

    pages = homepage.get("pages")
    required_links = representative_work.get("required_links")
    max_items = representative_work.get("max_items")
    supporting_only_links = homepage.get("supporting_only_links", [])

    errors: list[str] = []
    if not isinstance(pages, list) or not pages:
        errors.append("Contract must define at least one homepage page.")
        pages = []
    if not isinstance(required_links, list) or not all(
        isinstance(link, str) for link in required_links
    ):
        errors.append("Contract required_links must be a list of strings.")
        required_links = []
    if not isinstance(max_items, int) or max_items < 1:
        errors.append("Contract max_items must be a positive integer.")
        max_items = 0
    if not isinstance(supporting_only_links, list) or not all(
        isinstance(link, str) for link in supporting_only_links
    ):
        errors.append("Contract supporting_only_links must be a list of strings.")
        supporting_only_links = []

    total_items = 0
    supporting_only_set = set(supporting_only_links)
    for page in pages:
        if not isinstance(page, dict):
            errors.append("Each homepage page contract entry must be a mapping.")
            continue

        page_path_value = page.get("path")
        heading = page.get("representative_heading")
        if not isinstance(page_path_value, str) or not isinstance(heading, str):
            errors.append("Homepage page entries must define path and representative_heading.")
            continue

        page_path = Path(page_path_value)
        if not page_path.exists():
            errors.append(f"Homepage page does not exist: {page_path}.")
            continue

        links, link_errors = extract_representative_links(page_path, heading)
        errors.extend(link_errors)
        total_items += len(links)

        if len(links) > max_items:
            errors.append(
                f"{page_path}: Representative Work has {len(links)} items; "
                f"contract allows at most {max_items}."
            )

        if links != required_links:
            errors.append(
                f"{page_path}: Representative links must be "
                f"{required_links}, found {links}."
            )

        blocked_links = [link for link in links if link in supporting_only_set]
        if blocked_links:
            errors.append(
                f"{page_path}: Supporting-only links cannot appear as "
                f"Representative Work: {blocked_links}."
            )

    return errors, ContractSummary(len(pages), total_items)


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
