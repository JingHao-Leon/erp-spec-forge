from pathlib import Path

import pytest

from erp_spec_forge.cli import main

SPECS = Path(__file__).resolve().parents[1] / "specs"
EXPECTED_OUTPUTS = [
    "sql/schema.sql",
    "openapi/openapi.yaml",
    "rbac/matrix.md",
    "rbac/matrix.csv",
    "rbac/registry.json",
    "docs/data-dictionary.md",
    "docs/workflows.md",
    "docs/overview.md",
]


def test_cli_validate_ok(capsys):
    assert main(["validate", "--specs", str(SPECS)]) == 0
    out = capsys.readouterr().out
    assert "8 domains, 46 entities, 3 workflows, 9 roles" in out


def test_cli_generate_end_to_end(tmp_path):
    out = tmp_path / "dist"
    assert main(["generate", "--specs", str(SPECS), "--out", str(out)]) == 0
    for rel in EXPECTED_OUTPUTS:
        p = out / rel
        assert p.exists() and p.stat().st_size > 0, f"missing {rel}"
    sql = (out / "sql" / "schema.sql").read_text(encoding="utf-8")
    assert sql.count("CREATE TABLE") == 46


def test_cli_generate_fails_on_broken_specs(tmp_path):
    broken = tmp_path / "specs"
    broken.mkdir()
    (broken / "erp.yaml").write_text(
        "spec_version: t\nsystem: {name: t, display: t}\ndomains: [a]\n", encoding="utf-8"
    )
    (broken / "domains").mkdir()
    (broken / "domains" / "a.yaml").write_text(
        "domain: a\nname: a\nentities:\n  - name: t1\n    display: t\n"
        "    fields:\n      - {name: id, type: pk}\n"
        "  - name: t1\n    display: t2\n"
        "    fields:\n      - {name: id, type: pk}\n",
        encoding="utf-8",
    )
    assert main(["generate", "--specs", str(broken), "--out", str(tmp_path / "d")]) == 1


def test_cli_missing_domain_file(tmp_path):
    specs = tmp_path / "specs"
    specs.mkdir()
    (specs / "erp.yaml").write_text(
        "spec_version: t\nsystem: {name: t, display: t}\ndomains: [ghost]\n", encoding="utf-8"
    )
    with pytest.raises(FileNotFoundError):
        main(["validate", "--specs", str(specs)])
