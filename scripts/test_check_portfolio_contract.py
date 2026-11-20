from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from scripts.check_portfolio_contract import validate_contract


class PortfolioContractCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.contract_path = self.root / "portfolio.contract.yml"
        self.write_contract()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_contract(self) -> None:
        self.contract_path.write_text(
            """\
version: 2
homepage:
  representative_work:
    exact_items: 2
    required_links:
      - cluml.md
      - coupler.md
  pages:
    - path: index.md
      representative_heading: 대표 작업
      field_labels:
        type_period: 유형·기간
        role: 역할
        change: 핵심 변화
        proof: 검증
        technologies: 기술
      forbidden_headings:
        - 작업별 기술
      records:
        cluml.md:
          type_period: [정규 경력, "2025.03"]
          role: [Rust]
          change: [경합]
          proof: [회귀]
          technologies: [Rust, 동시성 제어]
        coupler.md:
          type_period: [개인 제품, 현재]
          role: [개발총괄]
          change: [API]
          proof: [심사 큐]
          technologies: [TypeScript, MySQL]
content_coverage:
  - path: detail.md
    required_terms: [문제와 진단, 제약과 선택]
    section_fields:
      주요 사례:
        검증과 결과: [허용 요청 수, 제한 검사, 같은 동시성 조건, 한도를 지켰습니다]
    forbidden_headings: [기술]
""",
            encoding="utf-8",
        )
        self.write_detail(
            "**검증과 결과:** 허용 요청\n수보다 많은 요청이 제한 검사를 통과했습니다.\n"
            "수정 후 같은 동시성 조건에서 한도를 지켰습니다."
        )

    def write_detail(self, case: str) -> None:
        (self.root / "detail.md").write_text(
            "# 상세\n\n## 주요 사례\n\n**문제와 진단:** 원인\n\n"
            f"**제약과 선택:** 결정\n\n{case}\n",
            encoding="utf-8",
        )

    def validate(self) -> list[str]:
        current = Path.cwd()
        try:
            import os

            os.chdir(self.root)
            findings, _ = validate_contract(self.contract_path)
            return findings
        finally:
            os.chdir(current)

    def write_home(self, *, reverse: bool = False, extra_tag: bool = False) -> None:
        cluml = """\
### [ClumL](cluml.md)

**유형·기간:** 정규 경력 · 2025.03

**역할:** Rust 백엔드

**핵심 변화:** 확인-예약 경합 수정

**검증:** 회귀 테스트

**기술:** `Rust` · `동시성 제어`
"""
        coupler_tags = "`TypeScript` · `MySQL`"
        if extra_tag:
            coupler_tags += " · `React` · `Express`"
        coupler = f"""\
### [Coupler](coupler.md)

**유형·기간:** 개인 제품 · 현재

**역할:** 개발총괄

**핵심 변화:** API 상태 통일

**검증:** 관리자 심사 큐 회귀 테스트

**기술:** {coupler_tags}
"""
        records = coupler + "\n" + cluml if reverse else cluml + "\n" + coupler
        (self.root / "index.md").write_text(
            "# 포트폴리오\n\n## 대표 작업\n\n" + records + "\n## 연락처\n",
            encoding="utf-8",
        )

    def test_expected_home_records_pass(self) -> None:
        self.write_home()
        self.assertEqual(self.validate(), [])

    def test_unexpected_order_fails(self) -> None:
        self.write_home(reverse=True)
        self.assertTrue(
            any("Representative links must be" in finding for finding in self.validate())
        )

    def test_missing_record_field_fails(self) -> None:
        self.write_home()
        path = self.root / "index.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("**검증:** 회귀 테스트\n", ""),
            encoding="utf-8",
        )
        self.assertTrue(any("exactly one `검증`" in item for item in self.validate()))

    def test_more_than_three_technology_tags_fails(self) -> None:
        self.write_home(extra_tag=True)
        self.assertTrue(any("2-3 technology tags" in item for item in self.validate()))

    def test_separate_technology_summary_fails(self) -> None:
        self.write_home()
        path = self.root / "index.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n## 작업별 기술\n",
            encoding="utf-8",
        )
        self.assertTrue(
            any("Forbidden duplicate-summary heading" in item for item in self.validate())
        )

    def test_missing_detail_reasoning_marker_fails(self) -> None:
        (self.root / "detail.md").write_text(
            "# 상세\n\n**문제와 진단:** 원인\n", encoding="utf-8"
        )
        self.write_home()
        self.assertTrue(any("Required content coverage" in item for item in self.validate()))

    def test_detail_evidence_must_be_in_the_named_case_field(self) -> None:
        self.write_home()
        proof = "허용 요청 수를 기준으로 제한 검사를 같은 동시성 조건에서 확인했습니다."
        for misplaced in (
            f"**구현:** {proof}",
            f"\n{proof}",
            f"\n### 하위 사례\n\n**검증과 결과:** {proof}",
            f"\n## 추가 작업\n\n**검증과 결과:** {proof}",
        ):
            with self.subTest(misplaced=misplaced):
                self.write_detail(f"**검증과 결과:** 토큰 예산을 확인했습니다.\n{misplaced}")
                findings = self.validate()
                self.assertEqual(len(findings), 1)
                self.assertIn("`주요 사례` / `검증과 결과` is missing `허용 요청 수`", findings[0])

    def test_detail_evidence_must_follow_the_configured_order(self) -> None:
        self.write_home()
        self.write_detail("**검증과 결과:** 같은 동시성 조건에서 허용 요청 수와 제한 검사를 확인했습니다.")
        findings = self.validate()
        self.assertEqual(len(findings), 1)
        self.assertIn("missing `같은 동시성 조건` in the required order", findings[0])

    def test_detail_evidence_must_keep_the_result(self) -> None:
        self.write_home()
        self.write_detail(
            "**검증과 결과:** 허용 요청 수보다 많은 요청이 제한 검사를 통과했습니다. "
            "수정 후에도 같은 동시성 조건에서 한도를 계속 넘었습니다."
        )
        findings = self.validate()
        self.assertEqual(len(findings), 1)
        self.assertIn("missing `한도를 지켰습니다`", findings[0])

    def test_comments_and_code_cannot_supply_visible_fields_or_headings(self) -> None:
        self.write_home()
        proof = (
            "**검증과 결과:** 허용 요청 수를 기준으로 제한 검사를 "
            "같은 동시성 조건에서 확인해 한도를 지켰습니다."
        )
        self.write_detail(f"    {proof}")
        findings = self.validate()
        self.assertEqual(len(findings), 1)
        self.assertIn("`주요 사례` / `검증과 결과` must appear exactly once", findings[0])

        for start, end in (("<!--", "-->"), ("````markdown", "````"), ("~~~", "~~~")):
            with self.subTest(start=start):
                self.write_detail(f"{start}\n{proof}\n{end}")
                findings = self.validate()
                self.assertEqual(len(findings), 1)
                self.assertIn("`주요 사례` / `검증과 결과` must appear exactly once", findings[0])
                self.write_detail(f"{start}\n## 추가 작업\n{end}\n\n{proof}")
                self.assertEqual(self.validate(), [])


if __name__ == "__main__":
    unittest.main()
