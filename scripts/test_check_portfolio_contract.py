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
    forbidden_headings: [기술]
""",
            encoding="utf-8",
        )
        (self.root / "detail.md").write_text(
            "# 상세\n\n**문제와 진단:** 원인\n\n**제약과 선택:** 결정\n",
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


if __name__ == "__main__":
    unittest.main()
