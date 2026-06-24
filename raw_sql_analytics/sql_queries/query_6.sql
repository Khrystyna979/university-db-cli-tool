-- Знайти список студентів у певній групі.

SELECT 
	g.group_name,  
	CONCAT(s.first_name, ' ', s.last_name) as student_name, 
	s.id as student_id
FROM students s 
JOIN groups g ON g.id = s.group_id 
WHERE g.id  = ?;