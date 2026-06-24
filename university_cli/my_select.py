from sqlalchemy import func, desc, select, distinct

from db_config import Session
from models import Group, Student, Teacher, Discipline, Grade
from sqlalchemy.orm import Session as SQLSession

session: SQLSession = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    stmt = (
        select(
            Grade.student_id, 
            Student.first_name, 
            Student.last_name, 
            func.round(func.avg(Grade.grade), 2).label('average_grade'))
        .select_from(Grade)
        .join(Student)
        .group_by(Grade.student_id, Student.first_name, Student.last_name).order_by(desc('average_grade'))
        .limit(5)
    )
    
    result = session.execute(stmt).all()
    return result

def select_2(discipline_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета.
    """
    stmt = (
        select(
            Grade.student_id, 
            Student.first_name, 
            Student.last_name, 
            Grade.discipline_id, 
            func.round(func.avg(Grade.grade), 2)
        .label('highest_average_grade')).select_from(Grade)
        .join(Student)
        .where(Grade.discipline_id==discipline_id)
        .group_by(Grade.student_id, Student.first_name, Student.last_name, Grade.discipline_id)
        .order_by(desc('highest_average_grade'))
        .limit(1)
    )
        
    result = session.execute(stmt).one_or_none()
    return result
    
def select_3(discipline_id: int):
    """Знайти середній бал у групах з певного предмета.
    """
    stmt = (
        select(
            Student.group_id, 
            Group.group_name, 
            Grade.discipline_id, 
            func.round(func.avg(Grade.grade), 2)
        .label('average_grade'))
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .where(Grade.discipline_id==discipline_id)
        .group_by(Student.group_id, Group.group_name, Grade.discipline_id)
    )
    result = session.execute(stmt).all()
    return result

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    stmt = select(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade)
    result = session.execute(stmt).scalar()
    return result

def select_5(teacher_id):
    """Знайти які курси читає певний викладач.
    """
    stmt = (
        select(
            Discipline.teacher_id, 
            func.concat(Teacher.first_name, ' ', Teacher.last_name).label('teacher_name'), 
            Discipline.discipline_name)
        .select_from(Discipline)
        .join(Teacher)
        .where(Discipline.teacher_id==teacher_id)
    )
    result = session.execute(stmt).all()
    return result

def select_6(group_id):
    """Знайти список студентів у певній групі.
    """
    stmt = (
        select(
            Group.group_name, 
            func.concat(Student.first_name, ' ', Student.last_name).label('student_name'), 
            Student.id)
        .select_from(Student)
        .join(Group)
        .where(Student.group_id==group_id)
    )
    result = session.execute(stmt).all()
    return result

def select_7(discipline_id, group_id):
    """Знайти оцінки студентів у окремій групі з певного предмета.
    """
    stmt = (
        select(
            Discipline.discipline_name, 
            Group.group_name, 
            Grade.student_id, 
            func.concat(Student.first_name, ' ', Student.last_name).label('student_name'), 
            Grade.grade)
        .select_from(Grade)
        .join(Discipline)
        .join(Student)
        .join(Group)
        .where(Grade.discipline_id==discipline_id, Student.group_id==group_id)
        .order_by('student_name')
    )
    
    result = session.execute(stmt).all()
    return result

def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    stmt = (
        select(
            func.concat(Teacher.first_name, ' ', Teacher.last_name).label('teacher_name'),
            Grade.discipline_id,
            Discipline.discipline_name,
            func.round(func.avg(Grade.grade), 2).label('discipline_average_grade'))
        .select_from(Grade)
        .join(Discipline)
        .join(Teacher)
        .where(Discipline.teacher_id==teacher_id)
        .group_by(Teacher.first_name, Teacher.last_name, Grade.discipline_id, Discipline.discipline_name)
    )
    result = session.execute(stmt).all()
    return result

def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент.
    """
    stmt = (
        select(
            distinct(Discipline.discipline_name).label('attended_disciplines'),
            func.concat(Student.first_name, ' ', Student.last_name).label('student_name')
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .where(Grade.student_id==student_id)
    )
    result = session.execute(stmt).all()
    return result

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач.
    """
    stmt = (
        select(
            distinct(Discipline.discipline_name),
            func.concat(Student.first_name, ' ', Student.last_name).label('student_name'),
            func.concat(Teacher.first_name, ' ', Teacher.last_name).label('teacher_name')
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Teacher)
        .where(Grade.student_id==student_id, Discipline.teacher_id==teacher_id)
    )
    result = session.execute(stmt).all()
    return result

def extra_select_1(student_id, teacher_id):
    """Середній бал, який певний викладач ставить певному студентові.
    """
    stmt = (
        select(
            func.concat(Student.first_name, ' ', Student.last_name).label('student_name'),
            func.concat(Teacher.first_name, ' ', Teacher.last_name).label('teacher_name'),
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .select_from(Grade)
        .join(Discipline)
        .join(Student)
        .join(Teacher)
        .where(Grade.student_id==student_id, Discipline.teacher_id==teacher_id)
        .group_by(Student.first_name, Student.last_name, Teacher.first_name, Teacher.last_name)
    )
    result = session.execute(stmt).all()
    return result

def extra_select_2(discipline_id, group_id):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті.
    """
    last_lesson_subq = select(func.max(Grade.created_at)).where(Grade.discipline_id==discipline_id).scalar_subquery()
    
    stmt = (
        select(
            Grade.grade,
            Grade.student_id,
            func.concat(Student.first_name, ' ', Student.last_name).label('student_name'),
            Grade.created_at.label('last_lesson'),
            Discipline.discipline_name,
            Group.group_name
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .where(Grade.discipline_id==discipline_id, Student.group_id==group_id, Grade.created_at==last_lesson_subq)
    )
    result = session.execute(stmt).all()
    return result

if __name__ == '__main__':
    print(extra_select_2(2, 2))
    
