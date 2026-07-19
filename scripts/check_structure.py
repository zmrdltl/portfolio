#!/usr/bin/env python3

from __future__ import annotations

import argparse
from collections import Counter
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


class MkDocsConfigLoader(yaml.SafeLoader):
    pass


def construct_python_name(loader: Any, tag_suffix: str, node: Any) -> str:
    # MkDocs may use Python-name tags for extension callbacks. The
    # structure check only needs nav/plugin metadata, so keep them inert.
    return tag_suffix


MkDocsConfigLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    construct_python_name,
)


ENGLISH_SUFFIX = ".en.md"
MARKDOWN_SUFFIX = ".md"
FORBIDDEN_STATIC_FILENAMES = {".DS_Store"}
HANGUL_PATTERN = re.compile(r"[가-힣]")
HEADING_PATTERN = re.compile(r"^(#{1,6})[ \t]+\S")
FENCE_OPEN_PATTERN = re.compile(r"^[ \t]*(`{3,}|~{3,})")
FRONT_MATTER_BOUNDARY = "---"
ALLOWED_OFF_NAV_ROLES = {"appendix", "legacy_redirect"}
META_REFRESH_PATTERN = re.compile(
    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\']0;\s*url=\.\./["\']\s*/?>',
    re.IGNORECASE,
)
FALLBACK_HOME_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(\.\./\)")


@dataclass(frozen=True)
class StructureSummary:
    translation_pairs: int
    nav_pages: int


def read_config(config_path: Path) -> dict[str, Any]:
    try:
        config = yaml.load(
            config_path.read_text(encoding="utf-8"),
            Loader=MkDocsConfigLoader,
        )
    except (FileNotFoundError, yaml.YAMLError):
        return {}

    return config if isinstance(config, dict) else {}


def find_i18n_config(config: dict[str, Any]) -> dict[str, Any] | None:
    plugins = config.get("plugins", [])
    if not isinstance(plugins, list):
        return None

    for plugin in plugins:
        if isinstance(plugin, dict) and isinstance(plugin.get("i18n"), dict):
            return plugin["i18n"]

    return None


def find_language(
    i18n_config: dict[str, Any], locale: str
) -> dict[str, Any] | None:
    languages = i18n_config.get("languages", [])
    if not isinstance(languages, list):
        return None

    for language in languages:
        if isinstance(language, dict) and language.get("locale") == locale:
            return language

    return None


def collect_nav(
    nav: Any,
) -> tuple[list[str], list[str], list[str]]:
    paths: list[str] = []
    titles: list[str] = []
    errors: list[str] = []

    def visit(items: Any, location: str) -> None:
        if not isinstance(items, list):
            errors.append(f"{location} must be a list.")
            return

        for index, item in enumerate(items):
            item_location = f"{location}[{index}]"
            if isinstance(item, str):
                paths.append(item)
                continue

            if not isinstance(item, dict):
                errors.append(
                    f"{item_location} must be a page path or title mapping."
                )
                continue

            for title, target in item.items():
                titles.append(str(title))
                if isinstance(target, str):
                    paths.append(target)
                elif isinstance(target, list):
                    visit(target, f"{item_location}.{title}")
                else:
                    errors.append(
                        f"{item_location}.{title} must contain a page path "
                        "or nested navigation list."
                    )

    visit(nav, "nav")
    return paths, titles, errors


def heading_outline(path: Path) -> list[int]:
    outline: list[int] = []
    fence_character: str | None = None
    fence_length = 0

    for line in path.read_text(encoding="utf-8").splitlines():
        if fence_character is not None:
            closing_marker = line.strip(" \t")
            if (
                closing_marker
                and set(closing_marker) == {fence_character}
                and len(closing_marker) >= fence_length
            ):
                fence_character = None
                fence_length = 0
            continue

        fence_match = FENCE_OPEN_PATTERN.match(line)
        if fence_match:
            opening_marker = fence_match.group(1)
            fence_character = opening_marker[0]
            fence_length = len(opening_marker)
            continue

        heading_match = HEADING_PATTERN.match(line)
        if heading_match:
            outline.append(len(heading_match.group(1)))

    return outline


