#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys


@dataclass(frozen=True)
class PublicCopyPattern:
    name: str
    pattern: re.Pattern[str]
    paths: tuple[str, ...] | None = None

    def applies_to(self, relative_path: str) -> bool:
        return self.paths is None or relative_path in self.paths


@dataclass(frozen=True)
class PublicAbbreviationRequirement:
    name: str
    token_pattern: re.Pattern[str]
    explanation_pattern: re.Pattern[str]


@dataclass(frozen=True)
class PublicLineRequirement:
    name: str
    trigger_pattern: re.Pattern[str]
    required_pattern: re.Pattern[str]
    paths: tuple[str, ...] | None = None

    def applies_to(self, relative_path: str) -> bool:
        return self.paths is None or relative_path in self.paths


PUBLIC_COPY_PATTERNS = [
    PublicCopyPattern(
        "verbose rationale heading",
        re.compile(r"^\s*\*\*왜 이 해결 방법인지:\*\*", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "opaque CAU rationale wording",
        re.compile(
            r"같은\s+metadata/generation\s+boundary|"
            r"same\s+metadata\s+and\s+generation\s+boundary|"
            r"read\s*시점|select\s+SQL\s+기준|select\s+SQL\s+criteria|"
            r"단순\s+audit\s+log로만|simple\s+audit\s+log",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "internal CAU acronym",
        re.compile(r"\bCAU\b"),
    ),
    PublicCopyPattern(
        "resolution-as-closing wording",
        re.compile(
            r"닫(?:았|았고|았습니다|는|으려면|고,|습니다)|"
            r"\bclosed\b.*\b(criteria|invariant|issue|problem|with)|"
            r"\bclose\b.*\b(issue|problem|criteria)",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "opaque generated-platform jargon",
        re.compile(
            r"generated[- ]service|generated\s+CRUD\s+service|"
            r"row[- ]snapshot|snapshot\s+copy|snapshot\s+재구성|"
            r"generation\s+boundary|metadata/generation\s+boundary|"
            r"storage[- ]surface|query\s+semantics|test[- ]suite|"
            r"경로로\s*구현|세대\s*경계|생성\s*경계",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "ambiguous supporting-structure wording",
        re.compile(r"보조\s*구조|supporting\s+structural\s+work", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "ambiguous Coupler operating-label wording",
        re.compile(
            r"개인\s*제품\s*Coupler\s*운영\s*기준|"
            r"Operating\s+criteria\s+for\s+the\s+personal\s+product\s+Coupler",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "opaque bundled-flow wording",
        re.compile(
            r"같은\s+[^.\n]{0,60}(?:흐름|thread|flow)\s+안에서\s+다뤘|"
            r"as\s+part\s+of\s+the\s+same\s+[^.\n]{0,60}(?:thread|flow)",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "evidence-style section heading",
        re.compile(
            r"^\s*#{1,6}\s+(검증\s+가능한\s+근거|Verifiable\s+Evidence)\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "standalone CLI application heading",
        re.compile(r"^\s*#{1,6}\s+CLI\s+Application\s*$", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "inconsistent numbered Parquet PR label",
        re.compile(r"Parquet\s+Storage\s+PR\s+#\d+", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "HOG CVE/parser misclassification",
        re.compile(
            r"\bHOG\b.*(?:CVE|parser|parse|parsing|파싱|파서)|"
            r"(?:CVE|parser|parse|parsing|파싱|파서).*\bHOG\b",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "internal public-boundary wording",
        re.compile(r"공개\s*(경계|범위)|public\s+(boundary|scope)", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "private evidence wording",
        re.compile(
            r"비공개|private\s+(repository|repo|issue|PR|link)",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "claim-boundary wording",
        re.compile(r"claim[- ]boundary|claim\s+scoped|주장\s*경계", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "source-record wording",
        re.compile(
            r"기록되어\s*(있습니다|있다|있는|있으며)?|"
            r"source\s+record\s+says|recorded\s+in\s+the\s+source",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "page-framing wording",
        re.compile(
            r"이\s*페이지(?:는|에서는)?|This\s+page\s+(?:is|presents|keeps|summarizes)",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "supporting-evidence wording",
        re.compile(
            r"supporting\s+evidence|not\s+a\s+separate\s+catalog|"
            r"대표\s*작업이\s*아니라",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "shallow portfolio headings",
        re.compile(
            r"^\s*(내가\s+한\s+일|검증/결과|What\s+I\s+did|Validation/result)\s*:",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "tool-centered homepage wording",
        re.compile(r"\bAI\s+agents?", re.IGNORECASE),
        paths=(
            "index.md",
            "index.en.md",
            "experience/index.md",
            "experience/index.en.md",
        ),
    ),
    PublicCopyPattern(
        "internal preparation wording",
        re.compile(
            r"case\s+stud(y|ies)|casebook|readiness|work\s+status|backlog|"
            r"대표\s*사례|사례집|경로\s*묶음",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "defensive metric wording",
        re.compile(
            r"사용자 수나 전환율이 아니라|event count로만|"
            r"not as (a )?(user-count|conversion-rate)|"
            r"I use this only",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "stale Coupler postback baseline",
        re.compile(
            r"(?:약\s*)?40(?:개|건|events?)?[^.\n]{0,80}1\.1k|"
            r"1\.1k[^.\n]{0,80}(?:약\s*)?40(?:개|건|events?)?",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "unverified Coupler conversion-cost metric",
        re.compile(
            r"전환율|가입\s*성공률|심사\s*시간\s*단축|"
            r"광고\s*단가|광고비|\bCAC\b|\bCPA\b|"
            r"cost\s+per|conversion\s+rate|signup\s+success|review\s+time",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "defensive implementation wording",
        re.compile(
            r"구현 주장이 아니라|not a .*implementation claim|"
            r"전체 개발 생산성 일반화|broad productivity claim",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "sensitive local or secret wording",
        re.compile(
            r"/Users/|localhost|\.env|credential|secret|token|password|"
            r"production host|DB endpoint",
            re.IGNORECASE,
        ),
    ),
]


PUBLIC_ABBREVIATION_REQUIREMENTS: list[PublicAbbreviationRequirement] = []


PUBLIC_LINE_REQUIREMENTS = [
    PublicLineRequirement(
        "unqualified Coupler Meta SDK postback metric",
        re.compile(r"(?=.*(?:약\s*)?50(?:개|건)?)(?=.*1\.1k)", re.IGNORECASE),
        re.compile(r"Meta\s+SDK\s+postback\s+event\s+count", re.IGNORECASE),
    ),
    PublicLineRequirement(
        "unqualified HOG wording",
        re.compile(r"\bHOG\b"),
        re.compile(
            r"탐지|detection|config|configuration|period|운영|operational|"
            r"brute[- ]force|threat|위협|network\s+event|네트워크\s*이벤트",
            re.IGNORECASE,
        ),
    ),
]


@dataclass(frozen=True)
class PublicCopySummary:
    checked_files: int
    findings: int


def collect_abbreviation_findings(docs_dir: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(docs_dir.rglob("*.md")):
        relative_path = path.relative_to(docs_dir).as_posix()
        text = path.read_text(encoding="utf-8")

        for requirement in PUBLIC_ABBREVIATION_REQUIREMENTS:
            if not requirement.token_pattern.search(text):
                continue
            if requirement.explanation_pattern.search(text):
                continue

            for line_number, line in enumerate(text.splitlines(), start=1):
                if requirement.token_pattern.search(line):
                    findings.append(
                        f"{relative_path}:{line_number}: "
                        f"{requirement.name}: {line.strip()}"
                    )
                    break

    return findings


def collect_public_copy_findings(docs_dir: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(docs_dir.rglob("*.md")):
        relative_path = path.relative_to(docs_dir).as_posix()
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            for copy_pattern in PUBLIC_COPY_PATTERNS:
                if copy_pattern.applies_to(relative_path) and copy_pattern.pattern.search(line):
                    findings.append(
                        f"{relative_path}:{line_number}: "
                        f"{copy_pattern.name}: {line.strip()}"
                    )
                    break

            for requirement in PUBLIC_LINE_REQUIREMENTS:
                if not requirement.applies_to(relative_path):
                    continue
                if not requirement.trigger_pattern.search(line):
                    continue
                if requirement.required_pattern.search(line):
                    continue

                findings.append(
                    f"{relative_path}:{line_number}: "
                    f"{requirement.name}: {line.strip()}"
                )
                break

    findings.extend(collect_abbreviation_findings(docs_dir))
    return findings


def validate_public_copy(
    docs_dir: Path,
) -> tuple[list[str], PublicCopySummary]:
    markdown_files = list(docs_dir.rglob("*.md"))
    findings = collect_public_copy_findings(docs_dir)
    return findings, PublicCopySummary(len(markdown_files), len(findings))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke-test public portfolio copy for internal review wording."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path("docs"),
        help="Documentation directory (default: docs).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    findings, summary = validate_public_copy(args.docs_dir)
    if findings:
        print("Public copy check failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1

    print(
        "Public copy check passed: "
        f"{summary.checked_files} files checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
