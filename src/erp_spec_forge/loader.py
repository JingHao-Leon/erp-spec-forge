"""Load and model the spec tree: erp.yaml + domains/*.yaml + rbac.yaml + workflows/*.yaml."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

FIELD_TYPES = {"pk", "fk", "string", "text", "int", "decimal", "bool", "date", "datetime", "enum", "json"}
CRUD_ACTIONS = ["list", "get", "create", "update", "delete"]


@dataclass
class Field:
    name: str
    type: str
    display: str = ""
    required: bool = False
    default: str | int | None = None
    values: list[str] = field(default_factory=list)  # enum
    target: str = ""  # fk target entity
    length: int = 0  # string length
    precision: tuple[int, int] = (12, 2)  # decimal
    comment: str = ""


@dataclass
class Entity:
    name: str
    display: str
    domain: str
    fields: list[Field]
    comment: str = ""
    lockable: bool = False
    auditable: bool = False


@dataclass
class Domain:
    code: str
    name: str
    description: str
    entities: list[Entity]


@dataclass
class Transition:
    from_state: str
    to_state: str
    event: str
    role: str = ""
    guard: str = ""


@dataclass
class Workflow:
    code: str
    entity: str
    display: str
    initial: str
    states: list[dict]  # {name, display, final}
    transitions: list[Transition]


@dataclass
class Module:
    code: str
    name: str
    domain: str
    functions: list[dict]  # {code, name}


@dataclass
class Role:
    code: str
    name: str
    description: str
    grants: dict[str, object]  # module_code -> "*" | [function codes]


@dataclass
class System:
    name: str
    display: str
    description: str
    dialect: str
    spec_version: str
    domains: list[Domain]
    workflows: list[Workflow]
    modules: list[Module]
    roles: list[Role]

    @property
    def entities(self) -> list[Entity]:
        return [e for d in self.domains for e in d.entities]

    def entity(self, name: str) -> Entity | None:
        return next((e for e in self.entities if e.name == name), None)


def _field(raw: dict) -> Field:
    f = Field(
        name=str(raw["name"]),
        type=str(raw["type"]),
        display=str(raw.get("display", "")),
        required=bool(raw.get("required", False)),
        default=raw.get("default"),
        values=[str(v) for v in raw.get("values", [])],
        target=str(raw.get("target", "")),
        length=int(raw.get("length", 0) or 0),
        comment=str(raw.get("comment", "")),
    )
    if f.type == "decimal" and "precision" in raw:
        p = str(raw["precision"]).split(",")
        f.precision = (int(p[0]), int(p[1]))
    return f


def _expand_flags(e: Entity) -> Entity:
    """Inject convention fields for entity-level switches (lockable / auditable).

    Hand-written fields with the same name win; only missing ones are appended.
    """
    names = {f.name for f in e.fields}
    if e.lockable:
        for f in (
            Field(name="status", type="enum", values=["normal", "locked"], default="normal", comment="状态（lockable 自动派生）"),
            Field(name="lock_operator", type="string", length=64, comment="禁用操作人（lockable 自动派生）"),
            Field(name="lock_time", type="datetime", comment="禁用时间（lockable 自动派生）"),
        ):
            if f.name not in names:
                e.fields.append(f)
                names.add(f.name)
    if e.auditable:
        for f in (
            Field(name="created_at", type="datetime", default="CURRENT_TIMESTAMP", comment="创建时间（auditable 自动派生）"),
            Field(name="created_by", type="string", length=64, comment="创建人（auditable 自动派生）"),
            Field(name="updated_at", type="datetime", comment="更新时间（auditable 自动派生）"),
        ):
            if f.name not in names:
                e.fields.append(f)
                names.add(f.name)
    return e


def _entity(raw: dict, domain: str) -> Entity:
    return _expand_flags(
        Entity(
            name=str(raw["name"]),
            display=str(raw.get("display", raw["name"])),
            domain=domain,
            fields=[_field(f) for f in raw.get("fields", [])],
            comment=str(raw.get("comment", "")),
            lockable=bool(raw.get("lockable", False)),
            auditable=bool(raw.get("auditable", False)),
        )
    )


def load(specs_dir: str | Path) -> System:
    root = Path(specs_dir)
    erp = yaml.safe_load((root / "erp.yaml").read_text(encoding="utf-8"))

    domains: list[Domain] = []
    for code in erp.get("domains", []):
        dpath = root / "domains" / f"{code}.yaml"
        if not dpath.exists():
            raise FileNotFoundError(f"domain file missing: {dpath}")
        d = yaml.safe_load(dpath.read_text(encoding="utf-8"))
        domains.append(
            Domain(
                code=str(d.get("domain", code)),
                name=str(d.get("name", code)),
                description=str(d.get("description", "")),
                entities=[_entity(e, d.get("domain", code)) for e in d.get("entities", [])],
            )
        )

    workflows: list[Workflow] = []
    wdir = root / "workflows"
    if wdir.exists():
        for wpath in sorted(wdir.glob("*.yaml")):
            w = yaml.safe_load(wpath.read_text(encoding="utf-8"))
            workflows.append(
                Workflow(
                    code=str(w["workflow"]),
                    entity=str(w.get("entity", "")),
                    display=str(w.get("display", w["workflow"])),
                    initial=str(w["initial"]),
                    states=[{"name": str(s["name"]), "display": str(s.get("display", s["name"])), "final": bool(s.get("final", False))} for s in w.get("states", [])],
                    transitions=[
                        Transition(
                            from_state=str(t["from"]),
                            to_state=str(t["to"]),
                            event=str(t["event"]),
                            role=str(t.get("role", "")),
                            guard=str(t.get("guard", "")),
                        )
                        for t in w.get("transitions", [])
                    ],
                )
            )

    modules: list[Module] = []
    roles: list[Role] = []
    rbpath = root / erp.get("rbac_file", "rbac.yaml")
    if rbpath.exists():
        rb = yaml.safe_load(rbpath.read_text(encoding="utf-8"))
        for m in rb.get("modules", []):
            fns = [{"code": str(f["code"]), "name": str(f.get("name", f["code"]))} for f in m.get("functions", [])]
            modules.append(Module(code=str(m["code"]), name=str(m.get("name", m["code"])), domain=str(m.get("domain", "")), functions=fns))
        for r in rb.get("roles", []):
            grants = {str(k): (v if v == "*" else [str(x) for x in v]) for k, v in (r.get("grants") or {}).items()}
            roles.append(Role(code=str(r["code"]), name=str(r.get("name", r["code"])), description=str(r.get("description", "")), grants=grants))

    return System(
        name=str(erp["system"]["name"]),
        display=str(erp["system"].get("display", erp["system"]["name"])),
        description=str(erp["system"].get("description", "")),
        dialect=str(erp["system"].get("dialect", "mysql8")),
        spec_version=str(erp.get("spec_version", "0.0")),
        domains=domains,
        workflows=workflows,
        modules=modules,
        roles=roles,
    )


def derived_functions(entity: Entity) -> list[dict]:
    """Standard CRUD function codes derived from an entity (the verb convention)."""
    return [{"code": f"{entity.name}_{a}", "name": f"{entity.display}·{a}"} for a in CRUD_ACTIONS]
