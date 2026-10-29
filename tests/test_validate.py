from erp_spec_forge.validate import validate


def test_bundled_specs_are_valid(system):
    errors = validate(system)
    assert errors == [], "bundled specs must validate clean, got: %s" % errors


def test_counts(system):
    assert len(system.domains) == 8
    assert len(system.entities) == 46
    assert len(system.workflows) == 3
    assert len(system.roles) == 9
    assert len(system.modules) == 8


def test_duplicate_entity_detected(tmp_path):
    (tmp_path / "erp.yaml").write_text(
        "spec_version: t\nsystem: {name: t, display: t}\ndomains: [a, b]\n", encoding="utf-8"
    )
    for code in ("a", "b"):
        (tmp_path / "domains").mkdir(exist_ok=True)
        (tmp_path / "domains" / f"{code}.yaml").write_text(
            f"domain: {code}\nname: {code}\nentities:\n  - name: dup\n    display: d\n"
            "    fields:\n      - {name: id, type: pk}\n",
            encoding="utf-8",
        )
    from erp_spec_forge.loader import load

    errors = validate(load(tmp_path))
    assert any("duplicate entity 'dup'" in e for e in errors)


def test_broken_fk_and_enum_detected(tmp_path):
    (tmp_path / "erp.yaml").write_text(
        "spec_version: t\nsystem: {name: t, display: t}\ndomains: [a]\n", encoding="utf-8"
    )
    (tmp_path / "domains").mkdir()
    (tmp_path / "domains" / "a.yaml").write_text(
        "domain: a\nname: a\nentities:\n"
        "  - name: thing\n    display: t\n"
        "    fields:\n"
        "      - {name: id, type: pk}\n"
        "      - {name: other_id, type: fk, target: no_such_entity}\n"
        "      - {name: state, type: enum, values: [], default: x}\n",
        encoding="utf-8",
    )
    from erp_spec_forge.loader import load

    errors = validate(load(tmp_path))
    assert any("fk target 'no_such_entity'" in e for e in errors)
    assert any("enum needs 'values'" in e for e in errors)
    assert any("default 'x' not in enum" in e for e in errors)


def test_unreachable_state_detected(system):
    # 复制一个正常 workflow，插入孤立状态后应报 unreachable
    from erp_spec_forge.loader import System, Workflow, Transition, Domain

    w = Workflow(
        code="w1",
        entity="goods",
        display="w",
        initial="s1",
        states=[{"name": "s1", "display": "s1", "final": False}, {"name": "s2", "display": "s2", "final": True}, {"name": "orphan", "display": "o", "final": False}],
        transitions=[Transition("s1", "s2", "go")],
    )
    d = Domain(code="base_data", name="bd", description="", entities=list(system.entities))
    s2 = System(name=system.name, display=system.display, description="", dialect="mysql8",
                spec_version="t", domains=[d], workflows=[w], modules=system.modules, roles=[])
    errors = validate(s2)
    assert any("unreachable" in e and "orphan" in e for e in errors)


def test_role_grant_unknown_function_detected(system):
    from erp_spec_forge.loader import Role

    bad = Role(code="bad_role", name="x", description="", grants={"procurement": ["no_such_fn"]})
    from dataclasses import replace

    s2 = replace(system, roles=system.roles + [bad])
    errors = validate(s2)
    assert any("no function 'no_such_fn'" in e for e in errors)
