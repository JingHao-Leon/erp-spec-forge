# 贡献指南

感谢关注 erp-spec-forge！本项目欢迎以下类型的贡献：

## 可以做什么

1. **规格校验规则**：`src/erp_spec_forge/validate.py`，补充新的结构校验（如环形 FK 检测）
2. **生成目标**：`gen_*.py` 系列文件，新增 Prisma/Drizzle/Django models 等产物
3. **SQL 方言**：为 `gen_sql.py` 增加 PostgreSQL/SQLite 方言
4. **示例规格**：用 `specs/` 语法描述其他行业 ERP 领域（零售/餐饮/制造），作为 `examples/` 补充
5. **文档**：规格语法、最佳实践、FAQ

## 约定

- Python ≥ 3.10，运行时依赖仅 PyYAML
- 提交前请确保：`pytest -q` 全绿；新功能必须带测试
- 实体/字段/功能码命名一律 snake_case
- **不要在规格或测试中写入真实系统的表结构、接口地址或凭据**——本库只收原创泛化的领域模型

## 流程

1. Fork → 分支（`feat/xxx`）
2. 改动 + 测试
3. `pytest -q` 通过
4. PR 描述写清动机与影响面

## 环境

```bash
pip install -e ".[dev]"
pytest -q
erp-spec-forge validate --specs specs
```
