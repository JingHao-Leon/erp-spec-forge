"""Documentation generators: data dictionaries per domain, workflow state-machine docs (mermaid)."""
from __future__ import annotations

from .loader import System

_TYPE_SHOW = {
    "pk": "PK·bigint",
    "fk": "FK·bigint",
    "string": "varchar",
    "text": "text",
    "int": "int",
    "decimal": "decimal",
    "bool": "bool",
    "date": "date",
    "datetime": "datetime",
    "enum": "enum",
    "json": "json",
}


def generate_data_dictionary(system: System) -> str:
    lines = [
        f"# {system.display} 数据字典",
        "",
        "> 由 erp-spec-forge 从 YAML 规格生成。每个实体即一张表，字段含类型/必填/默认值/说明。",
        "",
    ]
    for d in system.domains:
        lines.append(f"## {d.name}（{d.code}）")
        lines.append("")
        if d.description:
            lines.append(d.description)
            lines.append("")
        for e in d.entities:
            lines.append(f"### {e.display} `{e.name}`")
            lines.append("")
            lines.append("| 字段 | 类型 | 必填 | 默认 | 说明 |")
            lines.append("|---|---|---|---|---|")
            for f in e.fields:
                t = _TYPE_SHOW[f.type]
                if f.type == "enum":
                    t += "：" + "/".join(f.values)
                if f.type == "fk":
                    t += f"→{f.target}"
                if f.type == "string" and f.length:
                    t += f"({f.length})"
                if f.type == "decimal":
                    t += f"({f.precision[0]},{f.precision[1]})"
                default = "" if f.default is None else str(f.default)
                lines.append(f"| `{f.name}` | {t} | {'是' if f.required else '否'} | {default} | {f.comment} |")
            lines.append("")
    return "\n".join(lines)


def generate_workflows_md(system: System) -> str:
    lines = ["# 单据状态机（Workflow）", "", "> 由 erp-spec-forge 生成，mermaid 可直接渲染。", ""]
    for w in system.workflows:
        lines.append(f"## {w.display}（{w.code}）— 实体 `{w.entity}`")
        lines.append("")
        lines.append("```mermaid")
        lines.append("stateDiagram-v2")
        shown: set[str] = set()
        for s in w.states:
            label = f'{s["name"]} : {s["display"]}'
            if label not in shown:
                lines.append(f"    {s['name']} : {s['display']}")
                shown.add(s["name"])
        for t in w.transitions:
            edge = f"    {t.from_state} --> {t.to_state} : {t.event}"
            if t.role:
                edge += f"\\n({t.role})"
            lines.append(edge)
        lines.append("```")
        lines.append("")
        lines.append("| 事件 | 从 | 到 | 角色 |")
        lines.append("|---|---|---|---|")
        for t in w.transitions:
            lines.append(f"| {t.event} | {t.from_state} | {t.to_state} | {t.role or '—'} |")
        lines.append("")
    return "\n".join(lines)


def generate_readme_doc(system: System) -> str:
    eff_entities = system.entities
    lines = [
        f"# {system.display}",
        "",
        system.description or "",
        "",
        f"- 规格版本：`{system.spec_version}`",
        f"- 领域数：{len(system.domains)}",
        f"- 实体数：{len(eff_entities)}",
        f"- 单据状态机：{len(system.workflows)}",
        f"- 角色：{len(system.roles)}",
        "",
        "## 领域一览",
        "",
        "| 领域 | 实体 |",
        "|---|---|",
    ]
    for d in system.domains:
        lines.append(f"| {d.name}（{d.code}） | {len(d.entities)} |")
    lines.append("")
    return "\n".join(lines)
