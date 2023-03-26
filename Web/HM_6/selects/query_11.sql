-- 11. Середній бал, який певний викладач ставить певному студентові.
SELECT st.full_name, ROUND(AVG(g.grade), 2), t.full_name
FROM grades g 
LEFT JOIN subjects s ON s.id = g.subject_id 
LEFT JOIN teachers t ON t.id = s.teacher_id 
LEFT JOIN students st ON st.id = g.student_id 
WHERE st.id = 28 AND t.id = 3;