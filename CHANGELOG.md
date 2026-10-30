# Changelog

## 0.1.1 (2026-10-30)

真实系统逆向价值沉淀版。

- **实体级约定开关**：`lockable`（自动注入 状态/lock_operator/lock_time 锁定三件套）与 `auditable`（created_at/created_by/updated_at），手写同名字段优先、只补缺失
- 示例规格落地：6 实体 lockable（供应商/客户/采购员/承运商/司机/仓库）、5 单据 auditable；客户与供应商补 `external_code` 双轨同步字段
- **新增模式文档**（源自两套真实生产系统的授权逆向，已匿名化）：
  - `docs/patterns/domain-lessons.md` 领域结构模式 8 条（模块注册表、锁定三件套、比例分配、同步键……）
  - `docs/patterns/api-conventions.md` 动词功能码与 REST 同构、统一包络、四大端点族
  - `docs/patterns/security-hardening.md` 10 类真实反模式与规格层解法
- 测试 26 → 33 项

## 0.1.0 (2026-10-30)

首个公开版本。

- 规格语法 v0.1：根规格 / 领域实体 / RBAC / 单据状态机
- 生成器：MySQL 8 DDL、OpenAPI 3.1、RBAC 权限矩阵（md/csv）、模块注册表（json）、数据字典、状态机文档（mermaid）
- CLI：`erp-spec-forge validate` / `generate`
- 内置生鲜供应链 ERP 示例规格：8 领域 / 46 实体 / 8 模块 / 9 角色 / 3 状态机（242 功能码、92 API 路径、230 操作）
- 测试 26 项全绿
