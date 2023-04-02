from sqlalchemy import func, desc, and_

from database.models import Teacher, Student, Subject, Grade, Group
from database.db import session


def select_1():
    data = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg')) \
        .limit(5).all()
    return data


def select_2():
    data = session.query(Subject.name, Student.fullname,
                         func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Subject) \
        .filter(Subject.id == 3) \
        .group_by(Student.id, Subject.name).order_by(desc('avg_grade')).limit(1).first()

    return data


def select_3():
    data = session.query(Subject.name, Group.name, func.round(func.avg(Grade.grade), 2).label('avg')) \
        .select_from(Grade).join(Subject).join(Student).join(Group) \
        .filter(Subject.id == 4) \
        .group_by(Group.name, Subject.name).order_by(desc('avg')).all()
    return data


def select_4():
    data = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).all()
    return data


def select_5():
    data = session.query(Subject.name, Teacher.fullname).join(Subject) \
        .order_by(Teacher.fullname).all()
    return data


def select_6():
    data = session.query(Group.name, Student.fullname) \
        .join(Group).order_by(Group.id, Student.fullname).all()
    return data


def select_7():
    data = session.query(Subject.name, Group.name, Student.fullname, Grade.grade) \
        .select_from(Grade).join(Student).join(Group).join(Subject) \
        .filter(and_(Subject.id == 2, Group.id == 1)) \
        .order_by(Group.id, Student.fullname, desc(Grade.grade)).all()
    return data


def select_8():
    data = session.query(Teacher.fullname, Subject.name,
                         func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Subject).join(Teacher) \
        .filter(Teacher.id == 4).group_by(Teacher.fullname, Subject.name).all()
    return data


def select_9():
    data = session.query(Student.fullname, Subject.name) \
        .select_from(Student).join(Grade).join(Subject) \
        .filter(Student.id == 4).group_by(Student.fullname, Subject.name) \
        .order_by(Subject.name).all()
    return data


def select_10():
    data = session.query(Student.fullname, Subject.name, Teacher.fullname) \
        .select_from(Student).join(Grade).join(Subject).join(Teacher) \
        .filter(and_(Student.id == 4, Teacher.id == 4)).group_by(Student.fullname, Subject.name, Teacher.fullname) \
        .order_by(Subject.name).all()
    return data


def select_11():
    data = session.query(Student.fullname,
                         func.round(func.avg(Grade.grade), 2).label('avg_grade'),
                         Teacher.fullname) \
        .select_from(Grade).join(Subject).join(Student).join(Teacher) \
        .filter(and_(Student.id == 4, Teacher.id == 4)).group_by(Student.fullname, Teacher.fullname).all()
    return data


def select_12():
    date = session.query(func.max(Grade.date_of)) \
        .join(Student) \
        .filter(and_(Grade.discipline_id == 2, Student.group_id == 3)).scalar_subquery()

    data = session.query(Student.fullname, Subject.name, Grade.grade, Grade.date_of) \
        .select_from(Grade).join(Student).join(Subject) \
        .filter(and_(Grade.discipline_id == 2, Student.group_id == 2, Grade.date_of == date)).all()
    return data


if __name__ == '__main__':
    print(select_1())
