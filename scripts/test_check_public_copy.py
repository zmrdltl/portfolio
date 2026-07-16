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

    def write_coupler_page(self, text: str, *, english: bool = False) -> None:
        projects_dir = self.docs_dir / "projects"
        projects_dir.mkdir(exist_ok=True)
        filename = "coupler.en.md" if english else "coupler.md"
        (projects_dir / filename).write_text(text, encoding="utf-8")

    def write_tmaxcloud_page(self, text: str, *, english: bool = False) -> None:
        experience_dir = self.docs_dir / "experience"
        experience_dir.mkdir(exist_ok=True)
        filename = "tmaxcloud.en.md" if english else "tmaxcloud.md"
        (experience_dir / filename).write_text(text, encoding="utf-8")

    def korean_entity_export_import_section(self) -> str:
        return (
            "# 티맥스클라우드\n\n"
            "## 개요\n\n"
            "엔티티 내보내기·가져오기 기능은 Studio에서 엔티티를 내보내 "
            "다른 생성 앱으로 가져와 서비스 정의에 사용하고, 가져오기 "
            "시점에는 선택 속성 데이터를 복사한 뒤 이후 해당 속성의 변경을 "
            "메시지 브로커를 통해 동기화했습니다. 내보낸·가져온 엔티티 "
            "정보를 저장하는 DB 스키마·API 개발에 참여하고, 선택 속성 "
            "메타데이터와 메시지 브로커를 거치는 엔티티 연결 구조를 "
            "설계했으며, 내보내기 화면을 구현했습니다.\n\n"
            "### 엔티티 내보내기·가져오기와 선택 속성 동기화\n\n"
            "Studio에서 엔티티를 내보내 다른 생성 앱으로 가져오고, "
            "가져온 엔티티를 서비스 정의에 사용하며, 연결된 서비스에서 "
            "데이터 변경이 발생하면 선택한 속성의 변경을 메시지 브로커를 "
            "통해 동기화했습니다. 내보낸 엔티티와 가져온 엔티티 정보를 "
            "저장하는 DB 스키마와 API 개발에 참여하고, 선택 속성 "
            "메타데이터와 메시지 브로커를 거치는 내보내기·가져오기 "
            "엔티티 연결 구조를 설계했으며, 내보내기 화면을 구현했습니다. "
            "메시지 동기화 서비스 자체 구현과 스키마 변경 후 재배포 "
            "마이그레이션 전략은 맡지 않았습니다.\n"
        )

    def english_entity_export_import_section(self) -> str:
        return (
            "# TmaxCloud\n\n"
            "## Overview\n\n"
            "The entity export/import feature let a Studio user export an entity, "
            "import it into another generated application, and use the imported "
            "entity in service definitions. It copied selected attribute data at "
            "import time and synchronized later changes to those attributes through "
            "a message broker. I contributed to the DB schema and API, designed "
            "selected-attribute metadata and broker-mediated linkage between "
            "exported and imported entities, and implemented the export UI.\n\n"
            "### Entity Export/Import and Selected-Attribute Synchronization\n\n"
            "Studio needed to export an entity, import it into another generated "
            "application, use the imported entity in service definitions, and "
            "synchronize changes to selected attributes through a message broker "
            "when connected services changed data. I contributed to the DB schema "
            "and API, designed selected-attribute metadata and broker-mediated "
            "linkage between exported and imported entities, and implemented the "
            "export UI. I did not implement the message-synchronization service "
            "itself or the redeployment migration strategy.\n"
        )

    def test_clean_public_copy_passes(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n문제 해결 과정과 검증 방법을 정리했습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_curator_facing_review_wording_is_rejected(self) -> None:
        samples = (
            "## 대표 작업으로 보는 이유\n",
            "## Why This Is Representative Work\n",
            "## 보조 검증 작업\n",
            "## Supporting Validation Work\n",
            "- 직접 구현, review, 운영 검증의 역할을 같은 성과로 합치지 않았습니다.\n",
            "- Kept direct implementation, review, and operational validation "
            "as separate contribution types.\n",
            "용량 확인과 예약 갱신을 같은 잠금 구간으로 묶었습니다.\n",
        )

        for sample in samples:
            with self.subTest(sample=sample):
                (self.docs_dir / "index.md").write_text(sample, encoding="utf-8")
                self.assertTrue(self.validate())

    def test_canonical_coupler_observations_pass(self) -> None:
        pages = (
            (
                False,
                "# Coupler\n\n"
                "Meta SDK 최초 가입 심사 도달 이벤트: "
                "개편 전 약 10건, 개편 후 약 100건 관측\n",
            ),
            (
                True,
                "# Coupler\n\n"
                "Meta SDK event recorded upon reaching the initial signup review "
                "stage: "
                "observed about 10 times before the redesign and about 100 times "
                "after.\n",
            ),
        )

        for english, page in pages:
            with self.subTest(english=english):
                self.write_coupler_page(page, english=english)
                self.assertEqual(self.validate(), [])

    def test_unrelated_growth_in_another_list_item_does_not_taint_metric(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 프로젝트\n\n"
            "- 처리량 증가를 확인했습니다.\n"
            "- 최초 가입 심사 도달 시 기록되는 Meta SDK "
            "CompleteRegistration(등록 완료) 이벤트가 개편 전 약 10건에서 "
            "개편 후 약 100건으로 관측됐습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

    def test_non_canonical_korean_coupler_observation_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "최초 가입 심사 도달 시 기록되는 Meta SDK "
            "CompleteRegistration(등록 완료) 이벤트가 회원가입·심사 흐름 "
            "개편 전 약 10건에서 개편 후 약 100건으로 관측됐습니다.\n",
        )

        self.assertTrue(
            any(
                "non-canonical Coupler observation wording" in finding
                for finding in self.validate()
            )
        )

    def test_korean_coupler_full_year_period_passes(self) -> None:
        self.write_coupler_page(
            "# Coupler\n\n- 참여 기간: 2024.07 - 현재\n"
        )

        self.assertEqual(self.validate(), [])

    def test_korean_coupler_abbreviated_year_period_is_rejected(self) -> None:
        samples = ("- 참여 기간: 24.07 - 현재\n",)

        for sample in samples:
            with self.subTest(sample=sample):
                self.write_coupler_page(f"# Coupler\n\n{sample}")
                self.assertTrue(
                    any(
                        "abbreviated-year Coupler Korean portfolio period wording"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_redundant_coupler_phase_metadata_is_rejected(self) -> None:
        pages = (
            (False, "- 참여 단계: 2024.07 초기 기여\n"),
            (True, "- Phases: Initial contribution, Jul 2024\n"),
        )

        for english, metadata in pages:
            with self.subTest(english=english):
                self.write_coupler_page(
                    f"# Coupler\n\n{metadata}", english=english
                )
                self.assertTrue(
                    any(
                        "redundant Coupler phase metadata" in finding
                        for finding in self.validate()
                    )
                )

    def test_non_canonical_english_coupler_observation_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "The Meta SDK event recorded upon reaching the first signup review was "
            "observed at roughly 10 events before the signup/review-flow redesign "
            "and roughly 100 afterward.\n",
            english=True,
        )

        self.assertTrue(
            any(
                "non-canonical Coupler observation wording" in finding
                for finding in self.validate()
            )
        )

    def test_korean_coupler_complete_registration_growth_wording_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "Meta SDK CompleteRegistration(등록 완료) 이벤트가 회원가입·심사 흐름 "
            "개편 전 약 10건에서 개편 후 약 100건으로 증가했습니다.\n",
        )

        self.assertTrue(
            any(
                "unsupported Coupler CompleteRegistration growth wording"
                in finding
                for finding in self.validate()
            )
        )

    def test_english_coupler_complete_registration_growth_wording_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "The Meta SDK CompleteRegistration event increased from roughly 10 "
            "events before the signup/review-flow redesign to roughly 100 after.\n",
            english=True,
        )

        self.assertTrue(
            any(
                "unsupported Coupler CompleteRegistration growth wording"
                in finding
                for finding in self.validate()
            )
        )

    def test_korean_observed_growth_wording_is_rejected(self) -> None:
        claims = (
            "관측됐지만 증가했습니다.",
            "관측됐지만 늘어났습니다.",
        )

        for claim in claims:
            with self.subTest(claim=claim):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "최초 가입 심사 도달 시 기록되는 Meta SDK CompleteRegistration"
                    "(등록 완료) 이벤트가 개편 전 약 10건에서 개편 후 약 "
                    f"100건으로 {claim}\n",
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration growth wording"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_english_observed_growth_wording_is_rejected(self) -> None:
        claims = (
            "was observed to increase from roughly 10 events before the redesign "
            "to roughly 100 after.",
            "was observed at roughly 10 events before the redesign and roughly 100 "
            "after, and grew.",
            "was observed at roughly 10 events before the redesign and roughly 100 "
            "after, and rose.",
            "was observed at roughly 10 events before the redesign and roughly 100 "
            "after, and showed growth.",
        )

        for claim in claims:
            with self.subTest(claim=claim):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "The Meta SDK CompleteRegistration event recorded at first "
                    f"signup review {claim}\n",
                    english=True,
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration growth wording"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_multiline_unqualified_coupler_observation_is_rejected(self) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "Meta SDK CompleteRegistration(등록 완료) 이벤트가\n"
            "회원가입·심사 흐름 개편 전 약 10건에서\n"
            "개편 후 약 100건으로 관측됐습니다.\n",
        )

        self.assertTrue(
            any(
                "unqualified Coupler Meta SDK observation"
                in finding
                for finding in self.validate()
            )
        )

    def test_multiline_coupler_growth_wording_is_rejected(self) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "최초 가입 심사 도달 시 기록되는 Meta SDK\n"
            "CompleteRegistration(등록 완료) 이벤트가 개편 전 약 10건에서\n"
            "개편 후 약 100건으로 관측됐지만\n"
            "증가했습니다.\n",
        )

        self.assertTrue(
            any(
                "unsupported Coupler CompleteRegistration growth wording" in finding
                for finding in self.validate()
            )
        )

    def test_korean_coupler_complete_registration_without_first_review_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "Meta SDK CompleteRegistration(등록 완료) 이벤트가 회원가입·심사 흐름 "
            "개편 전 약 10건에서 개편 후 약 100건으로 관측됐습니다.\n",
        )

        self.assertTrue(
            any(
                "unqualified Coupler Meta SDK observation"
                in finding
                for finding in self.validate()
            )
        )

    def test_english_coupler_complete_registration_without_first_review_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "The Meta SDK CompleteRegistration event was observed at roughly 10 "
            "events before the redesign and roughly 100 afterward.\n",
            english=True,
        )

        self.assertTrue(
            any(
                "unqualified Coupler Meta SDK observation"
                in finding
                for finding in self.validate()
            )
        )

    def test_unqualified_korean_coupler_complete_registration_observation_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "최초 가입 심사 도달 이벤트가 개편 전 약 10건에서 "
            "개편 후 약 100건으로 관측됐습니다.\n",
        )

        self.assertTrue(
            any(
                "unqualified Coupler Meta SDK observation"
                in finding
                for finding in self.validate()
            )
        )

    def test_unqualified_english_coupler_complete_registration_observation_is_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "First-signup-review reach was observed at roughly 10 events before the "
            "redesign and roughly 100 afterward.\n",
            english=True,
        )

        self.assertTrue(
            any(
                "unqualified Coupler Meta SDK observation"
                in finding
                for finding in self.validate()
            )
        )

    def test_stale_coupler_pre_complete_registration_comparisons_are_rejected(
        self,
    ) -> None:
        for baseline in ("40", "50"):
            for high_value in ("1.1k", "1,100", "1100"):
                with self.subTest(language="ko", baseline=baseline, high=high_value):
                    self.write_coupler_page(
                        "# Coupler\n\n"
                        f"기존 비교는 약 {baseline}건에서 약 {high_value}건으로 "
                        "기록됐습니다.\n",
                    )

                    self.assertTrue(
                        any(
                            "stale Coupler pre-CompleteRegistration comparison"
                            in finding
                            for finding in self.validate()
                        )
                    )

                with self.subTest(language="en", baseline=baseline, high=high_value):
                    self.write_coupler_page(
                        "# Coupler\n\n"
                        "The old comparison changed from about "
                        f"{baseline} events to about {high_value} events.\n",
                        english=True,
                    )

                    self.assertTrue(
                        any(
                            "stale Coupler pre-CompleteRegistration comparison"
                            in finding
                            for finding in self.validate()
                        )
                    )

    def test_korean_coupler_complete_registration_user_counts_are_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "최초 가입 심사 도달 시 기록되는 Meta SDK CompleteRegistration"
            "(등록 완료) 이벤트가 개편 전 약 10명에서 개편 후 약 100명으로 "
            "관측됐습니다.\n",
        )

        self.assertTrue(
            any(
                "unsupported Coupler CompleteRegistration metric interpretation"
                in finding
                for finding in self.validate()
            )
        )

    def test_english_coupler_complete_registration_user_counts_are_rejected(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "The Meta SDK CompleteRegistration event for first signup review reach "
            "was observed at roughly 10 users before the redesign and roughly 100 "
            "users afterward.\n",
            english=True,
        )

        self.assertTrue(
            any(
                "unsupported Coupler CompleteRegistration metric interpretation"
                in finding
                for finding in self.validate()
            )
        )

    def test_korean_coupler_registration_result_counts_are_rejected(self) -> None:
        for result_label in ("가입 완료 건수", "가입 성공 건수"):
            with self.subTest(result_label=result_label):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "최초 가입 심사 도달 시 기록되는 Meta SDK CompleteRegistration"
                    f"(등록 완료) 이벤트의 {result_label}가 개편 전 약 10건에서 "
                    "개편 후 약 100건으로 관측됐습니다.\n",
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration metric interpretation"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_english_coupler_registration_result_counts_are_rejected(self) -> None:
        for result_label in ("completed registrations", "successful registrations"):
            with self.subTest(result_label=result_label):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "The Meta SDK CompleteRegistration event for first signup review "
                    f"reach was observed at roughly 10 {result_label} before the "
                    f"redesign and roughly 100 {result_label} afterward.\n",
                    english=True,
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration metric interpretation"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_korean_coupler_causal_metric_claims_are_rejected(self) -> None:
        for causal_wording in ("개편으로", "개편 때문에"):
            with self.subTest(causal_wording=causal_wording):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "최초 가입 심사 도달 시 기록되는 Meta SDK CompleteRegistration"
                    "(등록 완료) 이벤트는 개편 전 약 10건, 개편 후 약 100건으로 "
                    f"관측됐고 이는 {causal_wording} 발생했습니다.\n",
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration metric interpretation"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_english_coupler_causal_metric_claims_are_rejected(self) -> None:
        causal_claims = (
            "The change was caused by the redesign.",
            "The redesign led to this change.",
            "The redesign resulted in this change.",
        )
        for causal_claim in causal_claims:
            with self.subTest(causal_claim=causal_claim):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "The Meta SDK CompleteRegistration event for first signup review "
                    "reach was observed at roughly 10 events before and roughly 100 "
                    f"after. {causal_claim}\n",
                    english=True,
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration metric interpretation"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_korean_coupler_monthly_normalization_is_rejected(self) -> None:
        for period_wording in ("1개월 기준", "월간"):
            with self.subTest(period_wording=period_wording):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "최초 가입 심사 도달 시 기록되는 Meta SDK CompleteRegistration"
                    f"(등록 완료) 이벤트가 {period_wording} 개편 전 약 10건에서 "
                    "개편 후 약 100건으로 관측됐습니다.\n",
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration metric interpretation"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_english_coupler_monthly_normalization_is_rejected(self) -> None:
        for period_wording in ("monthly", "one-month"):
            with self.subTest(period_wording=period_wording):
                self.write_coupler_page(
                    "# Coupler\n\n"
                    "The Meta SDK CompleteRegistration event for first signup review "
                    f"reach was observed on a {period_wording} basis at roughly 10 "
                    "events before the redesign and roughly 100 afterward.\n",
                    english=True,
                )

                self.assertTrue(
                    any(
                        "unsupported Coupler CompleteRegistration metric interpretation"
                        in finding
                        for finding in self.validate()
                    )
                )

    def test_unrelated_rounded_ten_and_hundred_values_pass(self) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "월간 계획에는 약 10개의 화면과 회귀 테스트 약 100개가 있습니다. "
            "이벤트 문서는 40개이고 참고 포트는 1100입니다.\n",
        )
        (self.docs_dir / "analytics.md").write_text(
            "# Analytics\n\n"
            "The Meta SDK CompleteRegistration metric changed from about 10 users "
            "to about 100 users on a monthly basis.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

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

    def test_semantic_regression_wording_is_rejected(self) -> None:
        samples = (
            (
                "index.en.md",
                "Reworked signup around a server-driven review-state contract.\n",
                "ambiguous Coupler state-contract wording",
            ),
            (
                "projects/coupler.en.md",
                "- Classification: Independent project, initially outsourced maintenance\n",
                "ambiguous Coupler outsourced-maintenance wording",
            ),
            (
                "projects/coupler.en.md",
                "The policy separates signup from profile-edit reviews.\n",
                "Coupler review-scope terminology drift",
            ),
            (
                "engineering-principles.en.md",
                "I fix core behavior and exceptional paths in tests.\n",
                "engineering-principle semantic inversion",
            ),
            (
                "engineering-principles.md",
                "### 3. 이관은 기준선·전환·정리로 나눕니다\n",
                "abstract engineering-principle wording",
            ),
            (
                "engineering-principles.en.md",
                "### 1. Separate Symptoms from Causes and Define the Change\n",
                "abstract engineering-principle wording",
            ),
            (
                "projects/coupler.md",
                "## App / API / Admin 책임 경계\n",
                "abstract Coupler responsibility-boundary heading",
            ),
            (
                "index.md",
                "요청 제한 경합 수정, 반복 운영 설정 외부화\n",
                "vague ClumL operational-setting wording",
            ),
            (
                "experience/cluml.md",
                "### 탐지 화면·리포트 검토\n",
                "vague ClumL detection-threshold wording",
            ),
            (
                "index.en.md",
                "network-event detection-threshold configuration\n",
                "vague ClumL detection-threshold wording",
            ),
            (
                "index.en.md",
                "Aligned app/admin routing to server review state.\n",
                "ambiguous Coupler routing or review-stage wording",
            ),
            (
                "opensource/gluesql.en.md",
                "I implemented storage paths for GlueSQL.\n",
                "vague GlueSQL storage-path wording",
            ),
            (
                "experience/cluml.md",
                "MITRE 화면의 시간 변환 모듈을 Jiff로 전환했습니다.\n",
                "overbroad ClumL time-conversion module wording",
            ),
            (
                "experience/tmaxcloud.en.md",
                "### Exception Output Formatting\n",
                "vague TmaxCloud exception-output heading",
            ),
            (
                "opensource/gluesql.en.md",
                "Encouragement Award · NIPA President Award\n",
                "GlueSQL award split into two awards",
            ),
        )

        for relative_path, sample, expected_finding in samples:
            with self.subTest(relative_path=relative_path):
                path = self.docs_dir / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(sample, encoding="utf-8")
                self.assertTrue(
                    any(
                        expected_finding in finding
                        for finding in self.validate()
                    )
                )
                path.unlink()

    def test_abstract_headings_require_a_concrete_subject(self) -> None:
        samples = (
            "# 운영 설정\n",
            "## 책임 경계\n",
            "## 역할 경계\n",
            "## 실패 모드와 책임 경계\n",
            "## 기준선 전환 정리\n",
            "## 실행 가능한 계약\n",
            "## 계약 개선\n",
            "## Contract Improvements\n",
            "## New Contract\n",
            "## Additional Implementation\n",
            "## 추가 구현\n",
            "## Implementation Details\n",
            "## Verification Results\n",
            "## Optimization Approach\n",
            "## Contract Testing\n",
            "## Implementation Summary\n",
            "## Verification Overview\n",
            "## 데이터 이관\n",
            "## 데이터 마이그레이션\n",
            "## 리뷰\n",
            "## 구조 개선\n",
            "## 성능 최적화\n",
            "## 검증\n",
            "## 데이터 동기화\n",
            "### 구조 검토\n",
            "### 운영 설정\n",
            "## Ownership Boundaries\n",
            "## Role Boundaries\n",
            "## Boundaries\n",
            "## Failure Modes and Responsibility Boundaries\n",
            "## Baseline Transition Cleanup\n",
            "## Executable Contracts\n",
            "## Migration Strategy\n",
            "## Migration Strategies\n",
            "## Implementation Strategy\n",
            "### Architecture Review\n",
            "#### Architecture Reviews\n",
            "##### Reviewing Architecture\n",
            "### Operational Configuration\n",
            "## Rapid Contracts\n",
            "## Specific Configuration\n",
            "## Statement Review\n",
            "[운영 설정](https://example.com)\n------------------------------\n",
            "## 운영 설정 {#details}\n",
            "Operational Settings\n---------------------\n",
            "> ## Operational Settings\n",
            "- ## Operational Settings\n",
        )

        for sample in samples:
            with self.subTest(sample=sample):
                (self.docs_dir / "clarity.md").write_text(
                    f"# Portfolio\n\n{sample}",
                    encoding="utf-8",
                )
                self.assertTrue(
                    any("heading" in finding for finding in self.validate())
                )

    def test_headings_with_concrete_subjects_pass(self) -> None:
        page = (
            "# Portfolio\n\n"
            "## API 응답 계약\n\n"
            "## 데이터 변경 이력 저장과 과거 시점 조회 설계\n\n"
            "## Chrono에서 Jiff로 시간 처리 의존성 전환\n\n"
            "## Database Schema Migration\n\n"
            "## Chrono/Jiff Compatibility Review\n\n"
            "## WebSocket Configuration\n\n"
            "## UI Design\n\n"
            "## Redis Cache Configuration\n\n"
            "## Search Index Design\n\n"
            "## OAuth Callback Review\n\n"
            "## Design System Review\n\n"
            "## Design System Configuration\n\n"
            "## System Architecture Review\n\n"
            "## Data Architecture Review\n\n"
            "## Data Contract Testing\n\n"
            "## API Implementation Strategy\n\n"
            "### 리포트 조회 범위·DHCP 옵션 표시 검증\n\n"
            "## Moving a Network-Event Detection Threshold to External "
            "Configuration\n\n"
            "### ErrorLogger-Based Exception Formatting\n\n"
            "## Review, Mentoring, and Awards\n\n"
            "```markdown\n"
            "## Operational Settings\n\n"
            "Architecture Review\n"
            "-------------------\n"
            "```\n\n"
            "<!--\n"
            "## Operational Settings\n"
            "-->\n\n"
            "<pre>\n"
            "## Operational Settings\n"
            "</pre>\n\n"
            "<details>\n"
            "## Operational Settings\n"
            "</details>\n\n"
            "<div>\n"
            "## Operational Settings\n"
            "</div>\n"
        )
        (self.docs_dir / "clarity.md").write_text(page, encoding="utf-8")

        self.assertEqual(self.validate(), [])

    def test_unverified_coupler_conversion_and_cost_metrics_are_rejected(self) -> None:
        claims = (
            "전환율이 개선됐습니다.",
            "가입 성공률이 높아졌습니다.",
            "심사 시간 단축을 확인했습니다.",
            "CAC가 낮아졌습니다.",
            "CPA가 낮아졌습니다.",
        )

        for claim in claims:
            with self.subTest(claim=claim):
                self.write_coupler_page(f"# Coupler\n\n{claim}\n")

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

    def test_opaque_point_in_time_state_reconstruction_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n특정 시점 상태 재구성을 설계했습니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque generated-platform jargon" in finding
                for finding in self.validate()
            )
        )

    def test_english_point_in_time_state_reconstruction_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nI designed Point-in-Time State Reconstruction.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "opaque generated-platform jargon" in finding
                for finding in self.validate()
            )
        )

    def test_opaque_state_contract_reconstruction_is_rejected(self) -> None:
        (self.docs_dir / "project.md").write_text(
            "# 프로젝트\n\n상태 계약 재구성을 구현했습니다.\n",
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

    def test_coupler_complete_registration_counts_are_not_rejected_as_gluesql_count(
        self,
    ) -> None:
        self.write_coupler_page(
            "# Coupler\n\n"
            "최초 가입 심사 도달 시 기록되는 Meta SDK "
            "CompleteRegistration(등록 완료) 이벤트가 개편 전 약 10건에서 "
            "개편 후 약 100건으로 관측됐습니다.\n",
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

    def test_korean_entity_export_import_semantics_pass(self) -> None:
        self.write_tmaxcloud_page(self.korean_entity_export_import_section())

        self.assertEqual(self.validate(), [])

    def test_english_entity_export_import_semantics_pass(self) -> None:
        self.write_tmaxcloud_page(
            self.english_entity_export_import_section(),
            english=True,
        )

        self.assertEqual(self.validate(), [])

    def test_entity_export_import_initial_copy_only_is_rejected(self) -> None:
        page = self.korean_entity_export_import_section().replace(
            "Studio에서 엔티티를 내보내 다른 생성 앱으로 가져오고, "
            "가져온 엔티티를 서비스 정의에 사용하며, 연결된 서비스에서 "
            "데이터 변경이 발생하면 선택한 속성의 변경을 메시지 브로커를 "
            "통해 동기화했습니다.",
            "가져오기 시점의 초기 데이터 복사만 구현했습니다.",
        )
        self.write_tmaxcloud_page(page)

        self.assertTrue(
            any(
                "entity export/import reduced to initial-copy-only wording" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_missing_service_definition_use_is_rejected(
        self,
    ) -> None:
        page = self.korean_entity_export_import_section().replace(
            "가져온 엔티티를 서비스 정의에 사용하며, ",
            "",
        )
        self.write_tmaxcloud_page(page)

        self.assertTrue(
            any(
                "service-definition and synchronization flow" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_missing_broker_linkage_is_rejected(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "broker-mediated linkage",
            "linkage",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "missing direct contribution relationships" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_application_wide_scope_is_rejected(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "changes to selected attributes",
            "application-wide data changes",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "expanded to application-wide synchronization" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_sync_service_overclaim_is_rejected(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "I did not implement the message-synchronization service itself",
            "I implemented the message-synchronization service",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "message-synchronization service implementation overclaim" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_export_ui_negation_is_rejected(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "I did not implement the message-synchronization service itself",
            "I did not implement the export UI. "
            "I did not implement the message-synchronization service itself",
        ).replace(
            "and implemented the export UI.",
            ".",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "missing direct contribution relationships" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_korean_direct_contribution_negation_is_rejected(
        self,
    ) -> None:
        page = self.korean_entity_export_import_section().replace(
            "API 개발에 참여하고",
            "API 개발에 참여하지 않았고",
        ).replace(
            "연결 구조를 설계했으며",
            "연결 구조를 설계하지 않았으며",
        ).replace(
            "내보내기 화면을 구현했습니다",
            "내보내기 화면을 구현하지 않았습니다",
        )
        self.write_tmaxcloud_page(page)

        self.assertTrue(
            any(
                "missing direct contribution relationships" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_third_party_contribution_is_rejected(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "I contributed to the DB schema and API, designed selected-attribute "
            "metadata and broker-mediated linkage between exported and imported "
            "entities, and implemented the export UI.",
            "The team contributed to the DB schema and API. Another engineer "
            "designed selected-attribute metadata and broker-mediated linkage "
            "between exported and imported entities and implemented the export UI.",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "missing direct contribution relationships" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_korean_third_party_contribution_is_rejected(
        self,
    ) -> None:
        page = self.korean_entity_export_import_section().replace(
            "내보낸 엔티티와 가져온 엔티티 정보를 저장하는 DB 스키마와 "
            "API 개발에 참여하고, 선택 속성 메타데이터와 메시지 브로커를 "
            "거치는 내보내기·가져오기 엔티티 연결 구조를 설계했으며, "
            "내보내기 화면을 구현했습니다.",
            "팀이 내보낸 엔티티와 가져온 엔티티 정보를 저장하는 DB 스키마와 "
            "API 개발에 참여하고, 다른 엔지니어가 선택 속성 메타데이터와 "
            "메시지 브로커를 거치는 내보내기·가져오기 엔티티 연결 구조를 "
            "설계했으며, 내보내기 화면을 구현했습니다.",
        )
        self.write_tmaxcloud_page(page)

        self.assertTrue(
            any(
                "missing direct contribution relationships" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_korean_multisentence_contribution_passes(
        self,
    ) -> None:
        page = self.korean_entity_export_import_section().replace(
            "내보낸 엔티티와 가져온 엔티티 정보를 저장하는 DB 스키마와 "
            "API 개발에 참여하고, 선택 속성 메타데이터와 메시지 브로커를 "
            "거치는 내보내기·가져오기 엔티티 연결 구조를 설계했으며, "
            "내보내기 화면을 구현했습니다.",
            "내보낸 엔티티와 가져온 엔티티 정보를 저장하는 DB 스키마와 "
            "API 개발에 참여했습니다. 선택 속성 메타데이터와 메시지 "
            "브로커를 거치는 내보내기·가져오기 엔티티 연결 구조를 "
            "설계했습니다. 내보내기 화면을 구현했습니다.",
        )
        self.write_tmaxcloud_page(page)

        self.assertEqual(self.validate(), [])

    def test_entity_export_import_overview_scope_regression_is_rejected(
        self,
    ) -> None:
        page = self.english_entity_export_import_section().replace(
            "The entity export/import feature let a Studio user export an entity, "
            "import it into another generated application, and use the imported "
            "entity in service definitions. It copied selected attribute data at "
            "import time and synchronized later changes to those attributes through "
            "a message broker.",
            "The entity export/import feature synchronized application-wide data.",
        )
        self.write_tmaxcloud_page(page, english=True)

        findings = self.validate()
        self.assertTrue(
            any(
                "expanded to application-wide synchronization" in finding
                for finding in findings
            )
        )
        self.assertTrue(
            any(
                "overview loses entity export/import flow or contribution boundaries"
                in finding
                for finding in findings
            )
        )

    def test_entity_export_import_overview_service_definition_is_required(
        self,
    ) -> None:
        page = self.english_entity_export_import_section().replace(
            ", and use the imported entity in service definitions. It copied",
            ". It copied",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "overview loses entity export/import flow or contribution boundaries"
                in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_overview_ownership_overclaim_is_rejected(
        self,
    ) -> None:
        page = self.english_entity_export_import_section().replace(
            "It copied selected attribute data at import time and synchronized "
            "later changes to those attributes through a message broker.",
            "I implemented copying of selected attribute data at import time and "
            "synchronization of later changes through a message broker.",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "overview loses entity export/import flow or contribution boundaries"
                in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_korean_role_subject_is_rejected(self) -> None:
        page = self.korean_entity_export_import_section().replace(
            "내보낸 엔티티와 가져온 엔티티 정보를 저장하는 DB 스키마와 "
            "API 개발에 참여하고, 선택 속성 메타데이터와 메시지 브로커를 "
            "거치는 내보내기·가져오기 엔티티 연결 구조를 설계했으며, "
            "내보내기 화면을 구현했습니다.",
            "담당 엔지니어가 내보낸 엔티티와 가져온 엔티티 정보를 저장하는 "
            "DB 스키마와 API 개발에 참여하고, 선택 속성 메타데이터와 메시지 "
            "브로커를 거치는 내보내기·가져오기 엔티티 연결 구조를 "
            "설계했으며, 내보내기 화면을 구현했습니다.",
        )
        self.write_tmaxcloud_page(page)

        self.assertTrue(
            any(
                "missing direct contribution relationships" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_migration_overclaim_is_rejected(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "I did not implement the message-synchronization service "
            "itself or the redeployment migration strategy.",
            "I did not implement the message-synchronization service itself. "
            "I implemented the redeployment migration strategy.",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertTrue(
            any(
                "redeployment migration-strategy overclaim" in finding
                for finding in self.validate()
            )
        )

    def test_entity_export_import_paraphrase_passes(self) -> None:
        page = self.english_entity_export_import_section().replace(
            "Studio needed to export an entity, import it into another generated "
            "application,",
            "The product UI needed to export an entity, import it into a second app,",
        ).replace(
            "### Entity Export/Import and Selected-Attribute Synchronization",
            "### Entity Export and Import with Selected Attribute Change Synchronization",
        )
        self.write_tmaxcloud_page(page, english=True)

        self.assertEqual(self.validate(), [])

    def test_entity_export_import_contract_does_not_apply_to_other_pages(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n엔티티 초기 데이터 복사를 검토했습니다.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.validate(), [])

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

    def test_opaque_development_environment_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.md").write_text(
            "# 경험\n\n당시 개발 환경에서 반복되던 cycle을 줄였습니다.\n",
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

    def test_english_working_environment_wording_is_rejected(self) -> None:
        (self.docs_dir / "experience.en.md").write_text(
            "# Work\n\nIn the working environment, it reduced repetition.\n",
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

    def test_defensive_coupler_ai_ownership_wording_is_rejected(self) -> None:
        project_dir = self.docs_dir / "projects"
        project_dir.mkdir()
        (project_dir / "coupler.md").write_text(
            (
                "# Coupler\n\n"
                "LLM을 구현 보조에 사용했지만 제품·기술 판단은 직접 책임졌습니다.\n"
            ),
            encoding="utf-8",
        )

        self.assertTrue(
            any(
                "defensive Coupler AI-ownership wording" in finding
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
