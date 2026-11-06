SELECT * FROM c
SELECT c.station_name, c.city,c.status from c
SELECT c.station_name, c.capacity_kw,c.daily_sessions, c.revenue from c
SELECT c.id ,c.station_name FROM c 
SELECT * FROM c WHERE c.city = "Hyderabad"
SELECT * FROM c WHERE c.city = "Mumbai"
SELECT * FROM c WHERE c.status = "Maintenance"
SELECT * FROM c WHERE c.station_type = "Fast"
SELECT * FROM c WHERE c.connector_type = "CCS2"
SELECT * FROM c WHERE c.capacity_kw > 100
SELECT * FROM c WHERE c.revenue > 15000
SELECT * FROM c WHERE c.daily_sessions > 40
SELECT * FROM c WHERE c.uptime_percent < 96
SELECT * FROM c WHERE c.capacity_kw BETWEEN 50 AND 120
SELECT * FROM c WHERE c.revenue < 10000
SELECT * FROM c WHERE c.station_type = "Fast" AND c.status = "Active";
SELECT * FROM c WHERE c.city = "Hyderabad" AND c.revenue > 10000;
SELECT * FROM c WHERE c.capacity_kw > 100 AND c.daily_sessions > 40;
SELECT * FROM c WHERE c.status = "Active" AND c.uptime_percent > 97;
SELECT * FROM c WHERE c.station_type = "Standard" AND c.revenue < 10000;
SELECT * FROM c WHERE c.station_type = "Fast" AND c.status = "Active"
SELECT * FROM c WHERE c.city = "Hyderabad" AND c.revenue > 10000
SELECT * FROM c WHERE c.capacity_kw > 100 AND c.daily_sessions > 40
SELECT * FROM c WHERE c.status = "Active" AND c.uptime_percent > 97
SELECT * FROM c WHERE c.station_type = "Standard" AND c.revenue < 10000
SELECT * FROM c WHERE c.station_type = "Fast" AND c.status = "Active"
SELECT * FROM c WHERE c.city = "Hyderabad" AND c.revenue > 10000
SELECT * FROM c WHERE c.capacity_kw > 100 AND c.daily_sessions > 40
SELECT * FROM c WHERE c.status = "Active" AND c.uptime_percent > 97
SELECT * FROM c WHERE c.station_type = "Standard" AND c.revenue < 10000
SELECT VALUE COUNT(1) FROM c
SELECT VALUE COUNT(1) FROM c WHERE c.status = "Active"
SELECT VALUE COUNT(1) FROM c WHERE c.station_type = "Fast"
SELECT VALUE COUNT(1) FROM c WHERE c.city = "Pune"
SELECT VALUE COUNT(1) FROM c WHERE c.revenue > 15000
SELECT c.city, COUNT(1) AS total_stations FROM c GROUP BY c.city
SELECT c.station_type, COUNT(1) AS total_stations FROM c GROUP BY c.station_type
SELECT c.status, COUNT(1) AS total_stations FROM c GROUP BY c.status
SELECT c.city, SUM(c.revenue) AS total_revenue FROM c GROUP BY c.city
SELECT c.station_type, AVG(c.revenue) AS avg_revenue FROM c GROUP BY c.station_type
SELECT c.city, AVG(c.uptime_percent) AS avg_uptime FROM c GROUP BY c.city
SELECT c.city, SUM(c.daily_sessions) AS total_daily_sessions FROM c GROUP BY c.city
SELECT c.station_type, AVG(c.capacity_kw) AS avg_capacity FROM c GROUP BY c.station
SELECT c.city,SUM(c.revenue) AS total_revenue FROM c WHERE c.status="Active" GROUP BY c.city
SELECT c.city,COUNT(1) AS fast_station_count FROM c WHERE c.station_type="Fast" GROUP BY c.city
SELECT c.city,AVG(c.revenue) AS avg_revenue FROM c WHERE c.revenue>8000 GROUP BY c.city
SELECT c.station_type,SUM(c.daily_sessions) AS total_daily_sessions FROM c GROUP BY c.station_type
SELECT TOP 5 c.station_name,c.revenue FROM c ORDER BY c.revenue DESC
SELECT TOP 3 c.station_name,c.daily_sessions FROM c ORDER BY c.daily_sessions DESC
SELECT * FROM c WHERE c.station_type="Fast" AND c.status="Active" ORDER BY c.revenue DESC
SELECT * FROM c WHERE c.revenue>12000 AND c.uptime_percent>97 ORDER BY c.revenue DESC
SELECT * FROM c WHERE (c.city="Hyderabad" OR c.city="Bengaluru") AND c.daily_sessions>30
SELECT * FROM c WHERE c.status="Maintenance" ORDER BY c.uptime_percent ASC
SELECT c.station_name,c.city,c.revenue,c.uptime_percent FROM c WHERE c.revenue>15000
SELECT * FROM c WHERE c.station_type="Fast" AND c.capacity_kw>=120 ORDER BY c.capacity_kw DESC
SELECT TOP 1 c.city,SUM(c.revenue) AS total_revenue FROM c GROUP BY c.city ORDER BY total_revenue DESC
SELECT TOP 1 c.station_name,c.revenue FROM c ORDER BY c.revenue DESC
SELECT TOP 1 c.station_name,c.uptime_percent FROM c ORDER BY c.uptime_percent ASC
SELECT TOP 1 c.station_type,AVG(c.revenue) AS avg_revenue FROM c GROUP BY c.station_type ORDER BY avg_revenue DESC
SELECT TOP 1 c.city,SUM(c.daily_sessions) AS total_sessions FROM c GROUP BY c.city ORDER BY total_sessions DESC
SELECT VALUE COUNT(1) FROM c WHERE c.status = "Maintenance"
