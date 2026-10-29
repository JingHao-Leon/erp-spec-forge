# 生鲜供应链 ERP（示例规格） 数据字典

> 由 erp-spec-forge 从 YAML 规格生成。每个实体即一张表，字段含类型/必填/默认值/说明。

## 基础主数据（base_data）

商品、分类、单位、税率、区域等全系统共用的主数据。

### 商品分类 `goods_category`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `parent_id` | FK·bigint→goods_category | 否 |  | 上级分类，一级分类为空 |
| `level` | int | 是 |  | 层级 1/2/3 |
| `name` | varchar(64) | 是 |  | 分类名称 |
| `sort` | int | 否 | 0 | 排序号 |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 计量单位 `unit`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(32) | 是 |  | 单位名称，如 斤/箱/份 |
| `sort` | int | 否 | 0 |  |

### 税率 `tax_rate`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(64) | 是 |  | 税率名称 |
| `rate` | decimal(5,2) | 是 |  | 百分比数值 |

### 商品（SPU） `goods`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(128) | 是 |  | 商品名称 |
| `category_id` | FK·bigint→goods_category | 是 |  |  |
| `unit_id` | FK·bigint→unit | 是 |  |  |
| `tax_rate_id` | FK·bigint→tax_rate | 否 |  | 适用税率 |
| `alias` | varchar(128) | 否 |  | 别名，用于客户下单时匹配 |
| `spec` | varchar(64) | 否 |  | 规格，如 500g/袋 |
| `status` | enum：normal/stopped | 否 | normal | 启用状态 |
| `remark` | varchar(255) | 否 |  |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 商品 SKU `goods_sku`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `sku_name` | varchar(128) | 是 |  | SKU 名称 |
| `barcode` | varchar(64) | 否 |  | 条码 |
| `price` | decimal(12,2) | 否 |  | 参考售价 |
| `status` | enum：normal/stopped | 否 | normal |  |

### 区域 `region`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(64) | 是 |  |  |
| `parent_id` | FK·bigint→region | 否 |  | 上级区域 |
| `sort` | int | 否 | 0 |  |

## 采购管理（procurement）

供应商、采购员、报价与采购任务/单据的完整采购链路。

### 供应商 `supplier`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(128) | 是 |  | 供应商名称 |
| `contact_name` | varchar(64) | 否 |  |  |
| `contact_phone` | varchar(32) | 否 |  |  |
| `address` | varchar(255) | 否 |  |  |
| `settle_type` | enum：month/half_month/cash | 否 | month | 结算周期 |
| `status` | enum：normal/locked | 否 | normal | 启用/禁用 |
| `lock_operator` | varchar(64) | 否 |  | 禁用操作人 |
| `lock_time` | datetime | 否 |  | 禁用时间 |
| `remark` | varchar(255) | 否 |  |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 采购员 `buyer`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(64) | 是 |  |  |
| `phone` | varchar(32) | 否 |  |  |
| `group_tag` | enum：fresh/dry | 否 | fresh | 生鲜组/干货组 |
| `status` | enum：normal/locked | 否 | normal |  |

### 供应商-商品绑定 `supplier_goods`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `supplier_id` | FK·bigint→supplier | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `supply_price` | decimal(12,2) | 否 |  | 供货价 |
| `is_primary` | bool | 否 | 0 | 是否主供应商 |

### 供应商报价单 `supplier_price_sheet`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `sheet_no` | varchar(32) | 是 |  | 报价单号 |
| `supplier_id` | FK·bigint→supplier | 是 |  |  |
| `sheet_date` | date | 是 |  | 报价日期 |
| `status` | enum：draft/submitted/approved/rejected | 否 | draft |  |

### 报价明细 `supplier_price_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `sheet_id` | FK·bigint→supplier_price_sheet | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `price` | decimal(12,2) | 是 |  |  |

