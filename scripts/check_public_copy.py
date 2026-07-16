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


COUPLER_PUBLIC_PATHS = (
    "index.md",
    "index.en.md",
    "projects/coupler.md",
    "projects/coupler.en.md",
)

COUPLER_APPROXIMATE_COMPARISON = (
    r"(?=.*(?:약\s*|(?:about|around|roughly|approximately)\s+|~\s*)"
    r"10(?!\d))"
    r"(?=.*(?:약\s*|(?:about|around|roughly|approximately)\s+|~\s*)"
    r"100(?!\d))"
    r"(?=.*(?:에서|까지|개편\s*전|개편\s*후|변경\s*전|변경\s*후|"
    r"before|after|from|\bto\b|→|->))"
)

COUPLER_COMPLETE_REGISTRATION_COMPARISON = (
    r"(?=.*(?:CompleteRegistration|등록\s*완료))"
    r"(?=.*(?<!\d)10(?!\d))"
    r"(?=.*(?<!\d)100(?!\d))"
    r"(?=.*(?:에서|까지|개편\s*전|개편\s*후|변경\s*전|변경\s*후|"
    r"before|after|from|\bto\b|→|->))"
)

COUPLER_STALE_COMPARISON = (
    r"(?=.*(?<!\d)(?:40|50)(?![\d.]))"
    r"(?=.*(?<![\d.])(?:1\.1k|1,100|1100)(?![A-Za-z0-9_,.]))"
    r"(?=.*(?:에서|부터|까지|전후|비교|→|->|\bfrom\b|\bto\b|"
    r"\bbefore\b|\bafter\b|\bversus\b|\bvs\.?\b))"
)

COUPLER_GROWTH_WORDING = (
    r"증가|늘(?:어|었|어난|어났)|\bgrowth\b|"
    r"\bincreas(?:e|ed|es|ing)\b|\bgrew\b|\bgrown\b|"
    r"\brose\b|\bris(?:e|en|es|ing)\b"
)

COUPLER_PARAGRAPH_PATTERNS = (
    PublicCopyPattern(
        "stale Coupler pre-CompleteRegistration comparison",
        re.compile(COUPLER_STALE_COMPARISON, re.IGNORECASE),
        paths=COUPLER_PUBLIC_PATHS,
    ),
    PublicCopyPattern(
        "unsupported Coupler CompleteRegistration metric interpretation",
        re.compile(
            COUPLER_COMPLETE_REGISTRATION_COMPARISON
            + r"(?=.*(?:"
            r"(?<!\d)100\s*(?:명|users?\b)|"
            r"가입\s*(?:완료|성공)\s*(?:건수|횟수|수|건|명)|"
            r"(?:완료|성공)(?:한|된)?\s*가입\s*(?:건수|횟수|수|건|명)|"
            r"(?:completed|successful)\s+(?:registrations?|signups?)"
            r"(?:\s+counts?)?|"
            r"(?:registration|signup)\s+(?:completion|success)(?:es)?"
            r"(?:\s+counts?)?|"
            r"개편\s*으로|때문에|caused\s+by|led\s+to|resulted\s+in|"
            r"1\s*개월|월간|monthly|one[-\s]+month"
            r"))",
            re.IGNORECASE,
        ),
        paths=COUPLER_PUBLIC_PATHS,
    ),
    PublicCopyPattern(
        "unsupported Coupler CompleteRegistration growth wording",
        re.compile(
            COUPLER_APPROXIMATE_COMPARISON
            + rf"(?=.*(?:{COUPLER_GROWTH_WORDING}))",
            re.IGNORECASE,
        ),
        paths=COUPLER_PUBLIC_PATHS,
    ),
)

