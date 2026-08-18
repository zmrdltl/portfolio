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


@dataclass(frozen=True)
class PublicParagraphRequirement:
    name: str
    required_patterns: tuple[re.Pattern[str], ...]
    forbidden_patterns: tuple[re.Pattern[str], ...] = ()


@dataclass(frozen=True)
class PublicHeadingRequirement:
    name: str
    trigger_pattern: re.Pattern[str]


@dataclass(frozen=True)
class PublicUnsupportedOutcomeRule:
    name: str
    claim_patterns: tuple[re.Pattern[str], ...]

    def matches(self, paragraph: str) -> bool:
        return any(
            pattern.search(paragraph)
            for pattern in self.claim_patterns
        )


@dataclass(frozen=True)
class PublicSectionOutcomePolicy:
    container_heading_pattern: re.Pattern[str]
    container_heading_level: int
    heading_pattern: re.Pattern[str]
    heading_level: int
    content_pattern: re.Pattern[str]
    unsupported_outcomes: tuple[PublicUnsupportedOutcomeRule, ...]


PUBLIC_HEADING_EXEMPTIONS = (
    re.compile(r"리뷰·멘토링·수상", re.IGNORECASE),
    re.compile(r"Review,\s+Mentoring,\s+and\s+Awards", re.IGNORECASE),
)

NON_ASCII_DASH_PATTERN = re.compile(r"[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]")
OSSCA_MENTOR_PATHS = {"opensource/gluesql.md", "opensource/gluesql.en.md"}
OSSCA_MENTOR_PATTERN = re.compile(r"OSSCA\s*(?:멘토|mentor)", re.IGNORECASE)
OSSCA_HISTORICAL_MENTOR_PATTERN = re.compile(
    r"2023년(?:에는|에)[^.\n]{0,80}OSSCA\s*멘토|"
    r"OSSCA\s*멘토[^.\n]{0,80}2023년(?:에는|에)|"
    r"\b(?:in|during)\s+2023\b[^.\n]{0,80}OSSCA\s+mentor|"
    r"OSSCA\s+mentor[^.\n]{0,80}\b(?:in|during)\s+2023\b",
    re.IGNORECASE,
)
SENTENCE_BOUNDARY_PATTERN = re.compile(r"(?<=[.!?])(?:\s+|$)")

PUBLIC_HEADING_COMPOSITE_ARTIFACTS = (
    re.compile(
        r"\b(?:Data\s+Contract|Design\s+System|"
        r"(?:Data|System)\s+Architecture)\b",
        re.IGNORECASE,
    ),
)

PUBLIC_HEADING_RAW_HTML_TAGS = (
    "blockquote",
    "details",
    "div",
    "pre",
    "script",
    "section",
    "style",
    "table",
    "textarea",
)

PUBLIC_HEADING_WEAK_SUBJECTS = {
    "abstract",
    "additional",
    "architecture",
    "baseline",
    "basic",
    "better",
    "common",
    "concept",
    "data",
    "detail",
    "effective",
    "executable",
    "failure",
    "general",
    "generic",
    "improved",
    "efficiency",
    "mode",
    "new",
    "operational",
    "operation",
    "overview",
    "ownership",
    "performance",
    "quality",
    "rapid",
    "result",
    "revised",
    "responsibility",
    "role",
    "specific",
    "stability",
    "statement",
    "strategy",
    "structure",
    "summary",
    "system",
    "testing",
    "valid",
    "approach",
    "개념",
    "개요",
    "경우",
    "구조",
    "기본",
    "기준선",
    "데이터",
    "결과",
    "모드",
    "방식",
    "범위",
    "성능",
    "상세",
    "세부",
    "실패",
    "실행",
    "안정성",
    "역할",
    "운영",
    "유효",
    "일반",
    "접근",
    "전략",
    "책임",
    "테스트",
    "추가",
    "품질",
    "요약",
    "시험",
    "효율",
}

PUBLIC_HEADING_FILLER_WORDS = {
    "a",
    "an",
    "and",
    "based",
    "external",
    "for",
    "from",
    "in",
    "into",
    "moving",
    "of",
    "on",
    "the",
    "to",
    "using",
    "via",
    "with",
    "without",
    "가능한",
    "기반",
    "대한",
    "외부",
    "위한",
}

