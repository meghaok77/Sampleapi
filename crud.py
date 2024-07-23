from sqlalchemy.orm import Session
from models import Student


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student_id: int, name: str = None, age: int = None, rollno: int = None):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        if name:
            db_student.name = name
        if age:
            db_student.age = age
        if rollno:
            db_student.rollno = rollno
        db.commit()
        db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student