COUPLER_PARAGRAPH_REQUIREMENTS = (
    PublicLineRequirement(
        "unqualified Coupler Meta SDK observation",
        re.compile(COUPLER_APPROXIMATE_COMPARISON, re.IGNORECASE),
        re.compile(
            r"(?=.*Meta\s+SDK)"
            r"(?=.*(?:최초\s+가입\s+심사|first\s+signup\s+review))"
            r"(?=.*(?:관측|\bobserved\b))",
            re.IGNORECASE,
        ),
        paths=COUPLER_PUBLIC_PATHS,
    ),
    PublicLineRequirement(
        "non-canonical Coupler observation wording",
        re.compile(COUPLER_APPROXIMATE_COMPARISON, re.IGNORECASE),
        re.compile(
            r"^(?:"
            r"Meta SDK 최초 가입 심사 도달 이벤트:\s*"
            r"개편 전 약 10건,\s*개편 후 약 100건 관측|"
            r"Meta SDK first signup review event:\s*"
            r"observed about 10 times before the redesign and "
            r"about 100 times after\."
            r")$",
            re.IGNORECASE,
        ),
        paths=("projects/coupler.md", "projects/coupler.en.md"),
    ),
)


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
            r"특정\s*시점\s*상태\s*재구성|상태\s*계약\s*재구성|"
            r"point[- ]in[- ]time\s+state\s+reconstruction|"
            r"generation\s+boundary|metadata/generation\s+boundary|"
            r"storage[- ]surface|query\s+semantics|test[- ]suite|"
            r"경로로\s*구현|세대\s*경계|생성\s*경계",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "vague no-code consistency wording",
        re.compile(
            r"일관되게\s*(?:이어|동작|처리|반영)|"
            r"실행\s*코드,\s*SQL,\s*DB\s*상태,\s*테스트\s*요청\s*형식|"
            r"사용자가\s*정의한\s*서비스와\s*제품\s*변경이\s*실제\s*코드,\s*SQL,\s*데이터\s*흐름|"
            r"service\s+definition(?:과|와)\s*코드\s*실행\s*결과의\s*일치|"
            r"같은\s+(?:generation|생성)\s+흐름|"
            r"connects\s+user-defined\s+services\s+and\s+product\s+changes\s+to\s+working\s+code|"
            r"consistent\s+as\s+it\s+turned\s+into|"
            r"consistency\s+between\s+service\s+definitions\s+and\s+code\s+execution|"
            r"\bone\s+generation\s+flow\b|\bsame\s+generation\s+flow\b",
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
        "abbreviated-year Coupler Korean portfolio period wording",
        re.compile(r"^\s*-\s*참여\s*기간:.*(?<!\d)\d{2}\.\d{2}(?!\.\d)"),
        paths=("projects/coupler.md",),
    ),
    PublicCopyPattern(
        "redundant Coupler phase metadata",
        re.compile(r"^\s*-\s*(?:참여\s*단계|Phases)\s*:", re.IGNORECASE),
        paths=("projects/coupler.md", "projects/coupler.en.md"),
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
        "generic display-consistency wording",
        re.compile(
            r"변경\s*안전성\s*기준|change[- ]safety|"
            r"\bevent\s+context\b|같은\s+event\s+context|"
            r"\bdrift\b|표시\s*drift",
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
        "opaque related-work criteria heading",
        re.compile(
            r"^\s*#{1,6}\s+(관련\s*작업\s*기준|Related\s+Work\s+Criteria)\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "opaque display-consistency criteria heading",
        re.compile(
            r"^\s*#{1,6}\s+("
            r"표시\s*일관성\s*검토\s*기준|"
            r"Display[- ]Consistency\s+Review\s+Criteria"
            r")\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "generic validation-criteria heading",
        re.compile(
            r"^\s*#{1,6}\s+(검증과\s*기준|Validation\s+and\s+Criteria)\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "standalone CLI application heading",
        re.compile(r"^\s*#{1,6}\s+CLI\s+Application\s*$", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "duplicative technical focus heading",
        re.compile(
            r"^\s*#{1,6}\s+(주요\s*기술\s*영역|Technical\s+Focus\s+Areas)\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "duplicative homepage engineering-perspective heading",
        re.compile(
            r"^\s*#{1,6}\s+(개발\s*운영\s*관점|Engineering\s+Operating\s+Perspective)\s*$",
            re.IGNORECASE,
        ),
        paths=("index.md", "index.en.md"),
    ),
    PublicCopyPattern(
        "duplicative work-direction heading",
        re.compile(r"^\s*#{1,6}\s+(엔지니어링\s*방향|Direction)\s*$", re.IGNORECASE),
        paths=("experience/index.md", "experience/index.en.md"),
    ),
    PublicCopyPattern(
        "curator-facing representative-work heading",
        re.compile(
            r"^\s*#{1,6}\s+(대표\s*작업으로\s*보는\s*이유|"
            r"Why\s+This\s+Is\s+Representative\s+Work)\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "internal contribution-boundary wording",
        re.compile(
            r"직접\s*구현[^.\n]{0,80}같은\s*성과로\s*합치지|"
            r"kept\s+direct\s+implementation[^.\n]{0,100}"
            r"separate\s+contribution\s+types",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "ambiguous Korean reservation-renewal wording",
        re.compile(r"용량\s*확인[^.\n]{0,60}예약\s*갱신", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "curator-facing supporting-validation heading",
        re.compile(
            r"^\s*#{1,6}\s+(보조\s*검증\s*작업|Supporting\s+Validation\s+Work)\s*$",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "inconsistent numbered Parquet PR label",
        re.compile(r"Parquet\s+Storage\s+PR\s+#\d+", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "stale GlueSQL merged PR count wording",
        re.compile(
            r"병합\s+PR\s+44\s*건(?:\s*이상)?|"
            r"44(?:\+)?\s+merged\s+PRs|"
            r"병합\s+PR\s+50\s*건\s*이상|"
            r"50\+\s+merged\s+PRs",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "internal entity export/import identifier",
        re.compile(r"Broker\s+App|selected_attr_ids|syncservice\.ftl", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "internal HOG product name",
        re.compile(r"\bHOG\b", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "opaque detection-period wording",
        re.compile(r"탐지\s*period|detection[- ]period|탐지\s*주기\s*설정", re.IGNORECASE),
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
        "public defensive claim-disclaimer wording",
        re.compile(
            r"주장하지\s*(?:않|말)|주장으로\s*쓰지|"
            r"I\s+do\s+not\s+(?:present|claim|generalize)|"
            r"do\s+not\s+claim|does\s+not\s+extend|"
            r"일반화하지\s*않",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "public claim-scope wording",
        re.compile(
            r"성과\s*범위|결과\s*범위|구현\s*범위|"
            r"(?:근거|결과|성과)[^.\n]{0,40}로\s*제한(?:했|했습니다|한다|합니다)|"
            r"Result\s+Scope|Implementation\s+Scope|"
            r"I\s+scoped\s+the\s+result|limited\s+the\s+result|"
            r"scope(?:d)?\s+the\s+result",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "scope-limiting public selection wording",
        re.compile(
            r"(?:대표|검증|작업|성과|결과|구현)\s*범위(?:는|를)?"
            r"[^.\n]{0,50}(?:좁|줄|제한|한정)|"
            r"\bI\s+(?:scoped|narrowed)\s+(?:the\s+)?"
            r"(?:work|scope|representative\s+scope)"
            r"[^.\n]{0,50}(?:to|into)",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "defensive direct-scope wording",
        re.compile(
            r"제가\s*맡은\s*범위|직접\s*담당한\s*범위가\s*아닙니다|"
            r"\bdirect\s+scope\b|outside\s+my\s+direct\s+scope",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "opaque working-criteria wording",
        re.compile(
            r"당시\s*작업\s*기준|당시\s*개발\s*환경에서|"
            r"in\s+the\s+working\s+environment|under\s+the\s+working\s+conditions",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "public performance-disclaimer wording",
        re.compile(
            r"\bp95\b|\bp99\b|\bbenchmark\b|별도\s*benchmark|"
            r"운영\s*로그|operating\s+logs?|\blatency\b|"
            r"지연\s*시간\s*개선",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "unsupported admission wording",
        re.compile(r"\badmission\b|\badmit(?:s|ted|ting)?\b", re.IGNORECASE),
    ),
    PublicCopyPattern(
        "overclaim absolute-solution wording",
        re.compile(
            r"정확히\s*해결|완전히\s*해결|매우\s+많은|수많은|"
            r"exactly\s+solv|fully\s+solv|very\s+many|huge\s+number",
            re.IGNORECASE,
        ),
    ),
    PublicCopyPattern(
        "unverified Coupler conversion-cost metric",
        re.compile(
            r"전환율|가입\s*성공률|심사\s*시간\s*단축|"
            r"광고\s*단가|광고비|(?<![A-Za-z])CAC(?![A-Za-z])|"
            r"(?<![A-Za-z])CPA(?![A-Za-z])|"
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
        "defensive Coupler AI-ownership wording",
        re.compile(
            r"LLM[^.\n]{0,100}사용했지만[^.\n]{0,160}직접\s*책임|"
            r"I\s+used\s+LLMs?[^.\n]{0,160}"
            r"while\s+I\s+remained\s+directly\s+responsible",
            re.IGNORECASE,
        ),
        paths=("projects/coupler.md", "projects/coupler.en.md"),
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
        "unqualified percentage comparison",
        re.compile(r"\d+%\s*(?:이상\s*)?(?:줄|감소|단축|개선|reduc|decreas|improv)", re.IGNORECASE),
        re.compile(
            r"변경\s*전|변경\s*후|전후|비교|1회|작업\s*시간|"
            r"before|after|compared|one\s+.*change|work\s+time|workflow",
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


def normalized_markdown_paragraphs(text: str) -> list[tuple[int, str]]:
    paragraphs: list[tuple[int, str]] = []
    paragraph_lines: list[str] = []
    start_line = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            paragraphs.append((start_line, " ".join(paragraph_lines)))
            paragraph_lines = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped_line = line.strip()
        if stripped_line:
            starts_markdown_block = bool(
                re.match(r"^(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|>\s|```|~~~|\|)", stripped_line)
            )
            if paragraph_lines and starts_markdown_block:
                flush_paragraph()
            if not paragraph_lines:
                start_line = line_number
            paragraph_lines.append(stripped_line)
            continue

        flush_paragraph()

    flush_paragraph()

    return paragraphs


def collect_coupler_paragraph_findings(
    relative_path: str,
    text: str,
) -> list[str]:
    if relative_path not in COUPLER_PUBLIC_PATHS:
        return []

    findings: list[str] = []
    for line_number, paragraph in normalized_markdown_paragraphs(text):
        for copy_pattern in COUPLER_PARAGRAPH_PATTERNS:
            if copy_pattern.pattern.search(paragraph):
                findings.append(
                    f"{relative_path}:{line_number}: "
                    f"{copy_pattern.name}: {paragraph}"
                )
                break

        for requirement in COUPLER_PARAGRAPH_REQUIREMENTS:
            if not requirement.applies_to(relative_path):
                continue
            if not requirement.trigger_pattern.search(paragraph):
                continue
            if requirement.required_pattern.search(paragraph):
                continue

            findings.append(
                f"{relative_path}:{line_number}: "
                f"{requirement.name}: {paragraph}"
            )
            break

    return findings


def collect_public_copy_findings(docs_dir: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(docs_dir.rglob("*.md")):
        relative_path = path.relative_to(docs_dir).as_posix()
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
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

        findings.extend(collect_coupler_paragraph_findings(relative_path, text))

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
