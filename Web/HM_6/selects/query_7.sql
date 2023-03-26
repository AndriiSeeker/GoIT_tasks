-- 7. Знайти оцінки студентів у окремій групі з певного предмета.
SELECT sb.full_name, gr.grade, s.full_name, g.name
FROM groups g 
LEFT JOIN students s ON s.group_id = g.id 
LEFT JOIN grades gr ON gr.student_id = s.id 
LEFT JOIN subjects sb ON sb.id = gr.subject_id 
WHERE sb.id = 2 AND g.id = 2
ORDER BY  g.id, s.full_name;