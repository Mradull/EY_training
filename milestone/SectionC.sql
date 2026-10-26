SELECT * FROM parts WHERE category = 'Mechanical';
=============================================================================================
SELECT * FROM parts WHERE unit_price >1000 ORDER BY unit_price DESC;
=============================================================================================
SELECT category ,AVG(unit_price) AS average_unit_price FROM parts group by category;
=============================================================================================
SELECT category ,SUM(stock_qty) AS total_stock_quantity FROM parts group by category;
=============================================================================================
SELECT 
	po.po_id,
	s.supplier_name,
	po.order_date,
	po.status
FROM purchase_orders po
JOIN suppliers s
ON po.supplier_id = s.supplier_id;
=============================================================================================
SELECT 
	po.po_id,
  p.part_name,
  poi.quantity,
  p.unit_price
FROM purchase_orders po
JOIN purchase_order_items poi
ON po.po_id = poi.po_id
JOIN parts p
ON poi.part_id = p.part_id;
=============================================================================================
SELECT 
  po.po_id,
  p.part_name,
  poi.quantity,
  p.unit_price,
  poi.quantity * p.unit_price AS line_total
FROM purchase_orders po
JOIN purchase_order_items poi
ON po.po_id = poi.po_id
JOIN parts p
ON poi.part_id = p.part_id;

=============================================================================================
SELECT 
  s.supplier_id,
  s.supplier_name,
  po.po_id,
  po.order_date,
  po.status
FROM suppliers s
LEFT JOIN purchase_orders po
ON s.supplier_id = po.supplier_id;

=============================================================================================

SELECT 
  s.supplier_id,
  s.supplier_name
FROM suppliers s
LEFT JOIN purchase_orders po
ON s.supplier_id = po.supplier_id
WHERE po.po_id IS NULL;
=============================================================================================
  CREATE VIEW purchase_order_summary AS
SELECT 
  po.po_id,
  s.supplier_name,
  p.part_name,
  poi.quantity,
  p.unit_price,
  (poi.quantity * p.unit_price) AS line_total,
  po.status
FROM purchase_orders po
JOIN suppliers s
	ON po.supplier_id = s.supplier_id
JOIN purchase_order_items poi
ON po.po_id = poi.po_id
JOIN parts p 
ON poi.part_id = p.part_id;

=============================================================================================
  CREATE OR REPLACE FUNCTION calculate_part_discount(amount NUMERIC)
RETURNS NUMERIC AS
$$
BEGIN
    IF amount >= 2000 THEN
        RETURN amount * 0.10;
    ELSE
        RETURN 0;
    END IF;
END;
$$
LANGUAGE plpgsql;


=============================================================================================
  CREATE OR REPLACE FUNCTION final_part_price(amount NUMERIC)
RETURNS NUMERIC AS
$$
BEGIN
    RETURN amount - calculate_part_discount(amount);
END;
$$
LANGUAGE plpgsql;

SELECT
    part_id,
    part_name,
    unit_price,
    calculate_part_discount(unit_price) AS discount,
    final_part_price(unit_price) AS final_price
FROM parts;

=============================================================================================
  CREATE OR REPLACE PROCEDURE update_po_status(
    p_po_id INT,
    p_new_status VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE purchase_orders
    SET status = p_new_status
    WHERE po_id = p_po_id;
END;
$$;

CALL update_po_status(1, 'Received');


=============================================================================================
CREATE OR REPLACE PROCEDURE mark_old_pending_orders()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE purchase_orders
    SET status = 'Received'
    WHERE status = 'Pending'
      AND order_date < '2026-10-04';
END;
$$;

CALL mark_old_pending_orders();

SELECT *
FROM purchase_orders
WHERE order_date < '2026-10-04';
=============================================================================================
# supplier name and city is repeated for every order from supplier also part information is repeated
  to normalize the data i will seperate it into multiple table 

=============================================================================================


