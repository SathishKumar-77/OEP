from flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()



class Admin(db.Model):
    __tablename__ = 'Admin_Details'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(30), nullable = False)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    emp_id = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))

class Teacher(db.Model):
    __tablename__ = 'Teacher_Details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    department = db.Column(db.String(30), nullable = False)
    emp_id = db.Column(db.String(20), unique=True)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class Student(db.Model):
    __tablename__ = 'Student_Details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable= False)
    gender = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
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


    
   






