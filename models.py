from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime

db = SQLAlchemy()



class Admin(db.Model):
    __tablename__ = 'Admin_Details'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(30), nullable = False)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    emp_id = db.Column(db.String(20), unique=True)
    # password = db.Column(db.String(100))

class Teacher(db.Model):
    __tablename__ = 'Teacher_Details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    department = db.Column(db.String(30), nullable = False)
    emp_id = db.Column(db.String(20), unique=True)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    # password = db.Column(db.String(100))

class Student(db.Model):
    __tablename__ = 'Student_Details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable= False)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    # password = db.Column(db.String(100))
    reg_number = db.Column(db.String(40), nullable = False)
    dob = db.Column(db.String(50))
    department = db.Column(db.String(30), nullable = False)

class Course(db.Model):
    __course__ = 'Course_Details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    subjects = db.Column(db.String(300), nullable=False)


class Question_Banks(db.Model):
    __tablename__ = 'Question_Banks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable = False)
    difficulty = db.Column(db.String(20), nullable=False)  # New column

    questions = db.relationship('Questions', backref='question_bank', lazy=True)

class Questions(db.Model):
    __tablename__ = 'Questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable = False)
    option1 = db.Column(db.String(500), nullable = False)
    option2 = db.Column(db.String(500), nullable = False)
    option3 = db.Column(db.String(500), nullable = False)
    option4 = db.Column(db.String(500), nullable = False)
    correct_answer = db.Column(db.String(500), nullable=False)


    question_bank_id = db.Column(db.Integer, db.ForeignKey('Question_Banks.id'), nullable=False)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class Event(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    years = db.Column(db.JSON)
    departments = db.Column(db.JSON)
    event_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    semesters = db.Column(db.JSON)
    courses = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    event_type = db.Column(db.String(50))  # 'exam_schedule', 'timetable', etc.
    visibility = db.Column(db.String(20))  # 'teachers_only', 'all'
    status = db.Column(db.String(20))  # 'draft', 'published', 'modified'
    
class EventModification(db.Model):
    __tablename__ = 'EventModifications'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'))
    modified_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    modifications = db.Column(db.Text)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # Correct table reference
    title = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.String(10), nullable=False)  # Store event date as 'YYYY-MM-DD'
    type = db.Column(db.String(100), nullable=False)
    read = db.Column(db.Boolean, default=False, nullable=False)  # Track whether the notification was read

    def __init__(self, user_id, title, event_date, type):
        self.user_id = user_id
        self.title = title
        self.event_date = event_date
        self.type = type

class Exam(db.Model):
    __tablename__ = 'Exams'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'), nullable=False)
    question_bank_id = db.Column(db.Integer, db.ForeignKey('Question_Banks.id'), nullable=True)  # Optional for now
    exam_duration = db.Column(db.Integer)  # Duration in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Add this to your existing models.py file
class Result(db.Model):
    __tablename__ = 'Results'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('Exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('Questions.id'), nullable=False)
    selected_answer = db.Column(db.String(500), nullable=False)  # A, B, C, or D
    is_correct = db.Column(db.Boolean, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    # student = db.relationship('Student', backref='results')
    exam = db.relationship('Exam', backref='results')
    question = db.relationship('Questions', backref='results')


class ExamCompletion(db.Model):
    __tablename__ = 'exam_completions'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)  # Assuming 'users' table exists
    exam_id = db.Column(db.Integer, db.ForeignKey('Exams.id'), nullable=False)    # Assuming 'exams' table exists
    completed = db.Column(db.Boolean, default=False, nullable=False)              # True if exam is completed
    attempt_number = db.Column(db.Integer, default=1, nullable=False)             # Tracks attempt number
    completion_status = db.Column(db.String(50), nullable=True)                   # e.g., "success", "timeout", "error"
    completed_at = db.Column(db.DateTime, default=db.func.now())                  # Timestamp of completion

    def __repr__(self):
        return f'<ExamCompletion student_id={self.student_id} exam_id={self.exam_id} completed={self.completed}>'


    
   






