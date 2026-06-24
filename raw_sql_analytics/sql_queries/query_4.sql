-- Знайти середній бал на потоці (по всій таблиці оцінок).

SELECT ROUND(AVG(g.grade), 2) as average_grade
FROM grades g;

-- SELECT COUNT(DISTINCT g.student_id) as quantity_of_students, AVG(g.grade) as average_grade
-- FROM grades g; другий варіант із кількістю студентів на потоці


