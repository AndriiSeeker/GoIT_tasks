-- 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT s.full_name, ROUND(AVG(g.grade), 2) as average
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id 
GROUP BY s.full_name 
ORDER BY average DESC 
LIMIT 5;