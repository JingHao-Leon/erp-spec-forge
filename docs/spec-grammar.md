# 规格语法（Spec Grammar v0.1）

规格树结构：

```text
specs/
├── erp.yaml            # 根规格：系统元信息 + 领域清单
├── domains/*.yaml      # 领域：实体与字段
├── rbac.yaml           # 模块（含自定义功能码）+ 角色授权
└── workflows/*.yaml    # 单据状态机
```

## 1. 根规格 `erp.yaml`

| 字段 | 必填 | 说明 |
|---|---|---|
| `spec_version` | 是 | 规格版本，进入所有产物的元信息 |
| `system.name` | 是 | 系统标识（snake_case） |
| `system.display` | 否 | 展示名 |
| `system.description` | 否 | 一句话描述，进入 OpenAPI info |
| `system.dialect` | 否 | 目标 SQL 方言，当前仅 `mysql8` |
| `domains` | 是 | 领域文件名清单，须对应 `domains/<code>.yaml` |
| `rbac_file` | 否 | 默认 `rbac.yaml` |
| `workflows_dir` | 否 | 默认 `workflows/` |

## 2. 领域与实体 `domains/*.yaml`

| 字段 | 说明 |
|---|---|
| `domain` / `name` / `description` | 领域代码（snake_case）/ 展示名 / 描述 |
| `entities[].name` | 实体名 = 表名，全系统唯一，snake_case |
| `entities[].display` | 中文展示名，进入注释与文档 |
| `entities[].fields[]` | 字段清单，见下 |

字段类型：`pk` `fk` `string` `text` `int` `decimal` `bool` `date` `datetime` `enum` `json`。

| 字段属性 | 适用类型 | 说明 |
|---|---|---|
| `required` | 全部 | NOT NULL（pk/fk） |
| `default` | 全部 | 默认值；`datetime` 支持 `CURRENT_TIMESTAMP` |
| `target` | fk | 目标实体名，必须已定义 |
| `values` | enum | 枚举取值，非空 |
| `length` | string | VARCHAR 长度，默认 255 |
| `precision` | decimal | 形如 `"12,2"` |
| `comment` | 全部 | 说明，进入 SQL 注释与数据字典 |

### 实体级约定开关（v0.1.1 新增）

| 开关 | 自动注入字段（已手写的同名字段跳过） |
|---|---|
| `lockable: true` | `status`(enum normal/locked) + `lock_operator` + `lock_time` —— 主数据"锁定三件套" |
| `auditable: true` | `created_at`(默认 CURRENT_TIMESTAMP) + `created_by` + `updated_at` |

双轨系统同步约定：与外部平台对接的客户/供应商建议声明 `external_code` 字段（string 64），作为跨系统同步键。

校验规则：实体名/字段名 snake_case 且唯一；每个实体恰有一个 `pk`；`fk.target` 必须存在；`enum.values` 非空且 `default` 必须在取值内；状态机初始态可达、无死端。

## 3. RBAC `rbac.yaml`

```yaml
modules:
  - code: procurement          # 模块代码
    name: 采购管理
    domain: procurement        # 关联领域：该领域实体的 CRUD 功能码自动并入
    functions:                 # 自定义功能码（可选）
      - {code: purchase_task_release, name: 发布采购任务}
roles:
  - code: purchase_clerk
    name: 采购文员
    grants:
      procurement: "*"         # 授权模块全部功能码
      sales: [sales_order_list, sales_order_get]   # 或显式清单
```

功能码推导规则：领域内每个实体派生 `list/get/create/update/delete` 五个功能码，即 `<entity>_<action>`。

## 4. 状态机 `workflows/*.yaml`

| 字段 | 说明 |
|---|---|
| `workflow` / `entity` / `display` | 工作流代码 / 绑定实体 / 展示名 |
| `initial` | 初始状态，必须在 `states` |
| `states[].final` | 终态标记；非终态必须有出边 |
| `transitions[].from/to/event` | 迁移三元组 |
| `transitions[].role` | 允许触发该事件的 RBAC 角色代码（可选） |
| `transitions[].guard` | 守卫条件的自然语言描述（可选，进文档） |

## 5. 版本策略

- `0.x`：语法可能调整，升级看 CHANGELOG
- 破坏性变更递增 minor，向后兼容新增递增 patch
