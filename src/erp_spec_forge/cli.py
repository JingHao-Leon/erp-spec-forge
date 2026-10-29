"""CLI: validate / generate. Entry points: `erp-spec-forge` and `python -m erp_spec_forge`."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from . import __version__
from .gen_docs import generate_data_dictionary, generate_readme_doc, generate_workflows_md
from .gen_openapi import generate_openapi
from .gen_rbac import generate_matrix_csv, generate_matrix_md, generate_registry_json
from .gen_sql import generate_sql
from .loader import load
from .validate import validate


def _do_validate(specs: str) -> int:
    system = load(specs)
    errors = validate(system)
    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        print(f"validation failed: {len(errors)} problem(s)", file=sys.stderr)
        return 1
    n_entities = len(system.entities)
    print(
        f"OK {system.name} v{system.spec_version}: {len(system.domains)} domains, "
        f"{n_entities} entities, {len(system.workflows)} workflows, {len(system.roles)} roles"
    )
    return 0


def _do_generate(specs: str, out: str) -> int:
    code = _do_validate(specs)
    if code != 0:
        return code
    system = load(specs)
    outdir = Path(out)
    (outdir / "sql").mkdir(parents=True, exist_ok=True)
    (outdir / "openapi").mkdir(parents=True, exist_ok=True)
    (outdir / "rbac").mkdir(parents=True, exist_ok=True)
    (outdir / "docs").mkdir(parents=True, exist_ok=True)

    (outdir / "sql" / "schema.sql").write_text(generate_sql(system), encoding="utf-8")
    (outdir / "openapi" / "openapi.yaml").write_text(
        yaml.safe_dump(generate_openapi(system), allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    (outdir / "rbac" / "matrix.md").write_text(generate_matrix_md(system), encoding="utf-8")
    (outdir / "rbac" / "matrix.csv").write_text(generate_matrix_csv(system), encoding="utf-8")
    (outdir / "rbac" / "registry.json").write_text(generate_registry_json(system), encoding="utf-8")
    (outdir / "docs" / "data-dictionary.md").write_text(generate_data_dictionary(system), encoding="utf-8")
    (outdir / "docs" / "workflows.md").write_text(generate_workflows_md(system), encoding="utf-8")
    (outdir / "docs" / "overview.md").write_text(generate_readme_doc(system), encoding="utf-8")

    n_paths = len(generate_openapi(system)["paths"])
    print(f"generated into {outdir}: sql/openapi/rbac/docs "
          f"({len(system.entities)} entities, {n_paths} API paths, {len(system.roles)} roles)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="erp-spec-forge",
        description="Spec-driven ERP design toolkit: validate YAML specs, forge SQL/OpenAPI/RBAC/docs.",
    )
    parser.add_argument("--version", action="version", version=f"erp-spec-forge {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="validate the spec tree")
    p_val.add_argument("--specs", default="specs", help="spec directory (default: specs)")

    p_gen = sub.add_parser("generate", help="generate SQL/OpenAPI/RBAC/docs from the spec tree")
    p_gen.add_argument("--specs", default="specs", help="spec directory (default: specs)")
    p_gen.add_argument("--out", default="dist", help="output directory (default: dist)")

    args = parser.parse_args(argv)
    if args.command == "validate":
        return _do_validate(args.specs)
    if args.command == "generate":
        return _do_generate(args.specs, args.out)
    parser.error(f"unknown command {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
