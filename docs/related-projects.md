# Spec-Driven 生态：致敬对象与贡献路线

erp-spec-forge 站在 spec-driven / design-first 社区的肩膀上。以下项目是本库方法论的重要参考，也是我们计划回馈贡献的方向。

## 相关优质项目

- [github/spec-kit](https://github.com/github/spec-kit) — GitHub 官方的 Spec-Driven Development 工具包（specify/plan/tasks 工作流）。erp-spec-forge 的"规格先行、产物派生"思想与之一脉相承；差异在于 spec-kit 面向通用软件需求流程，本项目面向 ERP 领域模型的结构化规格。
- [OpenAPI Initiative](https://github.com/OAI/OpenAPI-Specification) — 接口契约事实标准，本项目将其作为生成目标之一。
- [C4 Model / Structurizr](https://github.com/structurizr) — 架构即代码的代表，启发我们把"领域结构"也当作可版本化的代码。
- [AsyncAPI](https://github.com/asyncapi/spec) — 事件驱动契约，未来 ERP 领域事件（如订单状态变更事件流）可对标。
- [Prisma / Drizzle](https://github.com/prisma/prisma) — schema-as-code 在 ORM 层的实践，是后续生成目标的候选。
- [dbml (dbdiagram)](https://github.com/holistics/dbml) — 数据库标记语言，DDL 之外的另一种可交互产物形态。

## 计划中的对外贡献

1. **向 spec-kit 生态贡献 ERP 领域模板**：以 `specs/` 为基础，沉淀"领域规格模板包"，配合 spec-kit 的 specify 流程使用。
2. **OpenAPI 工具链**：为生成的 3.1 文档补充 `x-` 扩展（权限码、状态机绑定），反馈给文档渲染器生态。
3. **方言适配器**：PostgreSQL/SQLite DDL 生成器以独立 contributor 身份回馈给需要的下游。
4. **状态机互操作**：探索与 XState/ Spring Statemachine 的规格互转。

> 欢迎通过 Issue 指出更多值得对标的 spec-driven 项目。