### 采购任务 `purchase_task`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `task_no` | varchar(32) | 是 |  | 任务单号 |
| `delivery_date` | date | 是 |  | 配送日期 |
| `task_type` | enum：fresh/dry | 否 | fresh | 生鲜/干货导单流程 |
| `status` | enum：draft/released/executing/completed/cancelled | 否 | draft | 生命周期见 workflow |
| `released_at` | datetime | 否 |  | 发布时间 |
| `released_by` | varchar(64) | 否 |  |  |
| `remark` | varchar(255) | 否 |  |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 采购任务明细 `purchase_task_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `task_id` | FK·bigint→purchase_task | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `plan_qty` | decimal(12,2) | 否 |  | 需求数量（汇总自销售订单） |
| `actual_qty` | decimal(12,2) | 否 |  | 实采数量 |
| `supplier_id` | FK·bigint→supplier | 否 |  | 指定供应商 |
| `buyer_id` | FK·bigint→buyer | 否 |  | 指定采购员 |
| `purchase_remark` | varchar(255) | 否 |  | 采购说明/加工要求 |

### 供应商比例分配 `goods_supply_ratio`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `supplier_id` | FK·bigint→supplier | 是 |  |  |
| `delivery_date` | date | 是 |  | 生效配送日期 |
| `ratio` | decimal(5,2) | 是 |  | 分配百分比 |

## 销售管理（sales）

B2B 客户档案与销售订单。

### 客户 `customer`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `code` | varchar(32) | 是 |  | 客户编号，如 C000000001 |
| `external_code` | varchar(64) | 否 |  | 外部平台客户编号（同步用） |
| `name` | varchar(128) | 是 |  | 客户名称 |
| `client_type` | enum：company/retail | 否 | company | 企业客户/零售客户 |
| `contact_name` | varchar(64) | 否 |  |  |
| `contact_phone` | varchar(32) | 否 |  |  |
| `address` | varchar(255) | 否 |  | 收货地址 |
| `region_id` | FK·bigint→region | 否 |  |  |
| `pay_type` | enum：pay_first/pay_later | 否 | pay_later | 先款/先货 |
| `pay_cycle` | enum：day/week/month | 否 | month |  |
| `account_manager` | varchar(64) | 否 |  | 客户经理 |
| `api_key` | varchar(64) | 否 |  | 对外下单 API 凭证 |
| `status` | enum：normal/locked | 否 | normal |  |
| `remark` | varchar(255) | 否 |  |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 销售订单 `sales_order`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `order_no` | varchar(32) | 是 |  | 订单号 |
| `customer_id` | FK·bigint→customer | 是 |  |  |
| `delivery_date` | date | 是 |  | 配送日期 |
| `total_amount` | decimal(12,2) | 否 | 0 |  |
| `source` | enum：manual/api/miniapp/import | 否 | manual | 订单来源 |
| `status` | enum：draft/confirmed/sorting/delivering/signed/cancelled | 否 | draft | 生命周期见 workflow |
| `remark` | varchar(255) | 否 |  |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 订单明细 `sales_order_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `order_id` | FK·bigint→sales_order | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `qty` | decimal(12,2) | 是 |  |  |
| `price` | decimal(12,2) | 是 |  |  |
| `process_requirement` | varchar(255) | 否 |  | 加工要求，如 去皮/切块 |
| `item_remark` | varchar(255) | 否 |  |  |

## 库存管理（inventory）

入库、出库、盘点、报损与库存调整。

### 仓库 `warehouse`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(64) | 是 |  |  |
| `address` | varchar(255) | 否 |  |  |
| `status` | enum：normal/stopped | 否 | normal |  |

### 入库单 `stock_in`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `in_no` | varchar(32) | 是 |  |  |
| `warehouse_id` | FK·bigint→warehouse | 是 |  |  |
| `supplier_id` | FK·bigint→supplier | 否 |  | 采购入库时的供应商 |
| `in_type` | enum：purchase/return/adjust/other | 否 | purchase |  |
| `status` | enum：draft/pending_review/posted/rejected | 否 | draft |  |
| `total_amount` | decimal(12,2) | 否 | 0 |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 入库明细 `stock_in_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `stock_in_id` | FK·bigint→stock_in | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `qty` | decimal(12,2) | 是 |  |  |
| `price` | decimal(12,2) | 是 |  |  |
| `batch_no` | varchar(64) | 否 |  | 关联溯源批次号 |

### 出库单 `stock_out`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `out_no` | varchar(32) | 是 |  |  |
| `warehouse_id` | FK·bigint→warehouse | 是 |  |  |
| `customer_id` | FK·bigint→customer | 否 |  | 销售出库时的客户 |
| `out_type` | enum：sale/purchase_return/adjust/other | 否 | sale |  |
| `status` | enum：draft/pending_review/posted/rejected | 否 | draft |  |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 出库明细 `stock_out_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `stock_out_id` | FK·bigint→stock_out | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `qty` | decimal(12,2) | 是 |  |  |
| `price` | decimal(12,2) | 是 |  |  |
| `batch_no` | varchar(64) | 否 |  |  |

