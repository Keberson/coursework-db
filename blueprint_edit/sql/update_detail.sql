UPDATE detail
SET name = '$detail_name', material = '$detail_material', weight = '$detail_weight', price = '$detail_price',
    quantity_available = '$detail_quantity', date_update = NOW()
    where id_detail = '$id_detail'