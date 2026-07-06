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
