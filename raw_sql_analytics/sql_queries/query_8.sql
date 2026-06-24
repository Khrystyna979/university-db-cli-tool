-- Знайти середній бал, який ставить певний викладач зі своїх предметів.

SELECT 
	CONCAT(t.first_name, ' ', t.last_name) as teacher_name, 
	g.discipline_id, 
	d.discipline_name, 
	ROUND(AVG(g.grade), 2) as discipline_average_grade
FROM grades g
JOIN disciplines d ON d.id = g.discipline_id 
JOIN teachers t ON t.id = d.teacher_id 
WHERE d.teacher_id = 2
GROUP BY 
	g.discipline_id, 
	d.teacher_id, 
	teacher_name, 
	d.discipline_name;