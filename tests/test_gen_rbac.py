import csv
import io
import json

from erp_spec_forge.gen_rbac import (
    effective_modules,
    generate_matrix_csv,
    generate_matrix_md,
    generate_registry_json,
    role_function_codes,
)


def test_effective_modules_derive_crud(system):
    eff = effective_modules(system)
    assert len(eff) == 8
    proc = next(m for m in eff if m["code"] == "procurement")
    codes = {f["code"] for f in proc["functions"]}
    # 8 个实体 × 5 个 CRUD = 40 推导 + 3 自定义
    assert len(codes) == 43
    assert "purchase_task_list" in codes
    assert "purchase_task_release" in codes
    assert "supplier_price_approve" in codes


def test_role_wildcard_grant(system):
    admin = next(r for r in system.roles if r.code == "sys_admin")
    codes = role_function_codes(system, admin)
    eff_total = sum(len(m["functions"]) for m in effective_modules(system))
    assert len(codes) == eff_total


def test_role_explicit_grant(system):
    clerk = next(r for r in system.roles if r.code == "purchase_clerk")
    codes = role_function_codes(system, clerk)
    assert "purchase_task_release" in codes
    assert "supplier_create" in codes
    assert "supplier_delete" not in codes  # 文员没有删除权
    assert "stock_in_list" not in codes  # 其他模块未授权


def test_matrix_md_shape(system):
    md = generate_matrix_md(system)
    assert md.startswith("# 权限矩阵")
    assert "| 功能码 |" in md
    assert md.count("●") >= 100  # 至少覆盖到大量授权点


def test_matrix_csv_and_registry(system):
    rows = list(csv.reader(io.StringIO(generate_matrix_csv(system))))
    assert rows[0][:3] == ["function_code", "sys_admin", "purchase_manager"]
    body = rows[1:]
    assert len(body) == sum(len(m["functions"]) for m in effective_modules(system))
    assert all(r[1] == "1" for r in body)  # sys_admin 全量授权

    registry = json.loads(generate_registry_json(system))
    assert registry["system"] == "fresh-supply-erp"
    assert len(registry["modules"]) == 8
    assert len(registry["roles"]) == 9