def page_metadata(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_BOUNDARY:
        return {}

    try:
        closing_index = next(
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.strip() == FRONT_MATTER_BOUNDARY
        )
    except StopIteration:
        return {}

    try:
        metadata = yaml.safe_load("\n".join(lines[1:closing_index]))
    except yaml.YAMLError:
        return {}
    return metadata if isinstance(metadata, dict) else {}


def validate_off_nav_page(path: Path, relative_path: str) -> list[str]:
    metadata = page_metadata(path)
    role = metadata.get("portfolio_role")
    if role not in ALLOWED_OFF_NAV_ROLES:
        return [f"Page missing from nav: {relative_path}."]
    if role != "legacy_redirect":
        return []

    errors: list[str] = []
    redirect_to = metadata.get("redirect_to")
    search = metadata.get("search")
    if redirect_to != "../":
        errors.append(
            f"Legacy redirect must target same-language home in one hop: {relative_path}."
        )
    if not isinstance(search, dict) or search.get("exclude") is not True:
        errors.append(f"Legacy redirect must be excluded from search: {relative_path}.")

    text = path.read_text(encoding="utf-8")
    if META_REFRESH_PATTERN.search(text) is None:
        errors.append(f"Legacy redirect is missing a one-hop meta refresh: {relative_path}.")
    if FALLBACK_HOME_LINK_PATTERN.search(text) is None:
        errors.append(f"Legacy redirect is missing a fallback home link: {relative_path}.")
    return errors


def validate_structure(
    docs_dir: Path, config_path: Path
) -> tuple[list[str], StructureSummary]:
    errors: list[str] = []
    for path in sorted(docs_dir.rglob("*")):
        if path.is_file() and path.name in FORBIDDEN_STATIC_FILENAMES:
            relative_path = path.relative_to(docs_dir).as_posix()
            errors.append(f"Forbidden static file in docs: {relative_path}.")

    markdown_files = sorted(
        path.relative_to(docs_dir).as_posix()
        for path in docs_dir.rglob(f"*{MARKDOWN_SUFFIX}")
        if path.is_file()
    )
    default_pages = sorted(
        path for path in markdown_files if not path.endswith(ENGLISH_SUFFIX)
    )
    english_pages = sorted(
        path for path in markdown_files if path.endswith(ENGLISH_SUFFIX)
    )

    for default_page in default_pages:
        english_page = (
            default_page[: -len(MARKDOWN_SUFFIX)] + ENGLISH_SUFFIX
        )
        if english_page not in english_pages:
            errors.append(
                f"Missing English translation: {english_page} "
                f"(source: {default_page})."
            )
            continue

        default_outline = heading_outline(docs_dir / default_page)
        english_outline = heading_outline(docs_dir / english_page)
        if default_outline != english_outline:
            errors.append(
                f"Heading outline mismatch: {default_page} "
                f"{default_outline} != {english_page} {english_outline}."
            )

        default_role = page_metadata(docs_dir / default_page).get("portfolio_role")
        english_role = page_metadata(docs_dir / english_page).get("portfolio_role")
        if default_role != english_role:
            errors.append(
                f"Portfolio role mismatch: {default_page} {default_role!r} != "
                f"{english_page} {english_role!r}."
            )

    for english_page in english_pages:
        default_page = english_page[: -len(ENGLISH_SUFFIX)] + MARKDOWN_SUFFIX
        if default_page not in default_pages:
            errors.append(
                f"Missing default-language source: {default_page} "
                f"(translation: {english_page})."
            )

    config = read_config(config_path)
    if not config:
        errors.append(f"Unable to read MkDocs config: {config_path}.")
        return errors, StructureSummary(len(default_pages), 0)

    nav_paths, nav_titles, nav_errors = collect_nav(config.get("nav"))
    errors.extend(nav_errors)
    local_nav_paths = [path for path in nav_paths if path.endswith(MARKDOWN_SUFFIX)]
    nav_path_counts = Counter(local_nav_paths)

    for path, count in sorted(nav_path_counts.items()):
        if count > 1:
            errors.append(f"Duplicate nav page: {path} appears {count} times.")

    default_page_set = set(default_pages)
    nav_page_set = set(local_nav_paths)
    for path in sorted(default_page_set - nav_page_set):
        errors.extend(validate_off_nav_page(docs_dir / path, path))
    for path in sorted(nav_page_set - default_page_set):
        errors.append(f"Nav references an unknown default-language page: {path}.")

    i18n_config = find_i18n_config(config)
    if i18n_config is None:
        errors.append("Missing mkdocs-static-i18n plugin configuration.")
        return errors, StructureSummary(len(default_pages), len(local_nav_paths))

    if i18n_config.get("docs_structure") != "suffix":
        errors.append("i18n docs_structure must remain `suffix`.")

    korean = find_language(i18n_config, "ko")
    english = find_language(i18n_config, "en")
    if korean is None or korean.get("default") is not True:
        errors.append("Korean locale must exist and remain the default language.")
    elif korean.get("build") is not True:
        errors.append("Korean locale build must remain enabled.")
    if english is None:
        errors.append("English locale configuration is missing.")
    else:
        if english.get("build") is not True:
            errors.append("English locale build must remain enabled.")

        if "nav" in english:
            errors.append(
                "English locale must use nav_translations instead of "
                "duplicating the full nav."
            )

        nav_translations = english.get("nav_translations")
        if not isinstance(nav_translations, dict):
            errors.append("English locale must define nav_translations.")
            nav_translations = {}

        normalized_nav_translations = {
            str(title): translation
            for title, translation in nav_translations.items()
        }
        unknown_titles = sorted(
            set(normalized_nav_translations) - set(nav_titles)
        )
        for title in unknown_titles:
            errors.append(
                f"nav_translations contains a title not present in nav: {title}."
            )

        for title, translation in sorted(normalized_nav_translations.items()):
            if not isinstance(translation, str) or not translation.strip():
                errors.append(
                    f"English nav translation must be a non-empty string: {title}."
                )

        translated_titles = set(normalized_nav_translations)
        for title in sorted(set(nav_titles)):
            if HANGUL_PATTERN.search(title) and title not in translated_titles:
                errors.append(f"Missing English nav translation: {title}.")

    return errors, StructureSummary(len(default_pages), len(local_nav_paths))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Korean/English MkDocs portfolio structure."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path("docs"),
        help="Documentation directory (default: docs).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("mkdocs.yml"),
        help="MkDocs configuration path (default: mkdocs.yml).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, summary = validate_structure(args.docs_dir, args.config)
    if errors:
        print("Portfolio structure check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Portfolio structure check passed: "
        f"{summary.translation_pairs} translation pairs, "
        f"{summary.nav_pages} nav pages."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
