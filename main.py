from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from models import Base, Student, engine, SessionLocal
import crud

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StudentCreate(BaseModel):
    name: str
    age: int
    rollno: int


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    rollno: Optional[int] = None


@app.get("/")
def index():
    return {"name": "first data"}


@app.get("/get-students/{student_id}")
def get_students(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/create-student/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name, age=student.age, rollno=student.rollno)
    return crud.create_student(db, db_student)


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id, name=student.name, age=student.age, rollno=student.rollno)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "student deleted successfully"}
