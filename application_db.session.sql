SELECT r.*, s.name, DATE_FORMAT(CONVERT_TZ(r.created, 'UTC', 'America/New_York'), '%Y-%m-%d %H:%i:%s')
FROM climatemonitor_reading r
    INNER JOIN climatemonitor_sensor s ON r.sensor_id = s.id
ORDER BY r.id desc;


select count(*) from climatemonitor_reading;
