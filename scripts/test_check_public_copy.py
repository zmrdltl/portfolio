from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.check_public_copy import validate_public_copy


class PublicCopyCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self.temp_dir.name) / "docs"
        self.docs_dir.mkdir()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def validate(self) -> list[str]:
        findings, _ = validate_public_copy(self.docs_dir)
        return findings

    def test_clean_public_copy_passes(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\nMeta SDK postback event가 증가한 것을 계측했습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_qualified_coupler_postback_metric_passes(self) -> None:
        (self.docs_dir / "projects.md").write_text(
            "# 프로젝트\n\n"
            "Meta SDK postback event count 기준으로 event가 "
            "약 50건에서 약 1.1k 수준으로 증가했습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_unqualified_coupler_postback_metric_is_rejected(self) -> None:
        (self.docs_dir / "projects.md").write_text(
            "# 프로젝트\n\n"
            "심사 요청 관련 event가 약 50건에서 약 1.1k 수준으로 증가했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "unqualified Coupler Meta SDK postback metric" in finding
                for finding in self.validate()
            )
        )

    def test_stale_coupler_postback_baseline_is_rejected(self) -> None:
        (self.docs_dir / "projects.md").write_text(
            "# 프로젝트\n\n"
            "Meta SDK postback event count 기준으로 event가 "
            "약 40건에서 약 1.1k 수준으로 증가했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "stale Coupler postback baseline" in finding
                for finding in self.validate()
            )
        )

    def test_ambiguous_coupler_operating_label_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n"
            "- [개인 제품 Coupler 운영 기준](projects/coupler.md): "
            "가입 심사 기준을 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "ambiguous Coupler operating-label wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_ambiguous_coupler_operating_label_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").write_text(
            "# Summary\n\n"
            "- [Operating criteria for the personal product Coupler]"
            "(projects/coupler.md): aligned review criteria.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "ambiguous Coupler operating-label wording" in finding
                for finding in self.validate()
            )
        )

    def test_unverified_coupler_conversion_cost_metric_is_rejected(self) -> None:
        (self.docs_dir / "projects.md").write_text(
            "# Coupler\n\n광고단가가 10만원에서 2만5천원으로 낮아졌습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "unverified Coupler conversion-cost metric" in finding
                for finding in self.validate()
            )
        )

    def test_public_hog_product_name_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\nHOG 탐지 period 설정을 외부 config로 분리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("internal HOG product name" in finding for finding in self.validate())
        )

    def test_unqualified_hog_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\nHOG 작업을 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("internal HOG product name" in finding for finding in self.validate())
        )

    def test_opaque_detection_period_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n탐지 period 설정을 외부 config로 분리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque detection-period wording" in finding
                for finding in self.validate()
            )
        )

    def test_verbose_rationale_heading_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n**왜 이 해결 방법인지:** 이 접근을 선택했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("verbose rationale heading" in finding for finding in self.validate())
        )

    def test_opaque_cau_rationale_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n"
            "write 시점의 snapshot copy와 read 시점의 select SQL 기준이 "
            "같은 metadata/generation boundary 안에 있어야 했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("opaque CAU rationale wording" in finding for finding in self.validate())
        )

    def test_resolution_as_closing_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n회귀 테스트 기준으로 닫았습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "resolution-as-closing wording" in finding
                for finding in self.validate()
            )
        )

    def test_opaque_generated_platform_jargon_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n"
            "generated service와 row snapshot copy를 같은 generation boundary로 "
            "관리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque generated-platform jargon" in finding
                for finding in self.validate()
            )
        )

    def test_ambiguous_supporting_structure_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\nSQL/DDL Generator는 보조 구조로 둡니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "ambiguous supporting-structure wording" in finding
                for finding in self.validate()
            )
        )

    def test_opaque_bundled_flow_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n"
            "탐지 화면과 PR review 기준도 같은 변경 안전성 흐름 안에서 다뤘습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque bundled-flow wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_opaque_bundled_flow_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").write_text(
            "# Summary\n\n"
            "I handled display consistency as part of the same change-safety thread.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque bundled-flow wording" in finding
                for finding in self.validate()
            )
        )

    def test_vague_no_code_consistency_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n화면 설계 정보가 실행 코드, SQL, DB 상태, 테스트 요청 형식까지 일관되게 이어져야 했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "vague no-code consistency wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_vague_no_code_consistency_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nDesign information had to remain consistent as it turned into executable code.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "vague no-code consistency wording" in finding
                for finding in self.validate()
            )
        )

    def test_vague_homepage_connection_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n사용자가 정의한 서비스와 제품 변경이 실제 코드, SQL, 데이터 흐름까지 이어지도록 정리합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "vague no-code consistency wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_vague_homepage_connection_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").write_text(
            "# Summary\n\nConnects user-defined services and product changes to working code.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "vague no-code consistency wording" in finding
                for finding in self.validate()
            )
        )

    def test_opaque_related_work_criteria_heading_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n## 관련 작업 기준\n\n추상적인 기준을 설명합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque related-work criteria heading" in finding
                for finding in self.validate()
            )
        )

    def test_english_opaque_related_work_criteria_heading_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\n## Related Work Criteria\n\nExplains internal criteria.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque related-work criteria heading" in finding
                for finding in self.validate()
            )
        )

    def test_display_consistency_criteria_heading_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n## 표시 일관성 검토 기준\n\n기준을 반복합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque display-consistency criteria heading" in finding
                for finding in self.validate()
            )
        )

    def test_generic_validation_criteria_heading_is_rejected(self) -> None:
        (self.docs_dir / "project.md").write_text(
            "# 프로젝트\n\n## 검증과 기준\n\n기준을 반복합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "generic validation-criteria heading" in finding
                for finding in self.validate()
            )
        )

    def test_english_generic_validation_criteria_heading_is_rejected(self) -> None:
        (self.docs_dir / "project.en.md").write_text(
            "# Project\n\n## Validation and Criteria\n\nRepeats criteria.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "generic validation-criteria heading" in finding
                for finding in self.validate()
            )
        )

    def test_generic_display_consistency_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n같은 event context가 유지되는지 변경 안전성 기준으로 봤습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "generic display-consistency wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_generic_display_consistency_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nI reviewed event context drift as change-safety.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "generic display-consistency wording" in finding
                for finding in self.validate()
            )
        )

    def test_evidence_style_section_heading_is_rejected(self) -> None:
        (self.docs_dir / "opensource.md").write_text(
            "# GlueSQL\n\n## 검증 가능한 근거\n\n- 링크 없이 주장합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("evidence-style section heading" in finding for finding in self.validate())
        )

    def test_english_evidence_style_section_heading_is_rejected(self) -> None:
        (self.docs_dir / "opensource.en.md").write_text(
            "# GlueSQL\n\n## Verifiable Evidence\n\n- Trust this claim.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("evidence-style section heading" in finding for finding in self.validate())
        )

    def test_standalone_cli_application_heading_is_rejected(self) -> None:
        (self.docs_dir / "opensource.md").write_text(
            "# GlueSQL\n\n## CLI Application\n\nCLI만 별도 섹션으로 둡니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "standalone CLI application heading" in finding
                for finding in self.validate()
            )
        )

    def test_duplicative_technical_focus_heading_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n## 주요 기술 영역\n\n- 대표 작업 요약을 다시 나열합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "duplicative technical focus heading" in finding
                for finding in self.validate()
            )
        )

    def test_english_duplicative_technical_focus_heading_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").write_text(
            "# Summary\n\n## Technical Focus Areas\n\n- Repeats representative work.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "duplicative technical focus heading" in finding
                for finding in self.validate()
            )
        )

    def test_homepage_engineering_perspective_heading_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n## 개발 운영 관점\n\n일반적인 개발 기준을 반복합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "duplicative homepage engineering-perspective heading" in finding
                for finding in self.validate()
            )
        )

    def test_english_homepage_engineering_perspective_heading_is_rejected(self) -> None:
        (self.docs_dir / "index.en.md").write_text(
            "# Summary\n\n## Engineering Operating Perspective\n\nRepeats principles.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "duplicative homepage engineering-perspective heading" in finding
                for finding in self.validate()
            )
        )

    def test_work_direction_heading_is_rejected(self) -> None:
        experience_dir = self.docs_dir / "experience"
        experience_dir.mkdir()
        (experience_dir / "index.md").write_text(
            "# 경력\n\n## 엔지니어링 방향\n\n홈과 원칙 페이지 내용을 반복합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "duplicative work-direction heading" in finding
                for finding in self.validate()
            )
        )

    def test_english_work_direction_heading_is_rejected(self) -> None:
        experience_dir = self.docs_dir / "experience"
        experience_dir.mkdir()
        (experience_dir / "index.en.md").write_text(
            "# Work\n\n## Direction\n\nRepeats the homepage and principles.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "duplicative work-direction heading" in finding
                for finding in self.validate()
            )
        )

    def test_inconsistent_numbered_parquet_pr_label_is_rejected(self) -> None:
        (self.docs_dir / "opensource.md").write_text(
            "# GlueSQL\n\n"
            "- [Parquet Storage PR #1269](https://github.com/gluesql/gluesql/pull/1269)\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "inconsistent numbered Parquet PR label" in finding
                for finding in self.validate()
            )
        )

    def test_current_gluesql_merged_pr_count_wording_passes(self) -> None:
        (self.docs_dir / "opensource.md").write_text(
            "# GlueSQL\n\nGitHub `is:merged` 검색 기준 병합 PR 50건을 작성했습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_english_current_gluesql_merged_pr_count_wording_passes(self) -> None:
        (self.docs_dir / "opensource.en.md").write_text(
            "# GlueSQL\n\nI authored 50 merged PRs under GitHub `is:merged` search.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_stale_gluesql_merged_pr_count_wording_is_rejected(self) -> None:
        (self.docs_dir / "opensource.md").write_text(
            "# GlueSQL\n\nGitHub `is:merged` 검색 기준 병합 PR 44건을 작성했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "stale GlueSQL merged PR count wording" in finding
                for finding in self.validate()
            )
        )

    def test_stale_gluesql_merged_pr_count_range_wording_is_rejected(self) -> None:
        (self.docs_dir / "opensource.md").write_text(
            "# GlueSQL\n\nGitHub `is:merged` 검색 기준 병합 PR 50건 이상을 작성했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "stale GlueSQL merged PR count wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_stale_gluesql_merged_pr_count_wording_is_rejected(self) -> None:
        (self.docs_dir / "opensource.en.md").write_text(
            "# GlueSQL\n\nI authored 44+ merged PRs in GitHub search.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "stale GlueSQL merged PR count wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_stale_gluesql_exact_merged_pr_count_is_rejected(self) -> None:
        (self.docs_dir / "opensource.en.md").write_text(
            "# GlueSQL\n\nI authored 44 merged PRs in GitHub search.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "stale GlueSQL merged PR count wording" in finding
                for finding in self.validate()
            )
        )

    def test_coupler_funnel_baseline_count_is_not_rejected_as_gluesql_count(self) -> None:
        (self.docs_dir / "projects.md").write_text(
            "# Coupler\n\n"
            "Meta SDK postback event count 기준으로 1개월 심사 요청 도달 event가 "
            "약 50건에서 약 1.1k 수준으로 증가했습니다.\n",
            encoding="utf-8",
        )

        self.assertFalse(
            any(
                "stale GlueSQL merged PR count wording" in finding
                for finding in self.validate()
            )
        )

    def test_internal_entity_export_import_identifier_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n`selected_attr_ids`와 Broker App 연결을 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "internal entity export/import identifier" in finding
                for finding in self.validate()
            )
        )

    def test_internal_entity_export_import_template_identifier_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n`syncservice.ftl`은 후속 영역으로 분리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "internal entity export/import identifier" in finding
                for finding in self.validate()
            )
        )

    def test_public_cau_abbreviation_is_rejected_even_when_explained(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n변경 이력 기능(CAU)의 table 생성 흐름을 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(any("internal CAU acronym" in finding for finding in self.validate()))

    def test_english_public_cau_abbreviation_is_rejected_even_when_explained(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nI implemented change-history feature (CAU) tables.\n",
            encoding="utf-8",
        )

        self.assertTrue(any("internal CAU acronym" in finding for finding in self.validate()))

    def test_unexplained_public_abbreviation_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\nCAU table과 snapshot copy 흐름을 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(any("internal CAU acronym" in finding for finding in self.validate()))

    def test_internal_boundary_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n이 수치는 사용자 수나 전환율이 아니라 event count로만 사용합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("defensive metric wording" in finding for finding in self.validate())
        )

    def test_public_defensive_claim_disclaimer_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\np95 latency 개선으로 주장하지 않습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "public defensive claim-disclaimer wording" in finding
                for finding in self.validate()
            )
        )

    def test_public_claim_scope_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n**선택:** 성과 범위는 반복 변경 절차로 제한했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("public claim-scope wording" in finding for finding in self.validate())
        )

    def test_english_public_claim_scope_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\n**Selection:** I scoped the result to the workflow.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("public claim-scope wording" in finding for finding in self.validate())
        )

    def test_scope_limiting_selection_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n**선택:** 검증 범위는 API 확인으로 좁혔습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "scope-limiting public selection wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_scope_limiting_selection_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\n**Selection:** I scoped the work to API validation.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "scope-limiting public selection wording" in finding
                for finding in self.validate()
            )
        )

    def test_defensive_direct_scope_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n제가 맡은 범위는 Export client page입니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "defensive direct-scope wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_defensive_direct_scope_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nThe import page is outside my direct scope.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "defensive direct-scope wording" in finding
                for finding in self.validate()
            )
        )

    def test_opaque_working_criteria_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n당시 작업 기준 반복되던 cycle을 줄였습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque working-criteria wording" in finding
                for finding in self.validate()
            )
        )

    def test_english_opaque_working_criteria_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nUnder the working conditions at the time, it helped.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque working-criteria wording" in finding
                for finding in self.validate()
            )
        )

    def test_unqualified_percentage_comparison_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n설정 변경을 config 중심으로 바꾸어 30% 이상 줄였습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "unqualified percentage comparison" in finding
                for finding in self.validate()
            )
        )

    def test_qualified_percentage_comparison_passes(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n반복 설정 변경 1회 기준 작업 시간이 30% 이상 줄었습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_english_public_defensive_claim_disclaimer_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nI do not present it as p95 latency improvement.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "public defensive claim-disclaimer wording" in finding
                for finding in self.validate()
            )
        )

    def test_public_performance_disclaimer_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n별도 benchmark나 운영 로그 없이 p95/p99 latency 개선을 말합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "public performance-disclaimer wording" in finding
                for finding in self.validate()
            )
        )

    def test_unsupported_admission_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nThe limiter prevented over-limit admission.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "unsupported admission wording" in finding
                for finding in self.validate()
            )
        )

    def test_overclaim_absolute_solution_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n문제를 정확히 해결했고 매우 많은 문제를 처리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "overclaim absolute-solution wording" in finding
                for finding in self.validate()
            )
        )

    def test_internal_preparation_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n이 대표 사례는 case study readiness 기준으로 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("internal preparation wording" in finding for finding in self.validate())
        )

    def test_source_record_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 결과\n\n약 4주에서 2주 수준으로 줄이는 데 기여한 것으로 기록되어 있습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("source-record wording" in finding for finding in self.validate())
        )

    def test_page_framing_wording_is_rejected(self) -> None:
        (self.docs_dir / "activities.md").write_text(
            "# 활동\n\n이 페이지는 대표 기술 설명을 보조합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("page-framing wording" in finding for finding in self.validate())
        )

    def test_extended_page_framing_wording_is_rejected(self) -> None:
        (self.docs_dir / "opensource.en.md").write_text(
            "# Open Source\n\nThis page presents PR and review records.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("page-framing wording" in finding for finding in self.validate())
        )

    def test_shallow_portfolio_headings_are_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n내가 한 일:\n\n- 문제를 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("shallow portfolio headings" in finding for finding in self.validate())
        )

    def test_homepage_ai_agent_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n동료와 AI agent가 같은 기준으로 구현합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("tool-centered homepage wording" in finding for finding in self.validate())
        )

    def test_ai_agent_wording_is_allowed_outside_summary_pages(self) -> None:
        principles = self.docs_dir / "engineering-principles.md"
        principles.write_text(
            "# 원칙\n\n사람과 AI agent가 같은 기준으로 리뷰합니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_sensitive_local_path_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n근거는 /Users/example/Desktop/private-repo 입니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "sensitive local or secret wording" in finding
                for finding in self.validate()
            )
        )


if __name__ == "__main__":
    unittest.main()
