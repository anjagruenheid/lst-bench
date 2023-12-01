DELETE FROM ${catalog}.${database}.inventory
WHERE inv_date_sk = ${inv_date_sk} AND inv_item_sk = ${inv_item_sk} AND inv_warehouse_sk = ${inv_warehouse_sk};
