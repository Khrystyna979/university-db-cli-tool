-- Знайти список курсів, які відвідує студент.

SELECT 
	DISTINCT d.discipline_name as attended_disciplines, 
	CONCAT(s.first_name, ' ', s.last_name) as student_name
FROM grades g
JOIN disciplines d ON d.id = g.discipline_id 
JOIN students s ON s.id = g.student_id 
WHERE g.student_id = ?;
