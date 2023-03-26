-- 6. Знайти список студентів у певній групі.
SELECT g.name, s.full_name 
FROM groups g 
LEFT JOIN students s ON s.group_id = g.id 
ORDER BY  g.id, s.full_name;