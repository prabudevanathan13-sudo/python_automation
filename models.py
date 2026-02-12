"""
School Management System - OOP Models
This module contains all the classes for the school management system.
"""

from datetime import datetime
from typing import List, Optional
import uuid


class Person:
    """Base class for all persons in the school"""
    
    def __init__(self, name: str, email: str, phone: str, address: str):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.created_at = datetime.now()
    
    def __str__(self):
        return f"{self.name} ({self.id})"
    
    def update_info(self, name: Optional[str] = None, email: Optional[str] = None, 
                   phone: Optional[str] = None, address: Optional[str] = None):
        """Update person information"""
        if name:
            self.name = name
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if address:
            self.address = address
    
    def to_dict(self):
        """Convert person to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'type': self.__class__.__name__
        }


class Student(Person):
    """Student class inheriting from Person"""
    
    def __init__(self, name: str, email: str, phone: str, address: str, 
                 grade: str, enrollment_date: str):
        super().__init__(name, email, phone, address)
        self.grade = grade
        self.enrollment_date = enrollment_date
        self.courses = []
        self.grades = {}
    
    def add_course(self, course):
        """Add a course to student's enrollment"""
        if course not in self.courses:
            self.courses.append(course)
    
    def remove_course(self, course):
        """Remove a course from student's enrollment"""
        if course in self.courses:
            self.courses.remove(course)
    
    def set_grade(self, course, grade):
        """Set grade for a course"""
        self.grades[course.name] = grade
    
    def get_gpa(self):
        """Calculate GPA based on grades"""
        if not self.grades:
            return 0.0
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        total = sum(grade_points.get(grade, 0.0) for grade in self.grades.values())
        return round(total / len(self.grades), 2)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'grade': self.grade,
            'enrollment_date': self.enrollment_date,
            'courses': [course.name for course in self.courses],
            'grades': self.grades,
            'gpa': self.get_gpa()
        })
        return data


class Teacher(Person):
    """Teacher class inheriting from Person"""
    
    def __init__(self, name: str, email: str, phone: str, address: str,
                 subject: str, salary: float):
        super().__init__(name, email, phone, address)
        self.subject = subject
        self.salary = salary
        self.courses = []
    
    def add_course(self, course):
        """Add a course to teacher's schedule"""
        if course not in self.courses:
            self.courses.append(course)
    
    def remove_course(self, course):
        """Remove a course from teacher's schedule"""
        if course in self.courses:
            self.courses.remove(course)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'subject': self.subject,
            'salary': self.salary,
            'courses': [course.name for course in self.courses]
        })
        return data


class Staff(Person):
    """Staff class inheriting from Person"""
    
    def __init__(self, name: str, email: str, phone: str, address: str,
                 department: str, position: str, salary: float):
        super().__init__(name, email, phone, address)
        self.department = department
        self.position = position
        self.salary = salary
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'department': self.department,
            'position': self.position,
            'salary': self.salary
        })
        return data


class Course:
    """Course class for managing academic courses"""
    
    def __init__(self, name: str, code: str, description: str, credits: int,
                 teacher: Teacher = None):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.code = code
        self.description = description
        self.credits = credits
        self.teacher = teacher
        self.students = []
    
    def add_student(self, student):
        """Add a student to the course"""
        if student not in self.students:
            self.students.append(student)
            student.add_course(self)
    
    def remove_student(self, student):
        """Remove a student from the course"""
        if student in self.students:
            self.students.remove(student)
            student.remove_course(self)
    
    def assign_teacher(self, teacher):
        """Assign a teacher to the course"""
        self.teacher = teacher
        teacher.add_course(self)
    
    def get_student_count(self):
        """Get number of enrolled students"""
        return len(self.students)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'credits': self.credits,
            'teacher': self.teacher.name if self.teacher else None,
            'student_count': self.get_student_count()
        }


class Classroom:
    """Classroom class for managing classroom information"""
    
    def __init__(self, room_number: str, capacity: int, building: str):
        self.id = str(uuid.uuid4())[:8]
        self.room_number = room_number
        self.capacity = capacity
        self.building = building
        self.schedule = []
    
    def add_to_schedule(self, course, time_slot):
        """Add a course to the classroom schedule"""
        self.schedule.append({'course': course, 'time_slot': time_slot})
    
    def is_available(self, time_slot):
        """Check if classroom is available at a given time"""
        return not any(slot['time_slot'] == time_slot for slot in self.schedule)
    
    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'capacity': self.capacity,
            'building': self.building,
            'schedule': [{'course': s['course'].name, 'time_slot': s['time_slot']} 
                        for s in self.schedule]
        }


class School:
    """Main school management class"""
    
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.students = []
        self.teachers = []
        self.staff = []
        self.courses = []
        self.classrooms = []
    
    # Student management
    def add_student(self, student: Student):
        """Add a new student to the school"""
        self.students.append(student)
    
    def remove_student(self, student_id: str):
        """Remove a student from the school"""
        self.students = [s for s in self.students if s.id != student_id]
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """Get a student by ID"""
        return next((s for s in self.students if s.id == student_id), None)
    
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        return self.students
    
    # Teacher management
    def add_teacher(self, teacher: Teacher):
        """Add a new teacher to the school"""
        self.teachers.append(teacher)
    
    def remove_teacher(self, teacher_id: str):
        """Remove a teacher from the school"""
        self.teachers = [t for t in self.teachers if t.id != teacher_id]
    
    def get_teacher(self, teacher_id: str) -> Optional[Teacher]:
        """Get a teacher by ID"""
        return next((t for t in self.teachers if t.id == teacher_id), None)
    
    def get_all_teachers(self) -> List[Teacher]:
        """Get all teachers"""
        return self.teachers
    
    # Staff management
    def add_staff(self, staff: Staff):
        """Add a new staff member"""
        self.staff.append(staff)
    
    def remove_staff(self, staff_id: str):
        """Remove a staff member"""
        self.staff = [s for s in self.staff if s.id != staff_id]
    
    def get_all_staff(self) -> List[Staff]:
        """Get all staff members"""
        return self.staff
    
    # Course management
    def add_course(self, course: Course):
        """Add a new course"""
        self.courses.append(course)
    
    def remove_course(self, course_id: str):
        """Remove a course"""
        self.courses = [c for c in self.courses if c.id != course_id]
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get a course by ID"""
        return next((c for c in self.courses if c.id == course_id), None)
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        return self.courses
    
    # Classroom management
    def add_classroom(self, classroom: Classroom):
        """Add a new classroom"""
        self.classrooms.append(classroom)
    
    def get_all_classrooms(self) -> List[Classroom]:
        """Get all classrooms"""
        return self.classrooms
    
    # Statistics
    def get_total_students(self):
        """Get total number of students"""
        return len(self.students)
    
    def get_total_teachers(self):
        """Get total number of teachers"""
        return len(self.teachers)
    
    def get_total_staff(self):
        """Get total number of staff"""
        return len(self.staff)
    
    def get_total_courses(self):
        """Get total number of courses"""
        return len(self.courses)
