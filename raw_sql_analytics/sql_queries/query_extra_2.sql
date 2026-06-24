-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT 
	g.grade, 
	g.student_id, 
	CONCAT(s.first_name, ' ', s.last_name) as student_name,
	g.created_at as last_lesson, 
	d.discipline_name, 
	g2.group_name
FROM grades g
JOIN students s ON s.id = g.student_id
JOIN disciplines d ON d.id = g.discipline_id 
JOIN groups g2 ON g2.id = s.group_id 
WHERE g.discipline_id = 2
	AND s.group_id = 2
 	AND g.created_at = (
 		SELECT MAX(created_at) 
 		FROM grades 
 		WHERE g.discipline_id = 2
 		);