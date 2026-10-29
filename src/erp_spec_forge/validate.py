"""Structural validation of a loaded System. Returns a list of human-readable errors."""
from __future__ import annotations

import re

from .loader import FIELD_TYPES, System

NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")
CODE_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def validate(system: System) -> list[str]:
    errors: list[str] = []

    if not system.name:
        errors.append("system.name is empty")

    # --- entities & fields ---
    seen_entities: dict[str, str] = {}
    for d in system.domains:
        for e in d.entities:
            if not NAME_RE.match(e.name):
                errors.append(f"entity name not snake_case: {e.name}")
            if e.name in seen_entities:
                errors.append(f"duplicate entity '{e.name}' in {d.code} (first seen in {seen_entities[e.name]})")
            else:
                seen_entities[e.name] = d.code
            seen_fields: set[str] = set()
            has_pk = False
            for f in e.fields:
                if not NAME_RE.match(f.name):
                    errors.append(f"{e.name}.{f.name}: field name not snake_case")
                if f.name in seen_fields:
                    errors.append(f"{e.name}.{f.name}: duplicate field")
                seen_fields.add(f.name)
                if f.type not in FIELD_TYPES:
                    errors.append(f"{e.name}.{f.name}: unknown type '{f.type}'")
                if f.type == "pk":
                    has_pk = True
                if f.type == "fk" and f.target and f.target not in seen_entities and system.entity(f.target) is None:
                    errors.append(f"{e.name}.{f.name}: fk target '{f.target}' not defined")
                if f.type == "enum" and not f.values:
                    errors.append(f"{e.name}.{f.name}: enum needs 'values'")
                if f.type == "enum" and f.default is not None and str(f.default) not in f.values:
                    errors.append(f"{e.name}.{f.name}: default '{f.default}' not in enum values")
            if not has_pk:
                errors.append(f"{e.name}: missing a pk field")

    # --- workflows ---
    for w in system.workflows:
        if system.entity(w.entity) is None:
            errors.append(f"workflow {w.code}: entity '{w.entity}' not defined")
        names = {s["name"] for s in w.states}
        if not names:
            errors.append(f"workflow {w.code}: no states")
        if w.initial not in names:
            errors.append(f"workflow {w.code}: initial '{w.initial}' not a state")
        for t in w.transitions:
            if t.from_state not in names:
                errors.append(f"workflow {w.code}: transition from '{t.from_state}' not a state")
            if t.to_state not in names:
                errors.append(f"workflow {w.code}: transition to '{t.to_state}' not a state")
        finals = {s["name"] for s in w.states if s["final"]}
        reachable: set[str] = {w.initial}

        def walk(state: str) -> None:
            for t in w.transitions:
                if t.from_state == state and t.to_state not in reachable:
                    reachable.add(t.to_state)
                    walk(t.to_state)

        walk(w.initial)
        for n in sorted(names - reachable):
            errors.append(f"workflow {w.code}: state '{n}' unreachable from initial")
        for n in sorted(reachable - finals):
            if not any(t.to_state != n for t in w.transitions if t.from_state == n):
                errors.append(f"workflow {w.code}: state '{n}' is a dead end (not final, no outgoing)")

    # --- rbac ---
    from .loader import derived_functions

    eff_functions: dict[str, set[str]] = {}
    for m in system.modules:
        codes = {f["code"] for f in m.functions}
        for d in system.domains:
            if d.code == m.domain:
                codes.update(f["code"] for e in d.entities for f in derived_functions(e))
        eff_functions[m.code] = codes

    seen_roles: set[str] = set()
    for r in system.roles:
        if not CODE_RE.match(r.code):
            errors.append(f"role code not snake_case: {r.code}")
        if r.code in seen_roles:
            errors.append(f"duplicate role code: {r.code}")
        seen_roles.add(r.code)
        for mod, fns in r.grants.items():
            if mod not in eff_functions:
                errors.append(f"role {r.code}: grant references unknown module '{mod}'")
                continue
            if fns == "*":
                continue
            for fn in fns:
                if fn not in eff_functions[mod]:
                    errors.append(f"role {r.code}: module '{mod}' has no function '{fn}'")

    # module domains should exist
    for m in system.modules:
        if m.domain and m.domain not in {d.code for d in system.domains}:
            errors.append(f"module {m.code}: unknown domain '{m.domain}'")

    return errors
