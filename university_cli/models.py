from datetime import datetime, date
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.sql.sqltypes import Date

class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_name: Mapped[str] = mapped_column(String(200), nullable=False)
    students: Mapped[list['Student']] = relationship(back_populates='group')
    
    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, group_name={self.group_name!r})"

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))
    group: Mapped['Group'] = relationship(back_populates='students')
    grades: Mapped[list['Grade']] = relationship(back_populates='student')
    
    def __repr__(self) -> str:
        return f"Student(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, group_id={self.group_id!r})"
    
class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    disciplines: Mapped[list['Discipline']] = relationship(back_populates='teacher')
    
    def __repr__(self) -> str:
        return f"Teacher(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"
    
class Discipline(Base):
    __tablename__ = 'disciplines'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discipline_name: Mapped[str] = mapped_column(String(255), nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    grades: Mapped[list['Grade']] = relationship(back_populates='discipline')
    teacher: Mapped['Teacher'] = relationship(back_populates='disciplines')
    
    def __repr__(self) -> str:
        return f"Discipline(id={self.id!r}, discipline_name={self.discipline_name!r}, teacher_id={self.teacher_id!r})"
    
class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    discipline_id: Mapped[int] = mapped_column(Integer, ForeignKey('disciplines.id', ondelete='CASCADE'))
    grade: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[date] = mapped_column(Date, default=datetime.now().date)
    discipline: Mapped['Discipline'] = relationship(back_populates='grades')
    student: Mapped['Student'] = relationship(back_populates='grades')

    def __repr__(self) -> str:
        return f"Grade(id={self.id!r}, student_id={self.student_id!r}, discipline_id={self.discipline_id!r}, grade={self.grade!r}, created_at={self.created_at!r})"