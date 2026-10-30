
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Student Management API")

students = []

class Student(BaseModel):
    id: int
    name: str
    course: str
    marks: float = Field(ge=0, le=100)


@app.post("/student", status_code=201)
def add_student(student: Student):
    if any(s.id == student.id for s in students):
        raise HTTPException(status_code=409, detail="Student ID already exists")

    students.append(student)
    return {"message": "Student added successfully", "student": student}


@app.get("/student")
def get_students(course: Optional[str] = None):
    if course:
        return [s for s in students if s.course.lower() == course.lower()]
    return students


@app.get("/student/{id}")
def get_student(id: int):
    for student in students:
        if student.id == id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


@app.put("/student/{id}")
def update_student(id: int, updated_student: Student):
    for index, student in enumerate(students):
        if student.id == id:
            if updated_student.id != id:
                raise HTTPException(status_code=400, detail="ID mismatch")
            students[index] = updated_student
            return {"message": "Student updated successfully", "student": updated_student}
    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/student/{id}")
def delete_student(id: int):
    for student in students:
        if student.id == id:
            students.remove(student)
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
