from erp_spec_forge.gen_openapi import generate_openapi


def test_openapi_paths_and_schemas(system):
    doc = generate_openapi(system)
    assert doc["openapi"] == "3.1.0"
    assert len(doc["components"]["schemas"]) == 46
    # 每个实体两个 path：集合 + /{id}
    assert len(doc["paths"]) == 92
    ops = sum(len(v) for v in doc["paths"].values())
    assert ops == 230  # 46 实体 × 5 个 CRUD 动作


def test_openapi_crud_verbs(system):
    doc = generate_openapi(system)
    order = doc["paths"]["/sales_orders"]
    assert set(order.keys()) == {"get", "post"}
    item = doc["paths"]["/sales_orders/{id}"]
    assert set(item.keys()) == {"get", "put", "delete"}


def test_openapi_envelope_and_enum(system):
    doc = generate_openapi(system)
    resp = doc["paths"]["/customers"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
    assert resp["properties"]["data"]["type"] == "array"
    props = doc["components"]["schemas"]["customer"]["properties"]
    assert props["client_type"]["enum"] == ["company", "retail"]
    assert props["code"]["description"]


def test_openapi_required_fields(system):
    doc = generate_openapi(system)
    schema = doc["components"]["schemas"]["sales_order"]
    assert "order_no" in schema["required"]
    assert "customer_id" in schema["required"]
    assert "id" not in schema["required"]
