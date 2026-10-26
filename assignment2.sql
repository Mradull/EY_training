1. Select * from vehicles;
-------------------------------------
2. Select * from service_bookings where service_status = 'Scheduled';
-------------------------------------------------------------------------
3. Select * from service_items where cost > 1500;
------------------------------------------------------------------------
4. Select * from technicians where specialization IN ('Battery' , 'Electrical');
--------------------------------------------------------------------------------
5. SELECT
    	c.customer_id,
    	c.customer_name,
    	c.city,
    	COUNT(v.vehicle_id) AS total_vehicles
    FROM customers c
    LEFT JOIN vehicles v
    	ON c.customer_id = v.customer_id
    GROUP BY c.customer_id , c.customer_name , c.city;
-----------------------------------------------------------------------------------
6. SELECT AVG(cost) from service_items ;
-------------------------------------------------------
7. SELECT 
    	c.customer_name,
    	v.model_name,
    	v.registration_no
    FROM customers c
    JOIN vehicles v
    ON c.customer_id = v.customer_id
-----------------------------------------------------------
8. SELECT 
    	v.vehicle_id,
    	v.model_name,
    	s.service_date,
    	s.service_status
    FROM vehicles v
    JOIN service_bookings s
    ON v.vehicle_id = s.vehicle_id
-------------------------------------------------------------------------
9. SELECT 
    	s.booking_id,
    	t.technician_name,
    	t.specialization,
    	s.service_status
    FROM service_bookings s
    JOIN technicians t
    ON s.technician_id = t.technician_id
----------------------------------------------------------------------
10. SELECT
        c.customer_name,
        v.model_name,
        t.technician_name,
        sb.service_date,
        sb.service_status
    FROM customers c
    JOIN vehicles v
        ON c.customer_id = v.customer_id
    JOIN service_bookings sb
        ON v.vehicle_id = sb.vehicle_id
    JOIN technicians t
        ON sb.technician_id = t.technician_id;
-----------------------------------------------------------------------
11. SELECT
        sb.booking_id,
        SUM(si.cost) AS total_service_cost
    FROM service_bookings sb
    JOIN service_items si
        ON sb.booking_id = si.booking_id
    GROUP BY sb.booking_id;

----------------------------------------------------------------------------------
12.
