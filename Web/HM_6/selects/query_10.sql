-- 10. Список курсів, які певному студенту читає певний викладач.
SELECT s.full_name, sb.full_name, t.full_name 
FROM students s 
LEFT JOIN grades g ON s.id = g.student_id 
LEFT JOIN subjects sb ON sb.id = g.subject_id 
LEFT JOIN teachers t ON t.id = sb.teacher_id 
WHERE s.id = 27
GROUP BY s.id, sb.id  
ORDER BY s.full_name;