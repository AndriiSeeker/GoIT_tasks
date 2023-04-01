from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.models import Teacher, Student, Subject, Grade, Group
from database.db import session


subjects = [
    "Алгоритмізація",
    "Вища математика",
    "Теорія алгоритмів",
    "Дискретна математика",
    "Комп'ютерні мережі",
    "Web-технології",
    "Операційні системи"
]

groups = ["1КН-22б", "ХП-31", "ГС-2"]

fake = faker.Faker('uk-UA')
number_of_teachers = 5
number_of_students = 50


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def seed_teachers():
    for _ in range(number_of_teachers):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)


def seed_subjects():
    teacher_ids = session.scalars(select(Teacher.id)).all()
    for subject in subjects:
        session.add(Subject(name=subject, teacher_id=choice(teacher_ids)))


def seed_groups():
    for group in groups:
        session.add(Group(name=group))


def seed_students():
    group_ids = session.scalars(select(Group.id)).all()
    for _ in range(number_of_students):
        student = Student(fullname=fake.name(), group_id=choice(group_ids))
        session.add(student)


def seed_grades():
    start_date = datetime.strptime("2020-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2021-05-30", "%Y-%m-%d")
    d_range = date_range(start=start_date, end=end_date)
    subjects_ids = session.scalars(select(Subject.id)).all()
    student_ids = session.scalars(select(Student.id)).all()

    for d in d_range:
        random_id_discipline = choice(subjects_ids)
        random_ids_student = [choice(student_ids) for _ in range(5)]

        for student_id in random_ids_student:
            grade = Grade(grade=randint(1, 12), date_of=d, student_id=student_id,
                          discipline_id=random_id_discipline)
            session.add(grade)


if __name__ == '__main__':
    try:
        seed_teachers()
        seed_subjects()
        session.commit()
        seed_groups()
        seed_students()
        session.commit()
        seed_grades()
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()
