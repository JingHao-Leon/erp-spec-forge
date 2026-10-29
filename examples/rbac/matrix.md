# 权限矩阵（RBAC Matrix）

> 行 = 功能码（模块内自定义 + 实体 CRUD 推导），列 = 角色，● = 授权。由 erp-spec-forge 生成。

| 功能码 | 系统管理员 | 采购主管 | 采购文员 | 分拣员 | 仓库管理员 | 配送调度 | 财务 | 溯源录入员 | 运营查看 |
|---|---|---|---|---|---|---|---|---|---|
| **基础设置（base_data）** |  |  |  |  |  |  |  |  |  |
| goods_category_list | ● | ● |  |  |  |  |  |  |  |
| goods_category_get | ● | ● |  |  |  |  |  |  |  |
| goods_category_create | ● | ● |  |  |  |  |  |  |  |
| goods_category_update | ● | ● |  |  |  |  |  |  |  |
| goods_category_delete | ● | ● |  |  |  |  |  |  |  |
| unit_list | ● | ● |  |  | ● |  |  |  |  |
| unit_get | ● | ● |  |  |  |  |  |  |  |
| unit_create | ● | ● |  |  |  |  |  |  |  |
| unit_update | ● | ● |  |  |  |  |  |  |  |
| unit_delete | ● | ● |  |  |  |  |  |  |  |
| tax_rate_list | ● | ● |  |  |  |  |  |  |  |
| tax_rate_get | ● | ● |  |  |  |  |  |  |  |
| tax_rate_create | ● | ● |  |  |  |  |  |  |  |
| tax_rate_update | ● | ● |  |  |  |  |  |  |  |
| tax_rate_delete | ● | ● |  |  |  |  |  |  |  |
| goods_list | ● | ● |  |  | ● |  |  | ● |  |
| goods_get | ● | ● |  |  | ● |  |  | ● |  |
| goods_create | ● | ● |  |  |  |  |  |  |  |
| goods_update | ● | ● |  |  |  |  |  |  |  |
| goods_delete | ● | ● |  |  |  |  |  |  |  |
| goods_sku_list | ● | ● |  |  | ● |  |  |  |  |
| goods_sku_get | ● | ● |  |  |  |  |  |  |  |
| goods_sku_create | ● | ● |  |  |  |  |  |  |  |
| goods_sku_update | ● | ● |  |  |  |  |  |  |  |
| goods_sku_delete | ● | ● |  |  |  |  |  |  |  |
| region_list | ● | ● |  |  |  |  |  |  |  |
| region_get | ● | ● |  |  |  |  |  |  |  |
| region_create | ● | ● |  |  |  |  |  |  |  |
| region_update | ● | ● |  |  |  |  |  |  |  |
| region_delete | ● | ● |  |  |  |  |  |  |  |
| **采购管理（procurement）** |  |  |  |  |  |  |  |  |  |
| purchase_task_release | ● | ● | ● |  |  |  |  |  |  |
| purchase_task_recall | ● | ● |  |  |  |  |  |  |  |
| supplier_price_approve | ● | ● |  |  |  |  |  |  |  |
| supplier_list | ● | ● | ● |  |  |  |  |  |  |
| supplier_get | ● | ● | ● |  |  |  |  |  |  |
| supplier_create | ● | ● | ● |  |  |  |  |  |  |
| supplier_update | ● | ● | ● |  |  |  |  |  |  |
| supplier_delete | ● | ● |  |  |  |  |  |  |  |
| buyer_list | ● | ● | ● |  |  |  |  |  |  |
| buyer_get | ● | ● | ● |  |  |  |  |  |  |
| buyer_create | ● | ● |  |  |  |  |  |  |  |
| buyer_update | ● | ● |  |  |  |  |  |  |  |
| buyer_delete | ● | ● |  |  |  |  |  |  |  |
| supplier_goods_list | ● | ● |  |  |  |  |  |  |  |
| supplier_goods_get | ● | ● |  |  |  |  |  |  |  |
| supplier_goods_create | ● | ● |  |  |  |  |  |  |  |
| supplier_goods_update | ● | ● |  |  |  |  |  |  |  |
| supplier_goods_delete | ● | ● |  |  |  |  |  |  |  |
| supplier_price_sheet_list | ● | ● | ● |  |  |  |  |  |  |
| supplier_price_sheet_get | ● | ● | ● |  |  |  |  |  |  |
| supplier_price_sheet_create | ● | ● | ● |  |  |  |  |  |  |
| supplier_price_sheet_update | ● | ● |  |  |  |  |  |  |  |
| supplier_price_sheet_delete | ● | ● |  |  |  |  |  |  |  |
| supplier_price_item_list | ● | ● | ● |  |  |  |  |  |  |
| supplier_price_item_get | ● | ● |  |  |  |  |  |  |  |
| supplier_price_item_create | ● | ● |  |  |  |  |  |  |  |
| supplier_price_item_update | ● | ● |  |  |  |  |  |  |  |
| supplier_price_item_delete | ● | ● |  |  |  |  |  |  |  |
| purchase_task_list | ● | ● | ● |  |  |  |  |  |  |
| purchase_task_get | ● | ● | ● |  |  |  |  |  |  |
| purchase_task_create | ● | ● | ● |  |  |  |  |  |  |
| purchase_task_update | ● | ● | ● |  |  |  |  |  |  |
| purchase_task_delete | ● | ● |  |  |  |  |  |  |  |
| purchase_task_item_list | ● | ● | ● |  |  |  |  |  |  |
| purchase_task_item_get | ● | ● |  |  |  |  |  |  |  |
| purchase_task_item_create | ● | ● |  |  |  |  |  |  |  |
| purchase_task_item_update | ● | ● |  |  |  |  |  |  |  |
| purchase_task_item_delete | ● | ● |  |  |  |  |  |  |  |
| goods_supply_ratio_list | ● | ● | ● |  |  |  |  |  |  |
| goods_supply_ratio_get | ● | ● |  |  |  |  |  |  |  |
| goods_supply_ratio_create | ● | ● |  |  |  |  |  |  |  |
| goods_supply_ratio_update | ● | ● |  |  |  |  |  |  |  |
| goods_supply_ratio_delete | ● | ● |  |  |  |  |  |  |  |
| **销售管理（sales）** |  |  |  |  |  |  |  |  |  |
| sales_order_audit | ● |  |  |  |  |  | ● |  |  |
| sales_order_edit_price | ● |  |  |  |  |  |  |  |  |
| customer_list | ● |  |  |  |  |  |  |  |  |
| customer_get | ● |  |  |  |  |  |  |  |  |
| customer_create | ● |  |  |  |  |  |  |  |  |
| customer_update | ● |  |  |  |  |  |  |  |  |
| customer_delete | ● |  |  |  |  |  |  |  |  |
| sales_order_list | ● |  |  | ● |  |  | ● |  | ● |
| sales_order_get | ● |  |  | ● |  |  | ● |  | ● |
| sales_order_create | ● |  |  |  |  |  |  |  |  |
| sales_order_update | ● |  |  |  |  |  |  |  |  |
| sales_order_delete | ● |  |  |  |  |  |  |  |  |
| sales_order_item_list | ● |  |  | ● |  |  |  |  |  |
| sales_order_item_get | ● |  |  |  |  |  |  |  |  |
| sales_order_item_create | ● |  |  |  |  |  |  |  |  |
| sales_order_item_update | ● |  |  |  |  |  |  |  |  |
| sales_order_item_delete | ● |  |  |  |  |  |  |  |  |
| **库存管理（inventory）** |  |  |  |  |  |  |  |  |  |
| stock_in_review | ● |  |  |  | ● |  | ● |  |  |
| stock_out_review | ● |  |  |  | ● |  | ● |  |  |
| warehouse_list | ● |  |  |  | ● |  |  |  |  |
| warehouse_get | ● |  |  |  | ● |  |  |  |  |
| warehouse_create | ● |  |  |  | ● |  |  |  |  |
| warehouse_update | ● |  |  |  | ● |  |  |  |  |
| warehouse_delete | ● |  |  |  | ● |  |  |  |  |
| stock_in_list | ● |  |  |  | ● |  | ● |  |  |
| stock_in_get | ● |  |  |  | ● |  | ● |  |  |
| stock_in_create | ● |  |  |  | ● |  |  |  |  |
| stock_in_update | ● |  |  |  | ● |  |  |  |  |
| stock_in_delete | ● |  |  |  | ● |  |  |  |  |
| stock_in_item_list | ● |  |  |  | ● |  |  |  |  |
| stock_in_item_get | ● |  |  |  | ● |  |  |  |  |
| stock_in_item_create | ● |  |  |  | ● |  |  |  |  |
| stock_in_item_update | ● |  |  |  | ● |  |  |  |  |
| stock_in_item_delete | ● |  |  |  | ● |  |  |  |  |
| stock_out_list | ● |  |  | ● | ● |  | ● |  |  |
| stock_out_get | ● |  |  | ● | ● |  | ● |  |  |
| stock_out_create | ● |  |  |  | ● |  |  |  |  |
| stock_out_update | ● |  |  |  | ● |  |  |  |  |
| stock_out_delete | ● |  |  |  | ● |  |  |  |  |
| stock_out_item_list | ● |  |  | ● | ● |  |  |  |  |
| stock_out_item_get | ● |  |  |  | ● |  |  |  |  |
| stock_out_item_create | ● |  |  |  | ● |  |  |  |  |
| stock_out_item_update | ● |  |  |  | ● |  |  |  |  |
| stock_out_item_delete | ● |  |  |  | ● |  |  |  |  |
| stocktake_list | ● |  |  |  | ● |  |  |  |  |
| stocktake_get | ● |  |  |  | ● |  |  |  |  |
| stocktake_create | ● |  |  |  | ● |  |  |  |  |
| stocktake_update | ● |  |  |  | ● |  |  |  |  |
| stocktake_delete | ● |  |  |  | ● |  |  |  |  |
| stocktake_item_list | ● |  |  |  | ● |  |  |  |  |
| stocktake_item_get | ● |  |  |  | ● |  |  |  |  |
| stocktake_item_create | ● |  |  |  | ● |  |  |  |  |
| stocktake_item_update | ● |  |  |  | ● |  |  |  |  |
| stocktake_item_delete | ● |  |  |  | ● |  |  |  |  |
| stock_adjust_list | ● |  |  |  | ● |  |  |  |  |
| stock_adjust_get | ● |  |  |  | ● |  |  |  |  |
| stock_adjust_create | ● |  |  |  | ● |  |  |  |  |
| stock_adjust_update | ● |  |  |  | ● |  |  |  |  |
| stock_adjust_delete | ● |  |  |  | ● |  |  |  |  |
| **配送管理（delivery）** |  |  |  |  |  |  |  |  |  |
| gps_alarm_handle | ● |  |  |  |  | ● |  |  |  |
| route_schedule | ● |  |  |  |  | ● |  |  |  |
| carrier_list | ● |  |  |  |  | ● |  |  |  |
| carrier_get | ● |  |  |  |  | ● |  |  |  |
| carrier_create | ● |  |  |  |  | ● |  |  |  |
| carrier_update | ● |  |  |  |  | ● |  |  |  |
| carrier_delete | ● |  |  |  |  | ● |  |  |  |
| driver_list | ● |  |  |  |  | ● |  |  |  |
| driver_get | ● |  |  |  |  | ● |  |  |  |
| driver_create | ● |  |  |  |  | ● |  |  |  |
| driver_update | ● |  |  |  |  | ● |  |  |  |
| driver_delete | ● |  |  |  |  | ● |  |  |  |
| route_list | ● |  |  |  |  | ● |  |  |  |
| route_get | ● |  |  |  |  | ● |  |  |  |
| route_create | ● |  |  |  |  | ● |  |  |  |
| route_update | ● |  |  |  |  | ● |  |  |  |
| route_delete | ● |  |  |  |  | ● |  |  |  |
| route_bind_list | ● |  |  |  |  | ● |  |  |  |
| route_bind_get | ● |  |  |  |  | ● |  |  |  |
| route_bind_create | ● |  |  |  |  | ● |  |  |  |
| route_bind_update | ● |  |  |  |  | ● |  |  |  |
| route_bind_delete | ● |  |  |  |  | ● |  |  |  |
| gps_device_list | ● |  |  |  |  | ● |  |  |  |
| gps_device_get | ● |  |  |  |  | ● |  |  |  |
| gps_device_create | ● |  |  |  |  | ● |  |  |  |
| gps_device_update | ● |  |  |  |  | ● |  |  |  |
| gps_device_delete | ● |  |  |  |  | ● |  |  |  |
| gps_alarm_list | ● |  |  |  |  | ● |  |  |  |
| gps_alarm_get | ● |  |  |  |  | ● |  |  |  |
| gps_alarm_create | ● |  |  |  |  | ● |  |  |  |
| gps_alarm_update | ● |  |  |  |  | ● |  |  |  |
| gps_alarm_delete | ● |  |  |  |  | ● |  |  |  |
| delivery_record_list | ● |  |  |  |  | ● |  |  |  |
| delivery_record_get | ● |  |  |  |  | ● |  |  |  |
| delivery_record_create | ● |  |  |  |  | ● |  |  |  |
| delivery_record_update | ● |  |  |  |  | ● |  |  |  |
| delivery_record_delete | ● |  |  |  |  | ● |  |  |  |
| **结算管理（settlement）** |  |  |  |  |  |  |  |  |  |
| settle_sheet_confirm | ● |  |  |  |  |  | ● |  |  |
| settle_sheet_list | ● |  |  |  |  |  | ● |  | ● |
| settle_sheet_get | ● |  |  |  |  |  | ● |  | ● |
| settle_sheet_create | ● |  |  |  |  |  | ● |  |  |
| settle_sheet_update | ● |  |  |  |  |  | ● |  |  |
| settle_sheet_delete | ● |  |  |  |  |  | ● |  |  |
| settle_item_list | ● |  |  |  |  |  | ● |  |  |
| settle_item_get | ● |  |  |  |  |  | ● |  |  |
| settle_item_create | ● |  |  |  |  |  | ● |  |  |
| settle_item_update | ● |  |  |  |  |  | ● |  |  |
| settle_item_delete | ● |  |  |  |  |  | ● |  |  |
| payment_record_list | ● |  |  |  |  |  | ● |  |  |
| payment_record_get | ● |  |  |  |  |  | ● |  |  |
| payment_record_create | ● |  |  |  |  |  | ● |  |  |
| payment_record_update | ● |  |  |  |  |  | ● |  |  |
| payment_record_delete | ● |  |  |  |  |  | ● |  |  |
| supplier_payable_list | ● |  |  |  |  |  | ● |  |  |
| supplier_payable_get | ● |  |  |  |  |  | ● |  |  |
| supplier_payable_create | ● |  |  |  |  |  | ● |  |  |
| supplier_payable_update | ● |  |  |  |  |  | ● |  |  |
| supplier_payable_delete | ● |  |  |  |  |  | ● |  |  |
| **溯源管理（traceability）** |  |  |  |  |  |  |  |  |  |
| inspect_report_upload | ● |  |  |  |  |  |  | ● |  |
| trace_batch_entry | ● |  |  |  |  |  |  | ● |  |
| trace_batch_list | ● |  |  |  |  |  |  | ● |  |
| trace_batch_get | ● |  |  |  |  |  |  | ● |  |
| trace_batch_create | ● |  |  |  |  |  |  | ● |  |
| trace_batch_update | ● |  |  |  |  |  |  | ● |  |
| trace_batch_delete | ● |  |  |  |  |  |  | ● |  |
| inspect_report_list | ● |  |  |  |  |  |  | ● |  |
| inspect_report_get | ● |  |  |  |  |  |  | ● |  |
| inspect_report_create | ● |  |  |  |  |  |  | ● |  |
| inspect_report_update | ● |  |  |  |  |  |  | ● |  |
| inspect_report_delete | ● |  |  |  |  |  |  | ● |  |
| trace_setting_list | ● |  |  |  |  |  |  | ● |  |
| trace_setting_get | ● |  |  |  |  |  |  | ● |  |
| trace_setting_create | ● |  |  |  |  |  |  | ● |  |
| trace_setting_update | ● |  |  |  |  |  |  | ● |  |
| trace_setting_delete | ● |  |  |  |  |  |  | ● |  |
| **系统设置（system_admin）** |  |  |  |  |  |  |  |  |  |
| admin_user_list | ● |  |  |  |  |  |  |  |  |
| admin_user_get | ● |  |  |  |  |  |  |  |  |
| admin_user_create | ● |  |  |  |  |  |  |  |  |
| admin_user_update | ● |  |  |  |  |  |  |  |  |
| admin_user_delete | ● |  |  |  |  |  |  |  |  |
| sys_module_list | ● |  |  |  |  |  |  |  |  |
| sys_module_get | ● |  |  |  |  |  |  |  |  |
| sys_module_create | ● |  |  |  |  |  |  |  |  |
| sys_module_update | ● |  |  |  |  |  |  |  |  |
| sys_module_delete | ● |  |  |  |  |  |  |  |  |
| sys_function_list | ● |  |  |  |  |  |  |  |  |
| sys_function_get | ● |  |  |  |  |  |  |  |  |
| sys_function_create | ● |  |  |  |  |  |  |  |  |
| sys_function_update | ● |  |  |  |  |  |  |  |  |
| sys_function_delete | ● |  |  |  |  |  |  |  |  |
| sys_role_list | ● |  |  |  |  |  |  |  |  |
| sys_role_get | ● |  |  |  |  |  |  |  |  |
| sys_role_create | ● |  |  |  |  |  |  |  |  |
| sys_role_update | ● |  |  |  |  |  |  |  |  |
| sys_role_delete | ● |  |  |  |  |  |  |  |  |
| sys_role_grant_list | ● |  |  |  |  |  |  |  |  |
| sys_role_grant_get | ● |  |  |  |  |  |  |  |  |
| sys_role_grant_create | ● |  |  |  |  |  |  |  |  |
| sys_role_grant_update | ● |  |  |  |  |  |  |  |  |
| sys_role_grant_delete | ● |  |  |  |  |  |  |  |  |
| sys_config_list | ● |  |  |  |  |  |  |  |  |
| sys_config_get | ● |  |  |  |  |  |  |  |  |
| sys_config_create | ● |  |  |  |  |  |  |  |  |
| sys_config_update | ● |  |  |  |  |  |  |  |  |
| sys_config_delete | ● |  |  |  |  |  |  |  |  |
| operation_log_list | ● |  |  |  |  |  |  |  |  |
| operation_log_get | ● |  |  |  |  |  |  |  |  |
| operation_log_create | ● |  |  |  |  |  |  |  |  |
| operation_log_update | ● |  |  |  |  |  |  |  |  |
| operation_log_delete | ● |  |  |  |  |  |  |  |  |
