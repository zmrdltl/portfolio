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

    def test_internal_boundary_wording_is_rejected(self) -> None:
        (self.docs_dir / "index.md").write_text(
            "# 소개\n\n이 수치는 사용자 수나 전환율이 아니라 event count로만 사용합니다.\n",
            encoding="utf-8",
        )

        self.assertTrue(
            any("defensive metric wording" in finding for finding in self.validate())
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
