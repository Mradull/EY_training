1. SELECT * FROM GUESTS;
--------------------------------------------------------------------------------
2. SELECT guest_name , city , membership_level FROM GUESTS;

--------------------------------------------------------------------------------
3. SELECT * from rooms WHERE price_per_night > 5000 ;

--------------------------------------------------------------------------------
4. SELECT * from rooms where status = 'Available';

--------------------------------------------------------------------------------
5. SELECT * from guests where membership_level = 'Gold';

--------------------------------------------------------------------------------
6. SELECT * from bookings where booking_status = 'Confirmed';

--------------------------------------------------------------------------------
7. SELECT * from bookings ORDER BY check_in_date ASC;

--------------------------------------------------------------------------------
8. SELECT * from rooms ORDER BY price_per_night DESC;

--------------------------------------------------------------------------------
9. SELECT * from rooms 
	  WHERE price_per_night BETWEEN 4000 and 8000;
--------------------------------------------------------------------------------
10. SELECT * from guests where city in ('Hyderabad' , 'Pune' , 'Mumbai') ;

--------------------------------------------------------------------------------
11. SELECT COUNT(*) from rooms;

--------------------------------------------------------------------------------
12. SELECT AVG(price_per_night) AS avgprice from rooms;

--------------------------------------------------------------------------------
13. SELECT * FROM rooms WHERE price_per_night = ( SELECT MAX(price_per_night) FROM rooms);

--------------------------------------------------------------------------------
14. SELECT * FROM rooms WHERE price_per_night = ( SELECT MIN(price_per_night) FROM rooms);

--------------------------------------------------------------------------------
15. SELECT room_type , COUNT(*) as room_count FROM rooms GROUP BY room_type ORDER BY room_count DESC;

--------------------------------------------------------------------------------
16. SELECT room_type , AVG(price_per_night) AS average_price FROM rooms GROUP BY room_type;

--------------------------------------------------------------------------------
17. SELECT membership_level , COUNT(*) AS total_guest FROM guests GROUP BY membership_level;

--------------------------------------------------------------------------------
18. SELECT booking_status , COUNT(*) AS booking_count FROM bookings GROUP BY booking_status;

--------------------------------------------------------------------------------
19. SELECT SUM(service_price) AS total_service_value FROM services;

--------------------------------------------------------------------------------
20. SELECT AVG(service_price) AS average_service_value FROM services;

--------------------------------------------------------------------------------
21. SELECT 
    	b.booking_id,
    	g.guest_name,
    	g.city,
    	b.check_in_date,
    	b.check_out_date,
    	b.booking_status
    
    FROM Bookings b
    JOIN Guests g
    ON b.guest_id = g.guest_id;


--------------------------------------------------------------------------------

22. SELECT 
    	b.booking_id,
    	r.room_id,
    	r.price_per_night,
    	b.check_in_date,
    	b.check_out_date
    
    FROM Bookings b
    JOIN Rooms r
    ON b.room_id = r.room_id;


--------------------------------------------------------------------------------

23. SELECT 
    	g.guest_name,
    	r.room_type,
    	r.price_per_night,
    	b.booking_status
    
    FROM Bookings b
    JOIN guests g
    	ON b.guest_id =  g.guest_id
    Join rooms r
    	ON b.room_id = r.room_id;


--------------------------------------------------------------------------------

24. SELECT 
    	b.booking_id,
    	s.service_name,
    	bs.quantity,
    	s.service_price
    
    FROM Bookings b
    JOIN booking_services bs
    	ON b.booking_id =  bs.booking_id
    Join services s
    	ON bs.service_id = s.service_id;


--------------------------------------------------------------------------------

25. SELECT 
    	bs.booking_id,
    	s.service_name,
    	bs.quantity,
    	s.service_price,
    	(bs.quantity * s.service_price) AS service_cost
    
    FROM booking_services bs
    Join services s
    	ON bs.service_id = s.service_id;


--------------------------------------------------------------------------------

26. SELECT 
    	g.guest_name,
    	b.booking_id,
    	r.room_type,
    	s.service_name,
    	bs.quantity,
    	b.booking_status
    
    FROM guests g
    JOIN bookings b
    	ON g.guest_id = b.guest_id
    JOIN rooms r
    	ON b.room_id = r.room_id
    JOIN booking_services bs
    	ON b.booking_id = bs.booking_id
    JOIN services s
    	ON bs.service_id = s.service_id;


--------------------------------------------------------------------------------

27. SELECT 
    	g.guest_name,
    	b.booking_id,
    	b.booking_status
    
    FROM guests g
    LEFT JOIN bookings b
    ON g.guest_id = b.guest_id;


--------------------------------------------------------------------------------

28. SELECT 
    	g.guest_id,
    	g.guest_name,
    	g.city
    
    FROM guests g
    LEFT JOIN bookings b
    ON g.guest_id = b.guest_id
    WHERE b.booking_id IS NULL;


--------------------------------------------------------------------------------

29. SELECT 
    	g.guest_name,
    	COUNT(b.booking_id) AS total_bookings
    
    FROM guests g
    LEFT JOIN bookings b
    ON g.guest_id = b.guest_id
    GROUP BY g.guest_id , g.guest_name
    ORDER BY total_bookings DESC;


--------------------------------------------------------------------------------

30. SELECT 
    	g.guest_name,
    	SUM(bs.quantity * s.service_price) AS total_service_cost
    
    FROM bookings b
    JOIN guests g
    	ON b.guest_id = g.guest_id
    JOIN booking_services bs
    	ON b.booking_id = bs.booking_id
    JOIN services s
    	ON bs.service_id = s.service_id
    GROUP BY 
    	b.booking_id,
    	g.guest_name
    ORDER BY total_service_cost DESC;


--------------------------------------------------------------------------------
	