PUBLIC_HEADING_REQUIREMENTS = (
    PublicHeadingRequirement(
        "abstract boundary heading without a concrete subject",
        re.compile(
            r"경계|\bboundar(?:y|ies)\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "abstract contract heading without a concrete subject",
        re.compile(r"계약|\bcontracts?\b", re.IGNORECASE),
    ),
    PublicHeadingRequirement(
        "migration heading without a concrete subject",
        re.compile(
            r"이관|전환|마이그레이션|"
            r"\bmigrat(?:e|es|ed|ing|ion|ions)\b|"
            r"\btransition(?:s|ed|ing)?\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "review heading without the reviewed artifact",
        re.compile(
            r"검토|리뷰|\breview(?:s|ed|ing)?\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "configuration heading without the configured subject",
        re.compile(
            r"설정|\bconfigur(?:e|es|ed|ing|ation|ations)\b|"
            r"\bsettings?\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "design heading without the designed artifact",
        re.compile(r"설계|\bdesign(?:s|ed|ing)?\b", re.IGNORECASE),
    ),
    PublicHeadingRequirement(
        "cleanup or formatting heading without the affected artifact",
        re.compile(
            r"정리|\bclean(?:up|ups|ed|ing)\b|"
            r"\bformat(?:s|ted|ting)?\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "improvement heading without the improved artifact",
        re.compile(
            r"개선(?:된|한|하기)?|강화(?:된|한|하기)?|"
            r"고도화(?:된|한|하기)?|향상(?:된|한|하기)?|"
            r"\bimprov(?:e|es|ed|ing|ement|ements)\b|"
            r"\benhanc(?:e|es|ed|ing|ement|ements)\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "optimization heading without the optimized artifact",
        re.compile(
            r"최적화(?:된|한|하기)?|"
            r"\boptimiz(?:e|es|ed|ing|ation|ations)\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "verification heading without the verified artifact",
        re.compile(
            r"검증|확인|\bverif(?:y|ies|ied|ying|ication|ications)\b|"
            r"\bvalidat(?:e|es|ed|ing|ion|ions)\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "synchronization heading without the synchronized artifact",
        re.compile(
            r"동기화|"
            r"\bsynchroniz(?:e|es|ed|ing|ation|ations)\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "implementation heading without the implemented artifact",
        re.compile(
            r"구현|"
            r"\bimplement(?:s|ed|ing|ation|ations)?\b",
            re.IGNORECASE,
        ),
    ),
    PublicHeadingRequirement(
        "testing heading without the tested artifact",
        re.compile(
            r"테스트|시험|\btests?\b|\btesting\b",
            re.IGNORECASE,
        ),
    ),
)


COUPLER_PUBLIC_PATHS = (
    "index.md",
    "index.en.md",
    "projects/coupler.md",
    "projects/coupler.en.md",
)

TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS = (
    "experience/tmaxcloud.md",
    "experience/tmaxcloud.en.md",
)

TMAXCLOUD_ENTITY_EXPORT_IMPORT_HEADINGS = {
    "experience/tmaxcloud.md": re.compile(
        r"(?=.*엔티티)"
        r"(?=.*내보내기(?:·|\s*(?:와|및)\s*)가져오기)"
        r"(?=.*(?:선택\s+속성|데이터\s+변경|동기화)).+"
    ),
    "experience/tmaxcloud.en.md": re.compile(
        r"(?=.*Entity\s+Export(?:/|\s+and\s+)Import)"
        r"(?=.*(?:Selected[- ]Attribute|Data|Change))"
        r"(?=.*Synchronization).+",
        re.IGNORECASE,
    ),
}

TMAXCLOUD_ENTITY_EXPORT_IMPORT_OVERVIEW_HEADINGS = {
    "experience/tmaxcloud.md": re.compile(r"개요"),
    "experience/tmaxcloud.en.md": re.compile(r"Overview", re.IGNORECASE),
}

TMAXCLOUD_ENTITY_EXPORT_IMPORT_OVERVIEW_REQUIREMENTS = {
    "experience/tmaxcloud.md": PublicParagraphRequirement(
        "overview loses entity export/import flow or contribution boundaries",
        (
            re.compile(r"(?:Studio|제품\s+UI)", re.IGNORECASE),
            re.compile(
                r"엔티티\s+내보내기(?:·|\s*(?:와|및)\s*)가져오기",
                re.IGNORECASE,
            ),
            re.compile(r"엔티티를\s+내보내", re.IGNORECASE),
            re.compile(
                r"(?:다른|두\s+번째)\s+(?:생성\s+)?앱으로\s+"
                r"가져(?:오|와)",
                re.IGNORECASE,
            ),
            re.compile(
                r"(?:가져온|가져와)\s+엔티티를?\s+서비스\s+정의에\s+사용|"
                r"가져와\s+서비스\s+정의에\s+사용",
                re.IGNORECASE,
            ),
            re.compile(r"선택\s+속성\s+데이터", re.IGNORECASE),
            re.compile(r"복사", re.IGNORECASE),
            re.compile(r"(?:이후|후속)", re.IGNORECASE),
            re.compile(r"(?:해당\s+)?속성의\s+변경", re.IGNORECASE),
            re.compile(r"동기화", re.IGNORECASE),
            re.compile(r"메시지\s+브로커", re.IGNORECASE),
            re.compile(
                r"(?:^|[.!?]\s+)"
                r"(?:(?:저는|제가|본인은)\s+)?"
                r"(?:(?:내보낸·가져온\s+엔티티|"
                r"내보낸\s+엔티티와\s+가져온\s+엔티티)"
                r"\s+정보를\s+저장하는\s+)?"
                r"DB\s+스키마[^.\n]{0,100}API\s+개발에\s+"
                r"참여(?:하고|했으며|했습니다)",
                re.IGNORECASE,
            ),
            re.compile(r"선택\s+속성\s+메타데이터", re.IGNORECASE),
            re.compile(
                r"메시지\s+브로커[^.\n]{0,160}"
                r"(?:내보내기·가져오기\s+)?엔티티\s+연결\s+구조를\s+"
                r"설계(?:하고|했으며|했습니다)",
                re.IGNORECASE,
            ),
            re.compile(
                r"내보내기\s+화면을\s+구현(?:했으며|했습니다)",
                re.IGNORECASE,
            ),
        ),
        (
            re.compile(
                r"(?:선택\s+속성[^.\n]{0,120})?"
                r"(?:데이터\s+복사[^.\n]{0,100}변경\s+동기화|"
                r"변경\s+동기화)(?:를|을)\s*(?:직접\s+)?"
                r"(?:구현|개발|구축|담당)",
                re.IGNORECASE,
            ),
            re.compile(
                r"(?:팀|팀원|동료|담당\s+엔지니어|프로젝트\s+구성원|"
                r"구성원|개발\s+담당자|다른\s+엔지니어|다른\s+개발자)"
                r"(?:이|가)",
                re.IGNORECASE,
            ),
        ),
    ),
    "experience/tmaxcloud.en.md": PublicParagraphRequirement(
        "overview loses entity export/import flow or contribution boundaries",
        (
            re.compile(r"(?:Studio|product\s+UI)", re.IGNORECASE),
            re.compile(
                r"entity\s+export(?:/|\s+and\s+)import",
                re.IGNORECASE,
            ),
            re.compile(r"export\s+an?\s+entit", re.IGNORECASE),
            re.compile(
                r"import\s+it\s+into\s+(?:another|a\s+second)"
                r"\s+(?:generated\s+)?app(?:lication)?",
                re.IGNORECASE,
            ),
            re.compile(
                r"imported\s+entit(?:y|ies)\s+in\s+service\s+definitions",
                re.IGNORECASE,
            ),
            re.compile(r"selected[- ]attribute\s+data", re.IGNORECASE),
            re.compile(r"(?:at\s+import\s+time|initial(?:ly)?)", re.IGNORECASE),
            re.compile(r"cop(?:y|ied|ies|ying)", re.IGNORECASE),
            re.compile(
                r"synchroniz[^.]{0,100}(?:later|subsequent)\s+changes",
                re.IGNORECASE,
            ),
            re.compile(r"message\s+broker", re.IGNORECASE),
            re.compile(
                r"(?:"
                r"I\s+contributed[^.]{0,120}DB\s+schema[^.]{0,50}API"
                r"[^.]{0,120}designed\s+selected[- ]attribute\s+metadata"
                r"[^.]{0,160}(?:message-broker|broker)-mediated\s+linkage"
                r"[^.]{0,120}exported\s+and\s+imported\s+entities"
                r"[^.]{0,120}and\s+implemented\s+the\s+export\s+UI"
                r"|"
                r"(?=.*I\s+contributed[^.]{0,120}DB\s+schema[^.]{0,50}API)"
                r"(?=.*I\s+designed\s+selected[- ]attribute\s+metadata"
                r"[^.]{0,160}(?:message-broker|broker)-mediated\s+linkage"
                r"[^.]{0,120}exported\s+and\s+imported\s+entities)"
                r"(?=.*I\s+implemented\s+the\s+export\s+UI).+"
                r")",
                re.IGNORECASE,
            ),
        ),
        (
            re.compile(
                r"I\s+(?:directly\s+)?"
                r"(?:implemented|built|developed|owned)[^.]{0,180}"
                r"(?:entity\s+export(?:/|\s+and\s+)import|"
                r"selected[- ]attribute[^.]{0,80}(?:copy|synchroniz)|"
                r"synchronization\s+of\s+(?:later|subsequent)\s+changes)",
                re.IGNORECASE,
            ),
        ),
    ),
}

TMAXCLOUD_ENTITY_EXPORT_IMPORT_REQUIREMENTS = {
    "experience/tmaxcloud.md": (
        PublicParagraphRequirement(
            "missing entity export/import service-definition and synchronization flow",
            (
                re.compile(r"(?:Studio|제품\s+UI)", re.IGNORECASE),
                re.compile(r"엔티티를\s+내보내", re.IGNORECASE),
                re.compile(
                    r"(?:다른|두\s+번째)\s+(?:생성\s+)?앱으로\s+가져오",
                    re.IGNORECASE,
                ),
                re.compile(
                    r"가져온\s+엔티티를\s+서비스\s+정의에\s+사용",
                    re.IGNORECASE,
                ),
                re.compile(r"선택(?:한)?\s+속성", re.IGNORECASE),
                re.compile(r"(?:데이터\s+)?변경", re.IGNORECASE),
                re.compile(r"동기화", re.IGNORECASE),
                re.compile(r"메시지\s+브로커", re.IGNORECASE),
            ),
        ),
        PublicParagraphRequirement(
            "missing direct contribution relationships",
            (
                re.compile(
                    r"(?:^|[.!?]\s+)"
                    r"(?:(?:저는|제가|본인은)\s+)?"
                    r"(?:(?:내보낸·가져온\s+엔티티|"
                    r"내보낸\s+엔티티와\s+가져온\s+엔티티)"
                    r"\s+정보를\s+저장하는\s+)?"
                    r"DB\s+스키마[^.\n]{0,100}API\s+개발에\s+"
                    r"참여(?:하고|했으며|했습니다)",
                    re.IGNORECASE,
                ),
                re.compile(r"선택\s+속성\s+메타데이터", re.IGNORECASE),
                re.compile(r"메시지\s+브로커", re.IGNORECASE),
                re.compile(
                    r"(?:내보내기·가져오기\s+)?엔티티\s+연결\s+구조를\s+"
                    r"설계(?:하고|했으며|했습니다)",
                    re.IGNORECASE,
                ),
                re.compile(
                    r"내보내기\s+화면을\s+구현(?:했으며|했습니다)",
                    re.IGNORECASE,
                ),
            ),
            (
                re.compile(
                    r"(?:팀|팀원|동료|담당\s+엔지니어|프로젝트\s+구성원|"
                    r"구성원|개발\s+담당자|다른\s+엔지니어|다른\s+개발자)"
                    r"(?:이|가)",
                    re.IGNORECASE,
                ),
                re.compile(r"(?:참여|설계|구현)하지\s+않", re.IGNORECASE),
            ),
        ),
        PublicParagraphRequirement(
            "missing synchronization and migration exclusions",
            (
                re.compile(r"메시지\s+동기화\s+서비스", re.IGNORECASE),
                re.compile(
                    r"메시지\s+동기화\s+서비스(?:\s+자체)?\s+구현"
                    r"[^.]{0,100}"
                    r"(?:맡지|담당하지|제외|별도|포함되지)",
                    re.IGNORECASE,
                ),
                re.compile(r"재배포\s+마이그레이션\s+전략", re.IGNORECASE),
                re.compile(
                    r"마이그레이션\s+전략[^.]{0,100}"
                    r"(?:맡지|담당하지|제외|별도|포함되지)",
                    re.IGNORECASE,
                ),
            ),
        ),
    ),
    "experience/tmaxcloud.en.md": (
        PublicParagraphRequirement(
            "missing entity export/import service-definition and synchronization flow",
            (
                re.compile(r"(?:Studio|product\s+UI)", re.IGNORECASE),
                re.compile(r"export\s+an?\s+entit", re.IGNORECASE),
                re.compile(
                    r"import\s+it\s+into\s+(?:another|a\s+second)"
                    r"\s+(?:generated\s+)?app(?:lication)?",
                    re.IGNORECASE,
                ),
                re.compile(
                    r"imported\s+entit(?:y|ies)\s+in\s+service\s+definitions",
                    re.IGNORECASE,
                ),
                re.compile(r"selected\s+attributes?", re.IGNORECASE),
                re.compile(r"chang", re.IGNORECASE),
                re.compile(r"synchroniz", re.IGNORECASE),
                re.compile(r"message\s+broker", re.IGNORECASE),
            ),
        ),
        PublicParagraphRequirement(
            "missing direct contribution relationships",
            (
                re.compile(
                    r"(?:"
                    r"I\s+contributed[^.]{0,120}DB\s+schema[^.]{0,50}API"
                    r"[^.]{0,120}designed\s+selected[- ]attribute\s+metadata"
                    r"[^.]{0,160}(?:message-broker|broker)-mediated\s+linkage"
                    r"[^.]{0,120}exported\s+and\s+imported\s+entities"
                    r"[^.]{0,120}and\s+implemented\s+the\s+export\s+UI"
                    r"|"
                    r"(?=.*I\s+contributed[^.]{0,120}DB\s+schema[^.]{0,50}API)"
                    r"(?=.*I\s+designed\s+selected[- ]attribute\s+metadata"
                    r"[^.]{0,160}(?:message-broker|broker)-mediated\s+linkage"
                    r"[^.]{0,120}exported\s+and\s+imported\s+entities)"
                    r"(?=.*I\s+implemented\s+the\s+export\s+UI).+"
                    r")",
                    re.IGNORECASE,
                ),
            ),
        ),
        PublicParagraphRequirement(
            "missing synchronization and migration exclusions",
            (
                re.compile(
                    r"(?:"
                    r"I\s+did\s+not\s+(?:implement|build|develop|own)"
                    r"[^.]{0,100}message-synchronization\s+service|"
                    r"message-synchronization\s+service[^.]{0,180}"
                    r"separate\s+(?:areas?|work)"
                    r")",
                    re.IGNORECASE,
                ),
                re.compile(
                    r"(?:"
                    r"I\s+did\s+not[^.]{0,220}"
                    r"redeployment\s+migration\s+strategy|"
                    r"redeployment\s+migration\s+strategy[^.]{0,180}"
                    r"separate\s+(?:areas?|work)"
                    r")",
                    re.IGNORECASE,
                ),
            ),
        ),
    ),
}

TMAXCLOUD_ENTITY_EXPORT_IMPORT_FORBIDDEN_PATTERNS = (
    PublicCopyPattern(
        "entity export/import reduced to initial-copy-only wording",
        re.compile(
            r"초기\s+데이터\s+복사(?:만|까지만)|"
            r"초기\s+복사(?:만|까지만)|"
            r"initial\s+(?:data\s+)?copying\s+only",
            re.IGNORECASE,
        ),
        paths=TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS,
    ),
    PublicCopyPattern(
        "entity export/import expanded to application-wide synchronization",
        re.compile(
            r"앱\s+전체\s+데이터|모든\s+앱\s+데이터|"
            r"전체\s+엔티티|모든\s+필드|"
            r"application-wide\s+data|all\s+application\s+data|"
            r"entire\s+entit(?:y|ies)|all\s+fields|full\s+application\s+state",
            re.IGNORECASE,
        ),
        paths=TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS,
    ),
    PublicCopyPattern(
        "message-synchronization service implementation overclaim",
        re.compile(
            r"메시지\s+동기화\s+서비스를\s+(?:직접\s+)?"
            r"(?:구현|개발|구축|담당)(?:했|했습니다)|"
            r"I\s+(?:directly\s+)?(?:implemented|built|developed|owned)"
            r"\s+the\s+message-synchronization\s+service",
            re.IGNORECASE,
        ),
        paths=TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS,
    ),
    PublicCopyPattern(
        "entity export/import copy or synchronization overclaim",
        re.compile(
            r"(?:선택\s+속성[^.\n]{0,120})?"
            r"(?:데이터\s+복사[^.\n]{0,100}변경\s+동기화|"
            r"변경\s+동기화)(?:를|을)\s*(?:직접\s+)?"
            r"(?:구현|개발|구축|담당)|"
            r"I\s+(?:directly\s+)?(?:implemented|built|developed|owned)"
            r"[^.]{0,180}(?:selected[- ]attribute[^.]{0,100}"
            r"(?:copy|synchroniz)|synchronization\s+of\s+"
            r"(?:later|subsequent)\s+changes)",
            re.IGNORECASE,
        ),
        paths=TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS,
    ),
    PublicCopyPattern(
        "redeployment migration-strategy overclaim",
        re.compile(
            r"재배포[^.\n]{0,80}마이그레이션\s+전략을\s+"
            r"(?:설계|구현|완성)(?:했|했습니다)|"
            r"I\s+(?:designed|implemented|completed|owned)"
            r"[^.\n]{0,100}redeployment\s+migration\s+strategy",
            re.IGNORECASE,
        ),
        paths=TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS,
    ),
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
            r"(?=.*(?:"
            r"최초\s+가입\s+심사[^.\n]{0,30}(?:도달|기록)|"
            r"(?:recorded|event\s+count)\s+upon\s+reaching\s+the\s+"
            r"(?:first|initial)\s+signup\s+review"
            r"))"
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
            r"Observed Meta SDK event count upon reaching the initial "
            r"signup review stage:\s*about 10 before the redesign and "
            r"about 100 after\."
            r")$",
            re.IGNORECASE,
        ),
        paths=("projects/coupler.md", "projects/coupler.en.md"),
    ),
)

COUPLER_TYPESCRIPT_CONTENT_PATTERN = re.compile(
    r"\b(?:TypeScript|TSX|JavaScript|JSX|typecheck)\b|allowJs",
    re.IGNORECASE,
)

COUPLER_TYPESCRIPT_UNSUPPORTED_OUTCOMES = (
    PublicUnsupportedOutcomeRule(
        "unsupported Coupler TypeScript error outcome claim",
        (
            re.compile(
                r"(?:"
                r"(?:오류|장애)\s*(?:율|률|수|건수)"
                r"(?:이|가|은|는|을|를)?[^.!?\n]{0,48}"
                r"(?:감소|줄(?:었|였|어들)|낮아|낮췄|개선|"
                r"사라(?:졌|진)|없어(?:졌|진)|제거(?:했|됐|되))|"
                r"(?:오류|장애)(?:가|는|도)[^.!?\n]{0,48}"
                r"(?:감소|줄(?:었|였|어들)|낮아|낮췄|개선|"
                r"사라(?:졌|진)|없어(?:졌|진)|제거(?:했|됐|되))|"
                r"(?:오류|장애)를\s*"
                r"(?:(?:약|대략|크게|많이|현저히|대폭|절반(?:으로)?|"
                r"\d+(?:\.\d+)?%?)\s*){0,4}"
                r"(?:감소|줄(?:였|어들)|낮췄|사라지게|없애|제거)|"
                r"(?:감소한|줄어든|낮아진|개선된|사라진|없어진|제거된)"
                r"\s*(?:런타임\s*)?(?:오류|장애)"
                r"(?:\s*(?:율|률|수|건수))?"
                r")",
                re.IGNORECASE,
            ),
            re.compile(
                r"(?:"
                r"(?:"
                r"\b(?:error|failure)\s+(?:rate|count)\b|"
                r"\b(?:the\s+)?number\s+of\s+"
                r"(?:runtime\s+)?(?:errors?|failures?)\b"
                r")"
                r"(?!\s+(?:handling|processing|calculation|logic|reporting))"
                r"[^.!?\n]{0,40}"
                r"(?:decreas\w*|reduc\w*|drop\w*|declin\w*|\bcut\b|halv\w*|"
                r"\bfell\b|\bfallen\b|\bwent\s+down\b|lower\w*|"
                r"improv\w*|eliminat\w*|(?:near(?:ly)?|almost)\s+zero)|"
                r"\b(?:runtime\s+)?(?:errors?|failures?)\b\s+"
                r"(?:(?:was|were|is|are|has\s+been|have\s+been|had\s+been)\s+)?"
                r"(?:(?:\d+(?:\.\d+)?%|significantly|substantially|"
                r"materially|sharply|greatly)\s+){0,3}"
                r"(?:decreas\w*|reduc\w*|drop\w*|declin\w*|\bcut\b|halv\w*|"
                r"\bfell\b|\bfallen\b|\bwent\s+down\b|lower\w*|"
                r"eliminat\w*|(?:near(?:ly)?|almost)\s+zero)|"
                r"(?:decreas\w*|reduc\w*|lower\w*|eliminat\w*|"
                r"\bcut\b|halv\w*)\s+"
                r"(?:(?:\d+(?:\.\d+)?%|significantly|substantially|"
                r"materially|sharply|greatly)\s+of\s+)?"
                r"(?:the\s+)?(?:"
                r"(?:runtime\s+)?(?:errors?|failures?)|"
                r"(?:error|failure)\s+(?:rate|count)|"
                r"number\s+of\s+(?:runtime\s+)?(?:errors?|failures?)"
                r")(?!\s+(?:handling|processing|calculation|logic|reporting))|"
                r"improv\w*\s+(?:the\s+)?"
                r"(?:error|failure)\s+(?:rate|count)\b"
                r"(?!\s+(?:handling|processing|calculation|logic|reporting))|"
                r"\bfewer\s+(?:runtime\s+)?(?:errors?|failures?)\b"
                r")",
                re.IGNORECASE,
            ),
        ),
    ),
    PublicUnsupportedOutcomeRule(
        "unsupported Coupler TypeScript response-performance outcome claim",
        (
            re.compile(
                r"(?:"
                r"(?:응답\s*(?:속도|시간|지연)|지연\s*시간)"
                r"(?:이|가|은|는|도)[^.!?\n]{0,48}"
                r"(?:감소|줄(?:었|어들)|낮아|개선|단축|빨라|짧아)|"
                r"(?:응답\s*(?:속도|시간|지연)|지연\s*시간)"
                r"(?:을|를)\s*"
                r"(?:(?:약|대략|크게|많이|현저히|대폭|절반(?:으로)?|"
                r"\d+(?:\.\d+)?%?)\s*){0,4}"
                r"(?:감소|줄(?:였|어들)|낮췄|단축|빠르게|짧게)|"
                r"응답(?:을|를)\s*"
                r"(?:(?:약|대략|크게|많이|현저히|대폭|더|"
                r"\d+(?:\.\d+)?%?)\s*){0,4}"
                r"(?:빠르게|빨리)\s*(?:했|만들)|"
                r"응답(?:이|가|은|는|도)[^.!?\n]{0,32}(?:빨라|빠르게)|"
                r"(?:감소한|줄어든|낮아진|개선된|단축된|빨라진|짧아진)"
                r"\s*(?:응답\s*(?:속도|시간|지연)|지연\s*시간)"
                r"(?!\s*(?:처리|계산|파싱|로직))|"
                r"(?:빨라진|빠른)\s*응답(?!\s*(?:처리|계산|파싱|로직))"
                r")",
                re.IGNORECASE,
            ),
            re.compile(
                r"(?:"
                r"\b(?:response\s+(?:speed|times?|latency)|latency)\b\s+"
                r"(?:(?:was|were|is|are|has\s+been|have\s+been|had\s+been|"
                r"became|become)\s+)?"
                r"(?:(?:\d+(?:\.\d+)?%|significantly|substantially|"
                r"materially|sharply)\s+){0,3}"
                r"(?:decreas\w*|reduc\w*|drop\w*|declin\w*|\bcut\b|halv\w*|"
                r"\bfell\b|\bfallen\b|\bwent\s+down\b|lower\w*|"
                r"improv\w*|\bfaster\b|\bshorter\b|"
                r"(?:near(?:ly)?|almost)\s+zero)|"
                r"(?:decreas\w*|reduc\w*|lower\w*|improv\w*|"
                r"\bcut\b|halv\w*)\s+"
                r"(?:the\s+)?(?:response\s+(?:speed|times?|latency)|latency)\b"
                r"(?!\s+(?:handling|processing|calculation|parsing|logic))|"
                r"(?:\d+(?:\.\d+)?%\s+)?(?:faster|shorter|lower)\s+"
                r"(?:response\s+(?:speed|times?|latency)|latency)\b"
                r"(?!\s+(?:handling|processing|calculation|parsing|logic))|"
                r"\b(?:API\s+)?responses?\b\s+"
                r"(?:(?:was|were|is|are|has\s+been|have\s+been|had\s+been|"
                r"became|become)\s+)?"
                r"(?:(?:\d+(?:\.\d+)?%|significantly|substantially|"
                r"materially|noticeably)\s+)?"
                r"(?:faster|quicker)\b|"
                r"\b(?:faster|quicker)\s+(?:API\s+)?responses?\b"
                r")",
                re.IGNORECASE,
            ),
        ),
    ),
)

COUPLER_TYPESCRIPT_SECTION_POLICIES = {
    "projects/coupler.md": PublicSectionOutcomePolicy(
        re.compile(r"추가 작업", re.IGNORECASE),
        2,
        re.compile(
            r"관리자 웹을 TypeScript로 전환하고 "
            r"JavaScript 재유입을 CI로 차단",
            re.IGNORECASE,
        ),
        3,
        COUPLER_TYPESCRIPT_CONTENT_PATTERN,
        COUPLER_TYPESCRIPT_UNSUPPORTED_OUTCOMES,
    ),
    "projects/coupler.en.md": PublicSectionOutcomePolicy(
        re.compile(r"Additional Work", re.IGNORECASE),
        2,
        re.compile(
            r"Migrating the Admin Web to TypeScript and Preventing "
            r"JavaScript Reintroduction in CI",
            re.IGNORECASE,
        ),
        3,
        COUPLER_TYPESCRIPT_CONTENT_PATTERN,
        COUPLER_TYPESCRIPT_UNSUPPORTED_OUTCOMES,
    ),
}


PUBLIC_COPY_PATTERNS = [
    PublicCopyPattern(
        "unnatural GlueSQL duplicate-state wording",
        re.compile(
            r"Duplication\s+is\s+defined\s+against\s+different\s+state\s+"
            r"in\s+projection\s+and\s+aggregate\s+execution",
            re.IGNORECASE,
        ),
        paths=("opensource/gluesql.en.md",),
    ),
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
        "generic Coupler home label",
        re.compile(
            r"Coupler\s*·\s*모바일\s+앱\s+개발총괄|"
            r"Coupler\s*·\s*Mobile\s+App\s+Engineering\s+Lead",
            re.IGNORECASE,
        ),
        paths=("index.md", "index.en.md"),
    ),
    PublicCopyPattern(
        "ambiguous Coupler state-contract wording",
        re.compile(
            r"\bserver-(?:owned|driven)\s+(?:review-)?state\s+contract\b|"
            r"서버\s+응답\s+기반\s+심사\s+상태\s+계약",
            re.IGNORECASE,
        ),
        paths=(
            "index.md",
            "index.en.md",
            "projects/coupler.md",
            "projects/coupler.en.md",
        ),
    ),
    PublicCopyPattern(
        "ambiguous Coupler outsourced-maintenance wording",
        re.compile(r"\binitially\s+outsourced\s+maintenance\b", re.IGNORECASE),
        paths=("projects/coupler.en.md",),
    ),
    PublicCopyPattern(
        "Coupler review-scope terminology drift",
        re.compile(r"\bprofile-edit\s+reviews?\b", re.IGNORECASE),
        paths=("projects/coupler.en.md",),
    ),
    PublicCopyPattern(
        "engineering-principle semantic inversion",
        re.compile(
            r"\bI\s+fix\s+core\s+behavior[^.\n]{0,120}\bin\s+tests\b",
            re.IGNORECASE,
        ),
        paths=("engineering-principles.en.md",),
    ),
    PublicCopyPattern(
        "abstract engineering-principle wording",
        re.compile(
            r"현상을\s+실패\s+모드와\s+책임\s+경계로\s+나눕니다|"
            r"완료\s+조건을\s+실행\s+가능한\s+계약으로\s+만듭니다|"
            r"이관은\s+기준선[·,\s]+전환[·,\s]+정리로\s+나눕니다|"
            r"Separate\s+Symptoms\s+into\s+Failure\s+Modes\s+and\s+"
            r"Ownership\s+Boundaries|"
            r"Turn\s+Completion\s+Criteria\s+into\s+Executable\s+Contracts|"
            r"Split\s+Migrations\s+into\s+Baseline,\s+Transition,\s+and\s+Cleanup|"
            r"Separate\s+Symptoms\s+from\s+Causes\s+and\s+Define\s+the\s+Change|"
            r"\bwait\s+policies\b|\boutside\s+the\s+task\b",
            re.IGNORECASE,
        ),
        paths=("engineering-principles.md", "engineering-principles.en.md"),
    ),
    PublicCopyPattern(
        "abstract Coupler responsibility-boundary heading",
        re.compile(
            r"^\s*#{1,6}\s+(?:"
            r"App\s*/\s*API\s*/\s*Admin\s+책임\s+경계|"
            r"App\s*/\s*API\s*/\s*Admin\s+Responsibility\s+Boundaries"
            r")\s*$",
            re.IGNORECASE,
        ),
        paths=("projects/coupler.md", "projects/coupler.en.md"),
    ),
    PublicCopyPattern(
        "vague ClumL operational-setting wording",
        re.compile(
            r"반복\s+운영\s+설정\s+외부화|"
            r"externalized\s+an\s+operational\s+setting",
            re.IGNORECASE,
        ),
        paths=("index.md", "index.en.md", "experience/cluml.md", "experience/cluml.en.md"),
    ),
    PublicCopyPattern(
        "vague ClumL detection-threshold wording",
        re.compile(
            r"탐지\s+판정값|"
            r"Rust\s+요청\s+제한·운영\s+설정|"
            r"탐지\s+화면·리포트\s+검토|"
            r"Detection\s+Screen\s+and\s+Report\s+Review|"
            r"network-event\s+detection-threshold\s+configuration",
            re.IGNORECASE,
        ),
        paths=(
            "index.md",
            "index.en.md",
            "experience/cluml.md",
            "experience/cluml.en.md",
        ),
    ),
    PublicCopyPattern(
        "ambiguous Coupler routing or review-stage wording",
        re.compile(
            r"aligned\s+app/admin\s+routing\s+to\s+server\s+review\s+state|"
            r"recorded\s+upon\s+reaching\s+the\s+first\s+signup\s+review\s*:",
            re.IGNORECASE,
        ),
        paths=("index.en.md", "projects/coupler.en.md"),
    ),
    PublicCopyPattern(
        "vague GlueSQL storage-path wording",
        re.compile(r"스토리지\s+경로|storage\s+paths?", re.IGNORECASE),
        paths=("opensource/gluesql.md", "opensource/gluesql.en.md"),
    ),
    PublicCopyPattern(
        "overbroad ClumL time-conversion module wording",
        re.compile(
            r"시간\s+변환\s+모듈|time[- ]conversion\s+module",
            re.IGNORECASE,
        ),
        paths=("experience/cluml.md", "experience/cluml.en.md"),
    ),
    PublicCopyPattern(
        "vague TmaxCloud exception-output heading",
        re.compile(
            r"^\s*#{1,6}\s+(예외\s+출력\s+정리|Exception\s+Output\s+Formatting)\s*$",
            re.IGNORECASE,
        ),
        paths=("experience/tmaxcloud.md", "experience/tmaxcloud.en.md"),
    ),
    PublicCopyPattern(
        "context-free TmaxCloud test-component wording",
        re.compile(
            r"WebSocket(?:\s+기반)?\s+E2E\s*(?:페이지|page)|"
            r"^\s*#{1,6}\s+(?:API\s+통합\s+테스트\s+환경(?:\s+구현)?|"
            r"API\s+Integration\s+Test\s+Environment)\s*$",
            re.IGNORECASE,
        ),
        paths=(
            "index.md",
            "index.en.md",
            "experience/tmaxcloud.md",
            "experience/tmaxcloud.en.md",
        ),
    ),
    PublicCopyPattern(
        "unverified TmaxCloud cycle-reduction metric",
        re.compile(
            r"4주(?:에서|에서\s+약)?\s*2주|"
            r"four\s+weeks[^.\n]{0,80}(?:about\s+)?two",
            re.IGNORECASE,
        ),
        paths=(
            "index.md",
            "index.en.md",
            "experience/tmaxcloud.md",
            "experience/tmaxcloud.en.md",
        ),
    ),
    PublicCopyPattern(
        "internal TmaxCloud exception-logger identifier",
        re.compile(r"\bErrorLogger\b", re.IGNORECASE),
        paths=("experience/tmaxcloud.md", "experience/tmaxcloud.en.md"),
    ),
    PublicCopyPattern(
        "unsafe GlueSQL award-evidence folder",
        re.compile(
            r"drive\.google\.com/drive/folders/"
            r"1llwXz9RquWtRVH0ZQh2FZOLelAzmuBfO",
            re.IGNORECASE,
        ),
        paths=("opensource/gluesql.md", "opensource/gluesql.en.md"),
    ),
    PublicCopyPattern(
        "unnatural English portfolio wording",
        re.compile(
            r"Fixed\s+over-limit\s+request\s+passing|"
            r"\bthe\s+number\s+passing\b|"
            r"\bduplicate\s+decisions\b|"
            r"opens\s+submission,\s+resubmission,\s+and\s+"
            r"subsequent-review\s+tabs\s+from",
            re.IGNORECASE,
        ),
        paths=(
            "experience/index.en.md",
            "experience/cluml.en.md",
            "opensource/gluesql.en.md",
            "projects/coupler.en.md",
        ),
    ),
    PublicCopyPattern(
        "GlueSQL award split into two awards",
        re.compile(
            r"(?:장려상|최우수상)\s*·\s*정보통신산업진흥원장상|"
            r"(?:Encouragement|Top\s+Excellence)\s+Award\s*·\s*"
            r"NIPA\s+President\s+Award",
            re.IGNORECASE,
        ),
        paths=("opensource/gluesql.md", "opensource/gluesql.en.md"),
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
            r"제가\s*맡은\s*범위|제\s*담당\s*범위|"
            r"직접\s*담당한\s*범위가\s*아닙니다|"
            r"\bdirect\s+scope\b|outside\s+my\s+(?:direct\s+)?scope",
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
            r"/Users/|localhost|\.env|production host|DB endpoint|"
            r"(?<![A-Za-z0-9])[\"'`]?(?:[A-Za-z0-9]+[_-])*"
            r"(?:api[ _-]?(?:key|token)|access[ _-]?(?:key|token)|"
            r"refresh[ _-]?token|auth(?:entication|orization)?[ _-]?token|"
            r"private[ _-]?key|token|password|secret|credentials?)"
            r"(?:[_-][A-Za-z0-9]+)*[\"'`]?"
            r"(?![A-Za-z0-9])\s*(?::|=)\s*"
            r"[\"'`]?[A-Za-z0-9._~+/=-]{4,}|"
            r"(?<![A-Za-z0-9])[\"'`]?Authorization[\"'`]?"
            r"\s*(?::|=)\s*[\"'`]?Bearer\s+[A-Za-z0-9._~+/=-]{8,}",
            re.IGNORECASE,
        ),
    ),
]


PUBLIC_ABBREVIATION_REQUIREMENTS: list[PublicAbbreviationRequirement] = []


PUBLIC_LINE_REQUIREMENTS = [
    PublicLineRequirement(
        "unqualified 2023 GlueSQL team award",
        re.compile(
            r"^\|\s*2023\s*\|[^\n]*(?:장려상|Encouragement)",
            re.IGNORECASE,
        ),
        re.compile(
            r"(?=.*(?:멘토|mentor))(?=.*(?:팀\s+수상|team\s+award))",
            re.IGNORECASE,
        ),
        paths=("opensource/gluesql.md", "opensource/gluesql.en.md"),
    ),
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


def extract_markdown_section(
    text: str,
    heading_pattern: re.Pattern[str],
    heading_level: int | None = None,
) -> tuple[int, str] | None:
    lines = text.splitlines()
    section_start: int | None = None
    section_level: int | None = None

    for index, line in enumerate(lines):
        heading_match = re.match(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", line)
        if heading_match is None:
            continue

        level = len(heading_match.group(1))
        title = heading_match.group(2).strip()
        if section_start is None:
            if heading_pattern.fullmatch(title) and (
                heading_level is None or level == heading_level
            ):
                section_start = index
                section_level = level
            continue

        if section_level is not None and level <= section_level:
            section_lines = lines[section_start:index]
            return section_start + 1, "\n".join(section_lines)

    if section_start is None:
        return None

    return section_start + 1, "\n".join(lines[section_start:])


def paragraph_satisfies_requirement(
    paragraph: str,
    requirement: PublicParagraphRequirement,
) -> bool:
    return all(
        pattern.search(paragraph)
        for pattern in requirement.required_patterns
    ) and not any(
        pattern.search(paragraph)
        for pattern in requirement.forbidden_patterns
    )


def collect_heading_clarity_findings(
    relative_path: str,
    text: str,
) -> list[str]:
    def strip_korean_particle(token: str) -> str:
        for suffix in (
            "으로부터",
            "에서",
            "에게",
            "으로",
            "로",
            "과",
            "와",
            "의",
            "을",
            "를",
            "이",
            "가",
            "은",
            "는",
            "도",
        ):
            if token.endswith(suffix) and len(token) > len(suffix):
                candidate = token[: -len(suffix)]
                if (
                    candidate in PUBLIC_HEADING_WEAK_SUBJECTS
                    or candidate in PUBLIC_HEADING_FILLER_WORDS
                ):
                    return candidate
        return token

    def has_concrete_subject(heading: str) -> bool:
        subject = re.sub(r"\s*\{[^{}\n]*\}\s*$", "", heading)
        subject = re.sub(
            r"!?\[([^\]\n]*)\]\([^)\n]*\)",
            r"\1",
            subject,
        )
        subject = re.sub(
            r"!?\[([^\]\n]*)\]\[[^\]\n]*\]",
            r"\1",
            subject,
        )
        for index, artifact_pattern in enumerate(
            PUBLIC_HEADING_COMPOSITE_ARTIFACTS,
            start=1,
        ):
            subject = artifact_pattern.sub(
                f"ConcreteCompositeArtifact{index}",
                subject,
            )
        for abstract_requirement in PUBLIC_HEADING_REQUIREMENTS:
            subject = abstract_requirement.trigger_pattern.sub(" ", subject)
        tokens = re.findall(r"[A-Za-z][A-Za-z0-9.+#/-]*|[가-힣]+", subject)
        for raw_token in tokens:
            token = strip_korean_particle(raw_token)
            normalized = token.casefold()
            if normalized in PUBLIC_HEADING_FILLER_WORDS:
                continue
            if normalized in PUBLIC_HEADING_WEAK_SUBJECTS:
                continue
            singular_candidates = ()
            if normalized.endswith("ies"):
                singular_candidates += (normalized[:-3] + "y",)
            if normalized.endswith("s"):
                singular_candidates += (normalized[:-1],)
            if any(
                candidate in PUBLIC_HEADING_WEAK_SUBJECTS
                for candidate in singular_candidates
            ):
                continue
            return True
        return False

    lines = text.splitlines()
    fenced_lines: set[int] = set()
    active_fence_character: str | None = None
    active_fence_length = 0
    for line_number, line in enumerate(lines, start=1):
        fence_match = re.match(r"^[ \t]{0,3}(`{3,}|~{3,})(.*)$", line)
        if active_fence_character is None:
            if fence_match is None:
                continue
            marker = fence_match.group(1)
            active_fence_character = marker[0]
            active_fence_length = len(marker)
            fenced_lines.add(line_number)
            continue

        fenced_lines.add(line_number)
        if re.fullmatch(
            rf"[ \t]{{0,3}}{re.escape(active_fence_character)}"
            rf"{{{active_fence_length},}}[ \t]*",
            line,
        ):
            active_fence_character = None
            active_fence_length = 0

    raw_html_lines: set[int] = set()
    active_raw_html_tag: str | None = None
    raw_html_tag_pattern = "|".join(
        re.escape(tag)
        for tag in PUBLIC_HEADING_RAW_HTML_TAGS
    )
    for line_number, line in enumerate(lines, start=1):
        if line_number in fenced_lines:
            continue
        if active_raw_html_tag is None:
            raw_html_match = re.match(
                r"^[ \t]{0,3}<"
                rf"({raw_html_tag_pattern})(?:[ \t>]|$)",
                line,
                re.IGNORECASE,
            )
            if raw_html_match is None:
                continue
            active_raw_html_tag = raw_html_match.group(1)

        raw_html_lines.add(line_number)
        if re.search(
            rf"</{re.escape(active_raw_html_tag)}[ \t]*>",
            line,
            re.IGNORECASE,
        ):
            active_raw_html_tag = None

    visible_lines = lines.copy()
    inside_html_comment = False
    for line_number, line in enumerate(lines, start=1):
        if line_number in fenced_lines or line_number in raw_html_lines:
            continue

        visible_parts: list[str] = []
        position = 0
        while position < len(line):
            if inside_html_comment:
                comment_end = line.find("-->", position)
                if comment_end == -1:
                    position = len(line)
                    continue
                inside_html_comment = False
                position = comment_end + 3
                continue

            comment_start = line.find("<!--", position)
            if comment_start == -1:
                visible_parts.append(line[position:])
                break
            visible_parts.append(line[position:comment_start])
            inside_html_comment = True
            position = comment_start + 4

        visible_lines[line_number - 1] = "".join(visible_parts)

    def strip_container_prefix(line: str) -> str:
        remaining = line
        while True:
            container_match = re.match(
                r"^[ \t]{0,3}(?:>[ \t]?|(?:[-+*]|\d+[.)])[ \t]+)",
                remaining,
            )
            if container_match is None:
                return remaining
            remaining = remaining[container_match.end():]

    displayed_lines = [
        strip_container_prefix(line)
        for line in visible_lines
    ]

    headings: list[tuple[int, str]] = []
    for line_number, line in enumerate(displayed_lines, start=1):
        if line_number in fenced_lines or line_number in raw_html_lines:
            continue
        atx_match = re.match(
            r"^[ \t]{0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$",
            line,
        )
        if atx_match is not None:
            headings.append((line_number, atx_match.group(1).strip()))
            continue
        if (
            line_number >= 2
            and line_number - 1 not in fenced_lines
            and line_number - 1 not in raw_html_lines
            and re.fullmatch(r"[ \t]{0,3}(?:=+|-+)[ \t]*", line)
            and displayed_lines[line_number - 2].strip()
        ):
            headings.append(
                (line_number - 1, displayed_lines[line_number - 2].strip())
            )

    findings: list[str] = []
    for line_number, heading in headings:
        if any(pattern.fullmatch(heading) for pattern in PUBLIC_HEADING_EXEMPTIONS):
            continue

        for requirement in PUBLIC_HEADING_REQUIREMENTS:
            if not requirement.trigger_pattern.search(heading):
                continue
            if has_concrete_subject(heading):
                continue
            findings.append(
                f"{relative_path}:{line_number}: "
                f"{requirement.name}: {heading}"
            )
            break

    return findings


def collect_tmaxcloud_entity_export_import_findings(
    relative_path: str,
    text: str,
) -> list[str]:
    if relative_path not in TMAXCLOUD_ENTITY_EXPORT_IMPORT_PATHS:
        return []

    heading_pattern = TMAXCLOUD_ENTITY_EXPORT_IMPORT_HEADINGS[relative_path]
    section = extract_markdown_section(text, heading_pattern)
    if section is None:
        return [
            f"{relative_path}:1: missing entity export/import synchronization section."
        ]

    line_number, section_text = section
    paragraphs = normalized_markdown_paragraphs(section_text)
    findings: list[str] = []
    for copy_pattern in TMAXCLOUD_ENTITY_EXPORT_IMPORT_FORBIDDEN_PATTERNS:
        if copy_pattern.pattern.search(text):
            findings.append(
                f"{relative_path}:{line_number}: "
                f"{copy_pattern.name}: {section_text}"
            )

    for requirement in TMAXCLOUD_ENTITY_EXPORT_IMPORT_REQUIREMENTS[relative_path]:
        if any(
            paragraph_satisfies_requirement(paragraph, requirement)
            for _, paragraph in paragraphs
        ):
            continue
        findings.append(
            f"{relative_path}:{line_number}: "
            f"{requirement.name}: {section_text}"
        )

    return findings


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


def collect_coupler_typescript_section_findings(
    relative_path: str,
    text: str,
) -> list[str]:
    policy = COUPLER_TYPESCRIPT_SECTION_POLICIES.get(relative_path)
    if policy is None:
        return []

    container = extract_markdown_section(
        text,
        policy.container_heading_pattern,
        policy.container_heading_level,
    )
    if container is None:
        misplaced_container = extract_markdown_section(
            text,
            policy.container_heading_pattern,
        )
        orphaned_section = extract_markdown_section(
            text,
            policy.heading_pattern,
        )
        content_match = policy.content_pattern.search(text)
        if misplaced_container is not None:
            finding_line = misplaced_container[0]
        elif orphaned_section is not None:
            finding_line = orphaned_section[0]
        elif content_match is not None:
            finding_line = text.count("\n", 0, content_match.start()) + 1
        else:
            finding_line = 1
        return [
            f"{relative_path}:{finding_line}: missing or misleveled "
            "Coupler Additional Work container section."
        ]

    container_line, container_text = container
    section = extract_markdown_section(
        container_text,
        policy.heading_pattern,
        policy.heading_level,
    )
    if section is None:
        return [
            f"{relative_path}:{container_line}: missing or misleveled "
            "Coupler TypeScript supporting-work section."
        ]

    nested_section_line, section_text = section
    section_line = container_line + nested_section_line - 1
    section_paragraphs = normalized_markdown_paragraphs(section_text)
    body_paragraphs = [
        (paragraph_line, paragraph)
        for paragraph_line, paragraph in section_paragraphs
        if not re.match(r"^#{1,6}\s", paragraph)
    ]
    findings: list[str] = []
    for paragraph_line, paragraph in body_paragraphs:
        for outcome_rule in policy.unsupported_outcomes:
            if not outcome_rule.matches(paragraph):
                continue
            findings.append(
                f"{relative_path}:{section_line + paragraph_line - 1}: "
                f"{outcome_rule.name}: {paragraph}"
            )
            break

    if findings:
        return findings

    if not any(
        policy.content_pattern.search(paragraph)
        for _, paragraph in body_paragraphs
    ):
        return [
            f"{relative_path}:{section_line}: missing Coupler TypeScript "
            "supporting-work content."
        ]

    return findings


def collect_public_copy_findings(docs_dir: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(docs_dir.rglob("*.md")):
        relative_path = path.relative_to(docs_dir).as_posix()
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if relative_path in OSSCA_MENTOR_PATHS:
                for sentence in SENTENCE_BOUNDARY_PATTERN.split(line):
                    if not OSSCA_MENTOR_PATTERN.search(sentence):
                        continue
                    if OSSCA_HISTORICAL_MENTOR_PATTERN.search(sentence):
                        continue
                    findings.append(
                        f"{relative_path}:{line_number}: "
                        f"undated OSSCA mentor role: {sentence.strip()}"
                    )

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
        findings.extend(
            collect_coupler_typescript_section_findings(relative_path, text)
        )
        findings.extend(
            collect_tmaxcloud_entity_export_import_findings(relative_path, text)
        )
        findings.extend(collect_heading_clarity_findings(relative_path, text))

    findings.extend(collect_abbreviation_findings(docs_dir))
    return findings


def collect_non_ascii_dash_findings(docs_dir: Path) -> list[str]:
    findings: list[str] = []
    visible_text_files = sorted(
        path
        for path in docs_dir.rglob("*")
        if path.suffix in {".md", ".svg"}
    )
    for path in visible_text_files:
        relative_path = path.relative_to(docs_dir).as_posix()
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if NON_ASCII_DASH_PATTERN.search(line):
                findings.append(
                    f"{relative_path}:{line_number}: "
                    f"non-ASCII dash punctuation: {line.strip()}"
                )

    return findings


def validate_public_copy(
    docs_dir: Path,
) -> tuple[list[str], PublicCopySummary]:
    visible_text_files = [
        path
        for path in docs_dir.rglob("*")
        if path.suffix in {".md", ".svg"}
    ]
    findings = collect_public_copy_findings(docs_dir)
    findings.extend(collect_non_ascii_dash_findings(docs_dir))
    return findings, PublicCopySummary(len(visible_text_files), len(findings))


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
