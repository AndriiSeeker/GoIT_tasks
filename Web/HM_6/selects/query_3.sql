-- 3. Знайти середній бал у групах з певного предмета.
SELECT sb.full_name, gr.name , ROUND(AVG(g.grade), 2) as average
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id  
LEFT JOIN subjects sb ON sb.id = g.subject_id
LEFT JOIN [groups] gr ON gr.id = s.group_id 
WHERE subject_id = 2
GROUP BY gr.id 
ORDER BY average DESC;