### 盘点单 `stocktake`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `warehouse_id` | FK·bigint→warehouse | 是 |  |  |
| `take_date` | date | 是 |  |  |
| `status` | enum：draft/counting/submitted/posted | 否 | draft |  |

### 盘点明细 `stocktake_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `stocktake_id` | FK·bigint→stocktake | 是 |  |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `book_qty` | decimal(12,2) | 否 |  | 账面数量 |
| `actual_qty` | decimal(12,2) | 否 |  | 实盘数量 |

### 库存调整 `stock_adjust`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `adjust_no` | varchar(32) | 是 |  |  |
| `warehouse_id` | FK·bigint→warehouse | 是 |  |  |
| `adjust_type` | enum：loss/waste/gain | 否 | loss | 报损/损耗/盘盈 |
| `reason` | varchar(255) | 否 |  |  |
| `status` | enum：draft/posted | 否 | draft |  |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `qty` | decimal(12,2) | 是 |  |  |

## 配送管理（delivery）

路线、承运商、司机、GPS 冷链设备与配送执行记录。

### 承运商 `carrier`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(128) | 是 |  |  |
| `phone` | varchar(32) | 否 |  |  |
| `status` | enum：normal/locked | 否 | normal |  |

### 司机 `driver`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(64) | 是 |  |  |
| `phone` | varchar(32) | 是 |  |  |
| `carrier_id` | FK·bigint→carrier | 是 |  |  |
| `id_card_no` | varchar(32) | 否 |  | 身份证号（加密存储） |
| `status` | enum：normal/locked | 否 | normal |  |

### 配送路线 `route`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `name` | varchar(64) | 是 |  |  |
| `route_type` | enum：breakfast/vegetable/meat/dry | 否 | vegetable |  |
| `carrier_id` | FK·bigint→carrier | 是 |  |  |
| `distance_km` | decimal(8,2) | 否 |  | 路线里程 |
| `status` | enum：normal/locked | 否 | normal |  |

### 路线绑定 `route_bind`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `route_id` | FK·bigint→route | 是 |  |  |
| `customer_id` | FK·bigint→customer | 是 |  |  |
| `driver_id` | FK·bigint→driver | 是 |  |  |
| `vehicle_no` | varchar(16) | 否 |  | 车牌号 |
| `gps_device_id` | FK·bigint→gps_device | 否 |  | 绑定 GPS 设备 |
| `sort` | int | 否 | 0 | 送达顺序 |

### GPS 设备 `gps_device`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `device_no` | varchar(32) | 是 |  | 设备号 |
| `plate_no` | varchar(16) | 否 |  | 绑定车牌 |
| `device_status` | enum：normal/offline/disabled | 否 | normal |  |
| `last_login_time` | datetime | 否 |  |  |

### GPS 报警 `gps_alarm`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `device_id` | FK·bigint→gps_device | 是 |  |  |
| `alarm_type` | enum：track_deviation/temperature/late/out_of_area/into_forbidden | 是 |  |  |
| `alarm_date` | date | 是 |  |  |
| `content` | varchar(255) | 否 |  | 报警内容 |
| `handled` | bool | 否 | 0 |  |

### 配送执行记录 `delivery_record`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `route_id` | FK·bigint→route | 是 |  |  |
| `delivery_date` | date | 是 |  |  |
| `customer_id` | FK·bigint→customer | 是 |  |  |
| `driver_id` | FK·bigint→driver | 是 |  |  |
| `arrive_time` | datetime | 否 |  | 送达时间 |
| `mileage_km` | decimal(8,2) | 否 |  | 本段里程 |
| `sign_status` | enum：pending/signed/refused | 否 | pending |  |

## 结算管理（settlement）

客户对账单、收款与供应商应付。

### 对账单 `settle_sheet`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `sheet_no` | varchar(32) | 是 |  |  |
| `customer_id` | FK·bigint→customer | 是 |  |  |
| `period_start` | date | 是 |  | 账期起 |
| `period_end` | date | 是 |  | 账期止 |
| `total_amount` | decimal(12,2) | 否 | 0 |  |
| `status` | enum：draft/confirmed/partial_paid/paid | 否 | draft |  |

### 对账明细 `settle_item`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `sheet_id` | FK·bigint→settle_sheet | 是 |  |  |
| `order_id` | FK·bigint→sales_order | 是 |  |  |
| `amount` | decimal(12,2) | 是 |  |  |

