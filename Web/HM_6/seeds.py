from datetime import datetime, timedelta, date
from random import randint
import sqlite3
from faker import Faker

fake = Faker('uk-UA')
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
NUMBERS_TEACHERS = 5
NUMBER_STUDENTS = 50

connect = sqlite3.connect('new_sql_hm.sqlite')
cur = connect.cursor()


def seed_teacher():
    teachers = [fake.name() for _ in range(NUMBERS_TEACHERS)]
    sql_ex = "INSERT INTO teachers(full_name) VALUES(?);"
    cur.executemany(sql_ex, zip(teachers,))


def seed_groups():
    sql_ex = "INSERT INTO groups(name) VALUES(?);"
    cur.executemany(sql_ex, zip(groups,))


def seed_subjects():
    list_teacher_id = [randint(1, NUMBERS_TEACHERS) for _ in range(len(subjects))]
    sql_ex = "INSERT INTO subjects(full_name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql_ex, zip(subjects, iter(list_teacher_id)))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    list_group_id = [randint(1, len(groups)) for _ in range(NUMBER_STUDENTS)]
    sql_ex = "INSERT INTO students(full_name, group_id) VALUES(?, ?);"
    cur.executemany(sql_ex, zip(students, iter(list_group_id)))


def seed_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-30", "%Y-%m-%d")

    sql_ex = "INSERT INTO grades(student_id, subject_id, grade, date_of) VALUES(?, ?, ?, ?);"

    def get_list_of_date(start_date, end_date):
        result = []
        current_date: date = start_date
        while current_date <= end_date:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_of_date(start_date, end_date)

    grades = []
    for day in list_dates:
        random_subjects = randint(1, len(subjects))
        random_students = [randint(1, NUMBER_STUDENTS) for _ in range(5)]
        for student in random_students:
            grades.append((student, random_subjects, randint(1, 12), day.date()))
    cur.executemany(sql_ex, grades)


if __name__ == '__main__':
    try:
        seed_teacher()
        seed_groups()
        seed_subjects()
        seed_students()
        seed_grades()
        connect.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        connect.close()
        