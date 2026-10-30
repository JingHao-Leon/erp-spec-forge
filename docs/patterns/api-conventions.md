# API 命名约定：动词功能码与 REST 路径的同构

> 同样提炼自两套真实生产系统的授权逆向（已匿名化）：一套采用 `<动词><实体>.do` 的 RPC 风格，一套采用 `/资源/子资源/动作` 的 REST 风格。两者在功能覆盖上完全同构。

## 1. 实体 CRUD 的五种动词

| 语义 | RPC 风格（老派） | REST 风格（现代） | erp-spec-forge 功能码 |
|---|---|---|---|
| 分页查询 | `ajaxPaging<实体>.do` | `GET /<实体复数>?page=&page_size=&keyword=` | `<entity>_list` |
| 查详情 | `ajaxGet<实体>ById.do` | `GET /<实体复数>/{id}` | `<entity>_get` |
| 新建 | `ajaxAdd<实体>.do` | `POST /<实体复数>` | `<entity>_create` |
| 更新 | `ajaxUpdate<实体>.do` | `PUT /<实体复数>/{id}` | `<entity>_update` |
| 删除 | `ajaxDelete<实体>.do` | `DELETE /<实体复数>/{id}` | `<entity>_delete` |

**结论**：无论底层风格如何，实体级权限面收敛为这 5 个动词。erp-spec-forge 据此把功能码推导为 `<entity>_<action>`（每实体 5 个），角色授权只需引用这些码。

## 2. 超越 CRUD 的端点族

真实系统在 CRUD 之外还有四类高频端点族，建议在 API 设计中预留：

1. **状态切换**：`change<X>LockStatus` / `set_status` —— 对应状态机事件，权限上独立于 update
2. **批量导入/导出**：`import<X>` / `exportExcel<X>` / `download<X>Template` —— Excel 模板下载、导入、按搜索条件导出三件套
3. **枚举/字典**：`ajaxGet<X>EnumDataMap` —— 前端下拉框一次性拉取某实体的枚举与关联字典
4. **备注与审计**：`update<X>Remark`、操作日志查询 —— 备注更新独立授权（客服可用，操作员不可）

## 3. 统一响应包络

两套系统都用三层包络（细节字段名不同，结构一致）：

```json
{ "code": 0, "msg": "ok", "data": { ... } }
```

- `code`：0 = 成功，非 0 为业务错误码（区别于 HTTP 层错误）
- `msg`：人类可读消息，前端 toast 直接展示
- `data`：单对象或 `{page: {rowCount, currPage, totalPage, pageSize}, list: [...]}` 分页结构

erp-spec-forge 的 OpenAPI 生成器为每个端点输出该包络（`_envelope`），分页端点的 `data` 为数组。

## 4. 分页与检索约定

- 请求：`page`（1 起）、`page_size`（默认 20）、`keyword`（模糊检索）
- 响应：`page.rowCount` 总数 + `list` 当前页
- 高频过滤器上浮为显式参数（如日期、状态、外键 id），低频的进 `keyword`

## 5. 对规格使用者的建议

1. 新端点先问"这属于哪个实体的哪个动词？"——是则用功能码，否则注册自定义功能码（如 `purchase_task_release`）
2. 状态切换端点的权限码与 `update` 分离——"能改单据"不等于"能推动状态"
3. 导入导出与备注更新同样独立授权
4. 所有写端点记操作日志（示例规格 `operation_log` 实体）