### 收款记录 `payment_record`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `customer_id` | FK·bigint→customer | 是 |  |  |
| `settle_sheet_id` | FK·bigint→settle_sheet | 否 |  | 关联对账单 |
| `amount` | decimal(12,2) | 是 |  |  |
| `pay_method` | enum：cash/bank/wechat/alipay | 否 | bank |  |
| `pay_time` | datetime | 否 |  |  |
| `status` | enum：pending/success/failed | 否 | pending |  |

### 供应商应付 `supplier_payable`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `supplier_id` | FK·bigint→supplier | 是 |  |  |
| `period_start` | date | 是 |  |  |
| `period_end` | date | 是 |  |  |
| `amount` | decimal(12,2) | 否 | 0 |  |
| `status` | enum：open/paid | 否 | open |  |

## 溯源管理（traceability）

食品安全溯源：批次、检测报告与公开扫码页配置。

### 溯源批次 `trace_batch`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `batch_no` | varchar(64) | 是 |  | 批次号 |
| `goods_id` | FK·bigint→goods | 是 |  |  |
| `supplier_id` | FK·bigint→supplier | 是 |  |  |
| `production_date` | date | 否 |  | 生产/采摘日期 |
| `in_date` | date | 否 |  | 入库日期 |
| `source_place` | varchar(128) | 否 |  | 产地 |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 检测报告 `inspect_report`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `report_no` | varchar(64) | 是 |  |  |
| `batch_id` | FK·bigint→trace_batch | 是 |  |  |
| `report_date` | date | 是 |  |  |
| `result` | enum：pending/pass/fail | 否 | pending |  |
| `items_json` | json | 否 |  | 检测项与数值 |
| `report_images` | json | 否 |  | 报告图片 URL 列表 |

### 溯源公开页设置 `trace_setting`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `show_client` | bool | 否 | 1 | 公开页是否展示客户 |
| `show_buy_num` | bool | 否 | 0 | 是否展示购买数量 |
| `show_node_time` | bool | 否 | 1 | 是否展示流转时间 |
| `qr_prefix` | varchar(128) | 否 |  | 扫码页 URL 前缀 |

## 系统管理（system_admin）

管理员、模块/功能注册表、角色、系统参数与操作日志。

### 管理员 `admin_user`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `username` | varchar(64) | 是 |  | 登录名（手机号/账号） |
| `name` | varchar(64) | 否 |  | 姓名 |
| `phone` | varchar(32) | 否 |  |  |
| `password_hash` | varchar(128) | 是 |  | 口令哈希（bcrypt/argon2） |
| `role_id` | FK·bigint→sys_role | 是 |  |  |
| `status` | enum：active/disabled | 否 | active |  |
| `created_by` | varchar(64) | 否 |  | 创建人 |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |

### 功能模块 `sys_module`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `code` | varchar(64) | 是 |  | 模块代码 |
| `name` | varchar(64) | 是 |  |  |
| `parent_id` | FK·bigint→sys_module | 否 |  | 父级模块 |
| `sort` | int | 否 | 0 |  |

### 功能点 `sys_function`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `module_id` | FK·bigint→sys_module | 是 |  |  |
| `code` | varchar(64) | 是 |  | 功能码 |
| `name` | varchar(64) | 是 |  |  |

### 角色 `sys_role`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `code` | varchar(64) | 是 |  |  |
| `name` | varchar(64) | 是 |  |  |
| `descr` | varchar(255) | 否 |  |  |

### 角色授权 `sys_role_grant`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `role_id` | FK·bigint→sys_role | 是 |  |  |
| `function_code` | varchar(64) | 是 |  | 授权的功能码 |

### 系统参数 `sys_config`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `config_key` | varchar(64) | 是 |  | 参数键 |
| `config_value` | varchar(255) | 否 |  | 参数值（敏感值须加密存储） |
| `description` | varchar(255) | 否 |  |  |

### 操作日志 `operation_log`

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `id` | PK·bigint | 否 |  |  |
| `user_id` | FK·bigint→admin_user | 是 |  |  |
| `action` | varchar(64) | 是 |  | 动作，如 login/update/delete |
| `target_table` | varchar(64) | 否 |  |  |
| `target_id` | varchar(64) | 否 |  |  |
| `detail_json` | json | 否 |  | 变更前后快照 |
| `created_at` | datetime | 否 | CURRENT_TIMESTAMP |  |
