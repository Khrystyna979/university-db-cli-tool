-- Знайти оцінки студентів у окремій групі з певного предмета.

SELECT 
    d.discipline_name, 
    g2.group_name, 
    g.student_id, 
    CONCAT(s.first_name, ' ', s.last_name) as student_name, 
    g.grade
FROM grades g 
JOIN disciplines d ON d.id = g.discipline_id
JOIN students s ON s.id = g.student_id 
JOIN groups g2 ON g2.id = s.group_id 
WHERE d.id = ? AND g2.id  = ?
ORDER BY student_name;