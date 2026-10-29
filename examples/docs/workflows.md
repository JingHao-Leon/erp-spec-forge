# 单据状态机（Workflow）

> 由 erp-spec-forge 生成，mermaid 可直接渲染。

## 采购任务生命周期（purchase_task_lifecycle）— 实体 `purchase_task`

```mermaid
stateDiagram-v2
    draft : 草稿
    released : 已发布
    executing : 采购执行中
    completed : 已完成
    cancelled : 已作废
    draft --> released : release\n(purchase_clerk)
    released --> draft : recall\n(purchase_clerk)
    released --> executing : start
    executing --> completed : complete
    draft --> cancelled : cancel
    released --> cancelled : cancel
```

| 事件 | 从 | 到 | 角色 |
|---|---|---|---|
| release | draft | released | purchase_clerk |
| recall | released | draft | purchase_clerk |
| start | released | executing | — |
| complete | executing | completed | — |
| cancel | draft | cancelled | — |
| cancel | released | cancelled | — |

## 销售订单生命周期（sales_order_lifecycle）— 实体 `sales_order`

```mermaid
stateDiagram-v2
    draft : 草稿
    confirmed : 已审核
    sorting : 分拣中
    delivering : 配送中
    signed : 已签收
    cancelled : 已取消
    draft --> confirmed : audit\n(finance)
    confirmed --> sorting : start_sorting
    sorting --> delivering : deliver
    delivering --> signed : sign
    draft --> cancelled : cancel
    confirmed --> cancelled : cancel\n(finance)
```

| 事件 | 从 | 到 | 角色 |
|---|---|---|---|
| audit | draft | confirmed | finance |
| start_sorting | confirmed | sorting | — |
| deliver | sorting | delivering | — |
| sign | delivering | signed | — |
| cancel | draft | cancelled | — |
| cancel | confirmed | cancelled | finance |

## 入库单审核流（stock_in_review）— 实体 `stock_in`

```mermaid
stateDiagram-v2
    draft : 草稿
    pending_review : 待审核
    posted : 已过账
    rejected : 已驳回
    draft --> pending_review : submit
    pending_review --> posted : review_pass\n(warehouse_keeper)
    pending_review --> rejected : review_reject\n(warehouse_keeper)
    rejected --> draft : rework
```

| 事件 | 从 | 到 | 角色 |
|---|---|---|---|
| submit | draft | pending_review | — |
| review_pass | pending_review | posted | warehouse_keeper |
| review_reject | pending_review | rejected | warehouse_keeper |
| rework | rejected | draft | — |
