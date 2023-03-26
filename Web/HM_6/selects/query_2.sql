-- 2. Знайти студента із найвищим середнім балом з певного предмета.
SELECT sb.full_name, s.id,  s.full_name, ROUND(AVG(g.grade), 2) as average
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id  
LEFT JOIN subjects sb ON sb.id = g.subject_id
WHERE subject_id = 1
GROUP BY sb.id;