DELETE FROM ${catalog}.${database}.store_returns
WHERE sr_item_sk = ${sr_item_sk} AND sr_ticket_number = ${sr_ticket_number};
