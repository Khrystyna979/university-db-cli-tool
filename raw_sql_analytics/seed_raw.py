from datetime import datetime
import faker
from random import randint
import sqlite3

DISCIPLINES = [
        "Higher Mathematics", "Discrete Mathematics", "Fundamentals of Programming",
        "Databases", "Algorithms and Data Structures", "System Administration",
        "Probability Theory", "English Language"
    ]

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20 


def generate_fake_data(number_teachers, number_groups, number_students, number_grades, disciplines) -> tuple:
    fake_teachers = []
    fake_groups = []
    fake_students = []
    fake_disciplines = []
    fake_grades = []
    
    fake_data = faker.Faker()
    number_disciplines = len(disciplines)
    
    for _ in range(number_teachers): 
        fake_teachers.append((fake_data.first_name(), fake_data.last_name()))

    for i in range(1, number_groups + 1):
        fake_groups.append((f"PY-{i}",))
        
    for _ in range(number_students):
        fake_students.append((fake_data.first_name(), fake_data.last_name(), randint(1, number_groups )))
        
        
    for i in range(number_disciplines):
        if i < number_teachers:
            fake_disciplines.append((disciplines[i], i + 1))
        else:
            fake_disciplines.append((disciplines[i], randint(1, number_teachers)))
        
        
    for student_id in range(1, number_students + 1):
        
    # Add grade for each student from each discipline, in result every student has at least 8 grades(we have 8 disciplines), 
    # than randomly add grades for ranfom student from random discipline, at the end max amount of grades for one student is 20 grades
        
        for discipline_id in range(1, number_disciplines + 1):
            fake_grades.append((
                student_id, 
                discipline_id, 
                randint(0, 100), 
                datetime(2025, 12, randint(10, 20)).date() # Imagine that grades was received in the end of 2025 session
            ))
        max_extra_grades = max(0, number_grades - number_disciplines)
        
        for _ in range(randint(0, max_extra_grades)):
            fake_grades.append((
                student_id, 
                randint(1, number_disciplines), 
                randint(0, 100), 
                datetime(2025, 12, randint(10, 20)).date()
            ))
            
    return fake_teachers, fake_groups, fake_students, fake_disciplines, fake_grades

def insert_data_to_db(teachers, groups, students, disciplines, grades) -> None:
    
    with sqlite3.connect('university.db') as con:

        cur = con.cursor()
        
        sql_to_teachers = """INSERT INTO teachers(first_name, last_name) VALUES (?, ?)"""
        cur.executemany(sql_to_teachers, teachers)
        
        sql_to_groups = """INSERT INTO groups(group_name) VALUES (?)"""
        cur.executemany(sql_to_groups, groups)
        
        sql_to_students = """INSERT INTO students(first_name, last_name, group_id) VALUES (?, ?, ?)"""
        cur.executemany(sql_to_students, students)
        
        sql_to_disciplines = """INSERT INTO disciplines(discipline_name, teacher_id) VALUES (?, ?)"""
        cur.executemany(sql_to_disciplines, disciplines)
        
        sql_to_grades = """INSERT INTO grades(student_id, discipline_id, grade, created_at) VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_grades, grades)
        
        
if __name__ == "__main__":
    
    insert_data_to_db(*generate_fake_data(
            NUMBER_TEACHERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_GRADES, disciplines=DISCIPLINES
        ))