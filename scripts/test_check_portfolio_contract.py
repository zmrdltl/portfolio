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
            "\n".join(
                [
                    "version: 1",
                    "homepage:",
                    "  pages:",
                    "    - path: index.md",
                    "      representative_heading: 대표 작업",
                    "  representative_work:",
                    "    max_items: 4",
                    "    required_links:",
                    "      - experience/cluml.md",
                    "      - experience/tmaxcloud.md",
                    "      - opensource/gluesql.md",
                    "      - projects/coupler.md",
                    "  supporting_only_links:",
                    "    - activities/index.md",
                    "",
                ]
            ),
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

    def write_home(self, body: str) -> None:
        (self.root / "index.md").write_text(body, encoding="utf-8")

    def test_expected_representative_work_passes(self) -> None:
        self.write_home(
            "\n".join(
                [
                    "# 포트폴리오",
                    "",
                    "## 대표 작업",
                    "",
                    "- [ClumL](experience/cluml.md): 설명",
                    "- [TmaxCloud](experience/tmaxcloud.md): 설명",
                    "- [GlueSQL](opensource/gluesql.md): 설명",
                    "- [Coupler](projects/coupler.md): 설명",
                    "",
                    "## 다음",
                    "",
                ]
            )
        )

        self.assertEqual(self.validate(), [])

    def test_supporting_only_home_item_fails(self) -> None:
        self.write_home(
            "\n".join(
                [
                    "# 포트폴리오",
                    "",
                    "## 대표 작업",
                    "",
                    "- [ClumL](experience/cluml.md): 설명",
                    "- [TmaxCloud](experience/tmaxcloud.md): 설명",
                    "- [GlueSQL](opensource/gluesql.md): 설명",
                    "- [Coupler](projects/coupler.md): 설명",
                    "- [Activities](activities/index.md): 설명",
                    "",
                ]
            )
        )

        self.assertTrue(
            any("Supporting-only links" in finding for finding in self.validate())
        )

    def test_unexpected_representative_order_fails(self) -> None:
        self.write_home(
            "\n".join(
                [
                    "# 포트폴리오",
                    "",
                    "## 대표 작업",
                    "",
                    "- [TmaxCloud](experience/tmaxcloud.md): 설명",
                    "- [ClumL](experience/cluml.md): 설명",
                    "- [GlueSQL](opensource/gluesql.md): 설명",
                    "- [Coupler](projects/coupler.md): 설명",
                    "",
                ]
            )
        )

        self.assertTrue(
            any("Representative links must be" in finding for finding in self.validate())
        )


if __name__ == "__main__":
    unittest.main()
