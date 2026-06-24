-- Середній бал, який певний викладач ставить певному студентові.

SELECT 
	CONCAT(s.first_name, ' ', s.last_name) as student_name,
	CONCAT(t.first_name, ' ', t.last_name) as teacher_name,
	ROUND(AVG(g.grade), 2) as average_grade
FROM grades g 
JOIN disciplines d ON d.id = g.discipline_id 
JOIN students s ON s.id = g.student_id
JOIN teachers t ON t.id = d.teacher_id
WHERE g.student_id = 20 AND d.teacher_id = 5;