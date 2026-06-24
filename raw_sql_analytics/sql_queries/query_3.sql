-- Знайти середній бал у групах з певного предмета.

SELECT s.group_id, 
	g2.group_name,
	g.discipline_id, 
	d.discipline_name, 
	ROUND(AVG(g.grade), 2) as average_grade
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN groups g2  ON g2.id = s.group_id 
JOIN disciplines d ON d.id = g.discipline_id 
WHERE g.discipline_id = ?
GROUP BY 
	s.group_id, 
	g2.group_name, 
	g.discipline_id, 
	d.discipline_name;

