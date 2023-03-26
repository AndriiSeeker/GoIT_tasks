-- 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT st.full_name, g.grade, s.full_name, g.date_of 
FROM grades g
LEFT JOIN subjects s ON s.id = g.subject_id 
LEFT JOIN students st ON st.id = g.student_id 
LEFT JOIN groups gp ON gp.id = st.group_id 
WHERE st.id = 28 and s.id = 2
ORDER BY date_of DESC 
LIMIT 1;