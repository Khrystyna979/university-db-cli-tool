-- Знайти студента із найвищим середнім балом з певного предмета.

SELECT 
    g.student_id, 
    s.first_name, 
    s.last_name, 
    g.discipline_id,
    ROUND(AVG(g.grade), 2) as highest_average_grade
FROM grades g
JOIN students s ON s.id = g.student_id 
WHERE g.discipline_id = ?
GROUP BY g.student_id, s.first_name, s.last_name, g.discipline_id
ORDER BY highest_average_grade DESC 
LIMIT 1;