-- 9. Знайти список курсів, які відвідує студент.
SELECT s.full_name, sb.full_name 
FROM students s 
LEFT JOIN grades g ON s.id = g.student_id 
LEFT JOIN subjects sb ON sb.id = g.subject_id 
WHERE s.id = 5
GROUP BY s.id, sb.id  
ORDER BY s.full_name;