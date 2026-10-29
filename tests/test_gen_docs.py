from erp_spec_forge.gen_docs import generate_data_dictionary, generate_workflows_md


def test_data_dictionary_covers_all_domains(system):
    md = generate_data_dictionary(system)
    for d in system.domains:
        assert f"## {d.name}（{d.code}）" in md
    assert "### 供应商 `supplier`" in md
    assert "FK·bigint→goods" in md
    assert "enum：company/retail" in md


def test_workflow_mermaid_and_table(system):
    md = generate_workflows_md(system)
    assert "stateDiagram-v2" in md
    assert "draft --> released : release" in md
    assert "delivering --> signed : sign" in md
    assert "pending_review --> posted : review_pass" in md
    assert "| 事件 | 从 | 到 | 角色 |" in md
