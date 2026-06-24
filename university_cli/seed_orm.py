from db_config import Session
from sqlalchemy.orm import Session as SQLSession
import faker
from random import randint, choice
from datetime import datetime
from sqlalchemy import select
from models import Group, Student, Teacher, Discipline, Grade

session: SQLSession = Session()

DISCIPLINES = [
        "Higher Mathematics", "Discrete Mathematics", "Fundamentals of Programming",
        "Databases", "Algorithms and Data Structures", "System Administration",
        "Probability Theory", "English Language"
    ]

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20 

fake_data = faker.Faker()

def seed_groups():
    for i in range(1, NUMBER_GROUPS + 1):
        group = Group(group_name=f"PY-{i}")
        session.add(group)
    session.commit()
    
def seed_teachers():
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(first_name=fake_data.first_name(), last_name=fake_data.last_name())
        session.add(teacher)
    session.commit()
    
def seed_disciplines():
    teacher_ids = session.scalars(select(Teacher.id)).all()
    for i, discipline in enumerate(DISCIPLINES):
        if i < len(teacher_ids):
            t_id = teacher_ids[i]
        else:
            t_id = choice(teacher_ids) 
        session.add(Discipline(discipline_name=discipline, teacher_id=t_id))
    session.commit()
    
def seed_students():
    group_ids = session.scalars(select(Group.id)).all()
    for _ in range(1, NUMBER_STUDENTS + 1):
        student = Student(first_name=fake_data.first_name(), last_name=fake_data.last_name(), group_id=choice(group_ids))
        session.add(student)
    session.commit()
    
def seed_grades():
    """
    Add grade for each student from each discipline in result every student has at least 8 grades, 
    than randomly add grades for ranfom student from random discipline, at the end max amount of grades in one student is 20 grades 
    """
    student_ids = session.scalars(select(Student.id)).all()
    discipline_ids = session.scalars(select(Discipline.id)).all()
    grades_to_add = []
    
    for s_id in student_ids:

        for d_id in discipline_ids:
            grades_to_add.append(Grade(
                student_id=s_id, 
                discipline_id=d_id, 
                grade=randint(1, 100), 
                created_at=datetime(2025, 12, randint(10, 20)).date()
            ))

        max_extra_grades = max(0, NUMBER_GRADES - len(discipline_ids))
        extra_grades_count = randint(0, max_extra_grades)
        
        for _ in range(extra_grades_count):
            grades_to_add.append(Grade(
                student_id=s_id, 
                discipline_id=choice(discipline_ids), 
                grade=randint(1, 100), 
                created_at=datetime(2025, 12, randint(10, 20)).date()
            ))
            
    session.add_all(grades_to_add)
    session.commit()

if __name__ == '__main__':
    try:
        seed_groups()
        seed_teachers()
        seed_disciplines()
        seed_students()
        seed_grades()
        print("База даних успішно наповнена!")
    except Exception as e:
        print(f"Помилка при заповненні: {e}")
        session.rollback()
    finally:
        session.close()
    
