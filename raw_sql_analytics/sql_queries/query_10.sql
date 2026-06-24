-- Список курсів, які певному студенту читає певний викладач

SELECT 
	DISTINCT d.discipline_name, 
	CONCAT(s.first_name,' ', s.last_name) as student_name, 
	CONCAT(t.first_name, ' ', t.last_name) as teacher_name
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN disciplines d ON d.id = g.discipline_id 
JOIN teachers t ON t.id = d.teacher_id 
WHERE g.student_id = ? AND d.teacher_id = ?;