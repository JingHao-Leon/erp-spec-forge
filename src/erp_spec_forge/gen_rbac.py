"""RBAC artifacts: effective function list per module (CRUD-derived + custom), permission matrix, module registry."""
from __future__ import annotations

import json

from .loader import System, derived_functions


def effective_modules(system: System) -> list[dict]:
    """Modules with their effective functions: custom functions plus CRUD codes of the
    entities belonging to the module's domain (verb convention)."""
    out = []
    entity_by_domain: dict[str, list] = {}
    for d in system.domains:
        entity_by_domain[d.code] = d.entities
    for m in system.modules:
        fns = list(m.functions)
        codes = {f["code"] for f in fns}
        for e in entity_by_domain.get(m.domain, []):
            for f in derived_functions(e):
                if f["code"] not in codes:
                    fns.append(f)
                    codes.add(f["code"])
        out.append({"code": m.code, "name": m.name, "domain": m.domain, "functions": fns})
    return out


def role_function_codes(system: System, role) -> set[str]:
    granted: set[str] = set()
    eff = {m["code"]: m for m in effective_modules(system)}
    for mod, fns in role.grants.items():
        m = eff.get(mod)
        if m is None:
            continue
        if fns == "*":
            granted.update(f["code"] for f in m["functions"])
        else:
            granted.update(fns)
    return granted


def generate_matrix_md(system: System) -> str:
    eff = effective_modules(system)
    roles = system.roles
    grant_map = {r.code: role_function_codes(system, r) for r in roles}
    lines = [
        "# 权限矩阵（RBAC Matrix）",
        "",
        "> 行 = 功能码（模块内自定义 + 实体 CRUD 推导），列 = 角色，● = 授权。由 erp-spec-forge 生成。",
        "",
    ]
    header = "| 功能码 | " + " | ".join(r.name for r in roles) + " |"
    sep = "|---|" + "---|" * len(roles)
    lines += [header, sep]
    for m in eff:
        lines.append(f"| **{m['name']}（{m['code']}）** | " + " | ".join([""] * len(roles)) + " |")
        for f in m["functions"]:
            marks = ["●" if f["code"] in grant_map.get(r.code, set()) else "" for r in roles]
            lines.append("| " + " | ".join([f["code"], *marks]) + " |")
    lines.append("")
    return "\n".join(lines)


def generate_matrix_csv(system: System) -> str:
    eff = effective_modules(system)
    roles = system.roles
    grant_map = {r.code: role_function_codes(system, r) for r in roles}
    rows = ["function_code," + ",".join(r.code for r in roles)]
    for m in eff:
        for f in m["functions"]:
            rows.append(f["code"] + "," + ",".join("1" if f["code"] in grant_map.get(r.code, set()) else "0" for r in roles))
    return "\n".join(rows) + "\n"


def generate_registry_json(system: System) -> str:
    doc = {
        "system": system.name,
        "display": system.display,
        "spec_version": system.spec_version,
        "modules": effective_modules(system),
        "roles": [{"code": r.code, "name": r.name, "description": r.description} for r in system.roles],
    }
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
