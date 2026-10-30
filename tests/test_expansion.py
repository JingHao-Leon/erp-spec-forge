"""Entity-level convention switches (lockable / auditable) — injected at load time."""
import re

from erp_spec_forge.gen_sql import generate_sql


def test_lockable_injects_triple(system):
    supplier = system.entity("supplier")
    assert supplier.lockable
    names = {f.name for f in supplier.fields}
    assert {"status", "lock_operator", "lock_time"} <= names
    status = next(f for f in supplier.fields if f.name == "status")
    assert status.values == ["normal", "locked"]


def test_lockable_not_set_keeps_hand_written_status(system):
    goods = system.entity("goods")
    assert not goods.lockable
    status = next(f for f in goods.fields if f.name == "status")
    assert status.values == ["normal", "stopped"]  # 手写枚举不受影响


def test_auditable_injects_missing_only(system):
    so = system.entity("sales_order")  # 手写已有 created_at
    assert so.auditable
    names = [f.name for f in so.fields]
    assert names.count("created_at") == 1  # 不重复注入
    assert "created_by" in names and "updated_at" in names


def test_lockable_count_in_example_specs(system):
    lockable = [e.name for e in system.entities if e.lockable]
    assert sorted(lockable) == ["buyer", "carrier", "customer", "driver", "supplier", "warehouse"]
    auditable = [e.name for e in system.entities if e.auditable]
    assert sorted(auditable) == ["purchase_task", "sales_order", "settle_sheet", "stock_in", "stock_out"]


def test_sql_emits_lock_columns_and_check(system):
    sql = generate_sql(system)
    supplier_block = sql.split("CREATE TABLE `supplier` (")[1].split(") ENGINE")[0]
    assert "`status` VARCHAR(32)" in supplier_block
    assert "CHECK (`status` IN ('normal', 'locked'))" in supplier_block
    assert "lock_operator" in supplier_block and "lock_time" in supplier_block


def test_sql_auditable_columns(system):
    sql = generate_sql(system)
    so_block = sql.split("CREATE TABLE `sales_order` (")[1].split(") ENGINE")[0]
    assert "created_by" in so_block and "updated_at" in so_block
    assert len(re.findall(r"`created_at`", so_block)) == 1


def test_external_code_sync_field(system):
    for name in ("customer", "supplier"):
        e = system.entity(name)
        assert any(f.name == "external_code" for f in e.fields), f"{name} missing external_code"
