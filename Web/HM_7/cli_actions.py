from datetime import datetime

from sqlalchemy import or_

from database.db import session
from database.models import Grade, Student, Group, Subject, Teacher


def show(model, name, _id):
    info = ""
    match model:
        case "Grade":
            if _id:
                info = session.query(Grade).filter(Grade.id == _id).one()
            else:
                print("If you want to get info from table 'Grade', enter 'id'")
        case "Student":
            if _id:
                info = session.query(Student).filter(Student.id == _id).one()
            elif name:
                info = session.query(Student).filter(Student.fullname == name).one()
            else:
                print("If you want to get info from table 'Student', enter 'id' or 'fullname'")
        case "Group":
            if _id:
                info = session.query(Group).filter(Group.id == _id).one()
            elif name:
                info = session.query(Group).filter(Group.name == name).one()
            else:
                print("If you want to get info from table 'Group', enter 'id' or 'name'")
        case "Subject":
            if _id:
                info = session.query(Subject).filter(Subject.id == _id).one()
            elif name:
                info = session.query(Subject).filter(Subject.name == name).one()
            else:
                print("If you want to get info from table 'Subject', enter 'id' or 'name'")
        case "Teacher":
            if _id:
                info = session.query(Teacher).filter(Teacher.id == _id).one()
            elif name:
                info = session.query(Teacher).filter(Teacher.fullname == name).one()
            else:
                print("If you want to get info from table 'Teacher', enter 'id' or 'fullname'")
    if info:
        return info


def remove(model, name, _id):
    info = ""
    match model:
        case "Grade":
            if _id:
                info = session.query(Grade).filter(Grade.id == _id).delete()
                info = _id
            else:
                print("If you want to remove info from table 'Grade', enter 'id'")
        case "Student":
            if _id:
                session.query(Student).filter(Student.id == _id).delete()
                info = _id
            elif name:
                session.query(Student).filter(Student.fullname == name).delete()
                info = name
            else:
                print("If you want to remove info from table 'Student', enter 'id' or 'fullname'")
        case "Group":
            if _id:
                session.query(Group).filter(Group.id == _id).delete()
                info = _id
            elif name:
                session.query(Group).filter(Group.name == name).delete()
                info = name
            else:
                print("If you want to remove info from table 'Group', enter 'id' or 'name'")
        case "Subject":
            if _id:
                session.query(Subject).filter(Subject.id == _id).delete()
                info = _id
            elif name:
                session.query(Subject).filter(Subject.name == name).delete()
                info = name
            else:
                print("If you want to remove info from table 'Subject', enter 'id' or 'name'")
        case "Teacher":
            if _id:
                session.query(Teacher).filter(Teacher.id == _id).delete()
                info = _id
            elif name:
                session.query(Teacher).filter(Teacher.fullname == name).delete()
                info = name
            else:
                print("If you want to remove info from table 'Teacher', enter 'id' or 'fullname'")
    session.commit()
    session.close()
    if info:
        return info


def create(model, _id, name, grade, _date, st_id, sb_id, gr_id, teach_id):
    match model:
        case "Grade":
            if _date:
                _date = datetime.strptime(_date, "%Y-%m-%d")
            info = Grade(grade=grade, date_of=_date, student_id=st_id, subject_id=sb_id)
        case "Student":
            info = Student(fullname=name, group_id=gr_id)
        case "Group":
            info = Student(name=name)
        case "Subject":
            info = Student(name=name, teacher_id=teach_id)
        case "Teacher":
            info = Student(fullname=name)
    session.add(info)
    session.commit()
    # except IntegrityError as err:
    #     print(f"Some parametr doesnt exists in table {model}")
    # finally:
    session.close()


def update(model, _id, name, grade, _date, st_id, sb_id, gr_id, teach_id):
    match model:
        case "Grade":
            row = session.query(Grade).filter(Grade.id == _id)
            if row:
                if _date:
                    _date = datetime.strptime(_date, "%Y-%m-%d")
                row.update({"grade": grade, "date_of": _date, "student_id": st_id, "subject_id": sb_id})
        case "Student":
            row = session.query(Student).filter(or_(Student.id == _id, Student.fullname == name))
            if row:
                row.update({"fullname": name, "group_id": gr_id})
        case "Group":
            row = session.query(Group).filter(or_(Group.id == _id, Group.fullname == name))
            if row:
                row.update({"name": name})
        case "Subject":
            row = session.query(Subject).filter(or_(Subject.id == _id, Subject.name == name))
            if row:
                row.update({"name": name, "teacher_id": teach_id})
        case "Teacher":
            row = session.query(Teacher).filter(or_(Teacher.id == _id, Teacher.fullname == name))
            if row:
                row.update({"fullname": name})
    session.commit()
    session.close()
    return row.first()
