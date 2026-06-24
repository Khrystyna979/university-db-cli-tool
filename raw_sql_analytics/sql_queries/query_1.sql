-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

SELECT g.student_id, s.first_name, s.last_name, ROUND(AVG(g.grade), 2) as average_grade
FROM grades g
JOIN students s ON s.id = g.student_id 
GROUP BY g.student_id, s.first_name, s.last_name
ORDER BY average_grade DESC 
LIMIT 5;