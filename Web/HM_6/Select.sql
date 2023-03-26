-- 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT s.full_name, ROUND(AVG(g.grade), 2) as average
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id 
GROUP BY s.full_name 
ORDER BY average DESC 
LIMIT 5;

-- 2. Знайти студента із найвищим середнім балом з певного предмета.
SELECT sb.full_name, s.id,  s.full_name, ROUND(AVG(g.grade), 2) as average
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id  
LEFT JOIN subjects sb ON sb.id = g.subject_id
WHERE subject_id = 1
GROUP BY sb.id;

-- 3. Знайти середній бал у групах з певного предмета.
SELECT sb.full_name, gr.name , ROUND(AVG(g.grade), 2) as average
FROM grades g 
LEFT JOIN students s ON s.id = g.student_id  
LEFT JOIN subjects sb ON sb.id = g.subject_id
LEFT JOIN [groups] gr ON gr.id = s.group_id 
WHERE subject_id = 2
GROUP BY gr.id 
ORDER BY average DESC;

-- 4. Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT ROUND(AVG(g.grade), 2)
FROM grades g;

-- 5. Знайти які курси читає певний викладач.
SELECT s.full_name, t.full_name 
FROM subjects s 
LEFT JOIN teachers t ON t.id = s.teacher_id 
ORDER BY t.full_name 

-- 6. Знайти список студентів у певній групі.
SELECT g.name, s.full_name 
FROM groups g 
LEFT JOIN students s ON s.group_id = g.id 
ORDER BY  g.id, s.full_name

-- 7. Знайти оцінки студентів у окремій групі з певного предмета.
SELECT sb.full_name, gr.grade, s.full_name, g.name
FROM groups g 
LEFT JOIN students s ON s.group_id = g.id 
LEFT JOIN grades gr ON gr.student_id = s.id 
LEFT JOIN subjects sb ON sb.id = gr.subject_id 
WHERE sb.id = 2 AND g.id = 2
ORDER BY  g.id, s.full_name

-- 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT ROUND(AVG(g.grade), 2)
FROM grades g 
LEFR JOIN