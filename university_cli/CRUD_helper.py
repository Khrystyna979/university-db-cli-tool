from models import Group, Student, Teacher, Discipline, Grade
from db_config import Session
from sqlalchemy.orm import Session as SQLSession
from sqlalchemy import select
import argparse
import textwrap

session: SQLSession = Session()

BANNER = """
   █████████  ███████████   █████  █████ ██████████      █████   █████ ██████████ █████       ███████████  ██████████ ███████████  
  ███░░░░░███░░███░░░░░███ ░░███  ░░███ ░░███░░░░███    ░░███   ░░███ ░░███░░░░░█░░███       ░░███░░░░░███░░███░░░░░█░░███░░░░░███ 
 ███     ░░░  ░███    ░███  ░███   ░███  ░███   ░░███    ░███    ░███  ░███  █ ░  ░███        ░███    ░███ ░███  █ ░  ░███    ░███ 
░███          ░██████████   ░███   ░███  ░███    ░███    ░███████████  ░██████    ░███        ░██████████  ░██████    ░██████████  
░███          ░███░░░░░███  ░███   ░███  ░███    ░███    ░███░░░░░███  ░███░░█    ░███        ░███░░░░░░   ░███░░█    ░███░░░░░███ 
░░███     ███ ░███    ░███  ░███   ░███  ░███    ███     ░███    ░███  ░███ ░   █ ░███      █ ░███         ░███ ░   █ ░███    ░███ 
 ░░█████████  █████   █████ ░░████████   ██████████      █████   █████ ██████████ ███████████ █████        ██████████ █████   █████
  ░░░░░░░░░  ░░░░░   ░░░░░   ░░░░░░░░   ░░░░░░░░░░      ░░░░░   ░░░░░ ░░░░░░░░░░ ░░░░░░░░░░░ ░░░░░        ░░░░░░░░░░ ░░░░░   ░░░░░ 
"""
def parse_args():
  """Setup of parsing arguments
  """
  full_description = f"{BANNER}\n\nCRUD HELPER help you to performs CRUD operations with database"
  parser = argparse.ArgumentParser(
    prog='CRUD_helper.py',
    usage='python %(prog)s [options]',
    description=full_description,
    epilog=textwrap.dedent("""
        Examples:
          python %(prog)s -a create -m Student --name "John"
          python %(prog)s -a list -m Grade --id 3
          python %(prog)s -a list -m Grade
          python %(prog)s --action remove -m Teacher --id 7
          python %(prog)s -a update -m Grade --id 651  
    """),
    formatter_class=argparse.RawDescriptionHelpFormatter
  )
  parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], required=True, help='Choose CRUD operation')
  parser.add_argument('-m', '--model', choices=['Group', 'Student', 'Teacher', 'Discipline', 'Grade'], required=True, help='Choose model')
  parser.add_argument('--name', '-n', help='Print name')
  parser.add_argument('--id', type=int, help='Record ID. For Grade: if you specify --id with list, it will show grades only for this student')
  parser.add_argument('--id2', type=int, help='Print second id')
  parser.add_argument('--grade', type=int, help='Print grade for Grade model or change in update action')
  
  return parser.parse_args()

def update_obj_name(model_name, name, id):
  obj = session.get(model_name, id)
  if obj:
    if model_name.__name__ == 'Group':
      obj.group_name = name
    elif model_name.__name__ == 'Discipline':
      obj.discipline_name = name
    else:
      try:
        first_name, last_name = name.split(' ')  
        obj.first_name = first_name
        obj.last_name = last_name
      except ValueError:
        print('Error: enter first and last name separated by a space')
    session.commit()
    return f'{model_name.__name__} name with id={id} updated on name {name}'
  else:
    return f'{model_name.__name__} with id={id} not found'

def delete_obj(id, model_name):
  obj = session.get(model_name, id)
  if obj:
    session.delete(obj)
    session.commit()
    return f'{model_name.__name__} with id={id} deleted'
  else:
    return f"{model_name.__name__} with id={id} not found"
  
def main(args):
  if args.action == 'create':
    match args.model:
      case 'Group':
        session.add(Group(group_name=args.name))
        session.commit()
        print(f'{Group.__name__} instance created')
      case 'Student':
        try:
          first_name, last_name = args.name.split(' ')
          session.add(Student(first_name=first_name, last_name=last_name, group_id=args.id))
          session.commit()
          print(f'{Student.__name__} instance created')
        except (ValueError, AttributeError) as e:
          print(f'Error: {e}') 
      case 'Teacher':
        try:
          first_name, last_name = args.name.split(' ')
          session.add(Teacher(first_name=first_name, last_name=last_name))
          session.commit()
          print(f'{Teacher.__name__} instance created')
        except (ValueError, AttributeError) as e:
          print(f'Error: {e}') 
      case 'Discipline':
        session.add(Discipline(discipline_name=args.name, teacher_id=args.id))
        session.commit()
        print(f'{Discipline.__name__} instance created')
      case 'Grade':
        session.add(Grade(student_id=args.id, discipline_id=args.id2, grade=args.grade))
        session.commit()
        print(f'{Grade.__name__} instance created')
  elif args.action == 'list':
    match args.model:
      case 'Group':
        groups = session.scalars(select(Group)).all()
        for group in groups:
          print(group)
      case 'Student':
        students = session.scalars(select(Student)).all()
        for student in students:
          print(student)
      case 'Teacher':
        teachers = session.scalars(select(Teacher)).all()
        for teacher in teachers:
          print(teacher)
      case 'Discipline':
        disciplines = session.scalars(select(Discipline)).all()
        for discipline in disciplines:
          print(discipline)
      case 'Grade':
        if args.id:
          grades = session.scalars(select(Grade).where(Grade.student_id==args.id)).all()
        else:
          grades = session.scalars(select(Grade)).all()
        for grade in grades:
          print(grade)
  elif args.action == 'update':
    match args.model:
      case 'Group':
        print(update_obj_name(Group, args.name, args.id))
      case 'Student':
        print(update_obj_name(Student, args.name, args.id))
      case 'Teacher':
        print(update_obj_name(Teacher, args.name, args.id))
      case 'Discipline':
        print(update_obj_name(Discipline, args.name, args.id))
      case 'Grade':
        obj = session.get(Grade, args.id)
        if obj:
          obj.grade = args.grade
          session.commit()
          print(f'Grade with id={args.id} updated on {args.grade}')
        else:
          print(f"Grade with id={args.id} not found")
  elif args.action == 'remove':
    match args.model:
      case 'Group':
        print(delete_obj(args.id, Group))
      case 'Student':
        print(delete_obj(args.id, Student))
      case 'Teacher':
        print(delete_obj(args.id, Teacher))
      case 'Discipline':
        print(delete_obj(args.id, Discipline))
      case 'Grade':
        print(delete_obj(args.id, Grade))

if __name__ == "__main__":
  args = parse_args()
  main(args)