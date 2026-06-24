-- Знайти які курси читає певний викладач.

SELECT 
    d.teacher_id,
    CONCAT(t.first_name, ' ', t.last_name) AS teacher_name, 
    d.discipline_name
FROM disciplines d 
JOIN teachers t ON t.id = d.teacher_id 
WHERE d.teacher_id = ?;
