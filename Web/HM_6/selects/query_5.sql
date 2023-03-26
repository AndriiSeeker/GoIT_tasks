-- 5. Знайти які курси читає певний викладач.
SELECT s.full_name, t.full_name 
FROM subjects s 
LEFT JOIN teachers t ON t.id = s.teacher_id 
ORDER BY t.full_name;