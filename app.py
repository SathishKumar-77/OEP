from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from models import db, Teacher, Admin, Student, Question_Banks, Questions
from flask_migrate import Migrate
from config import *
from flask_mail import Mail
from email_utils import send_email
import config
import bcrypt
import csv
import io
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import chardet



app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session handling and flashing messages

app.config.from_object(config)


db.init_app(app)
migrate = Migrate(app, db)


mail = Mail(app)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return redirect(url_for("login"))





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        ROLE_MODELS = {
            'Admin': Admin,
            'Teacher': Teacher,
            'Student': Student
        }

        user_model = ROLE_MODELS.get(role)
        if not user_model:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('login'))

        # Query the user based on role and username
        if role == 'Student':
            user = user_model.query.filter_by(reg_number=username).first()
        else:
            user = user_model.query.filter_by(emp_id=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['username'] = user.name
            session['role'] = role
            session['user_id'] = user.id
            session.permanent = True

            # Redirect based on role
            return redirect(url_for(f"{role.lower()}_dashboard"))

        flash('Invalid credentials', 'danger')
        return redirect(url_for('login'))

    return render_template('pages/login.html')





@app.route('/get_teachers', methods=['GET'])
def get_teachers():
    try:
        teachers = Teacher.query.all()
        teacher_list = [
            {
                "id": teacher.id,
                "name": teacher.name,
                "email": teacher.email,
                "department": teacher.department,
            }
            for teacher in teachers
        ]
        return jsonify(teacher_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    try:
        # Form data
        name = request.form.get('name')
        department = request.form.get('department')
        gender = request.form.get('gender')
        email = request.form.get('email')
        role = "Teacher / Tutor"

        # Generate hashed password
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_str = hashed_password.decode('utf-8')
        
        # Generate emp_id: Find the last emp_id and increment it
        last_teacher = Teacher.query.order_by(Teacher.id.desc()).first()
        if last_teacher and last_teacher.emp_id:
            # Extract numeric part from the last emp_id
            last_emp_num = int(last_teacher.emp_id.split('_')[1])
            new_emp_num = last_emp_num + 1
        else:
            new_emp_num = 1 

        emp_id = f"EMP_{new_emp_num:04}"

        # Create new teacher record
        new_teacher = Teacher(
            emp_id=emp_id, 
            name=name, 
            department=department, 
            gender=gender,
            email=email, 
            password=hashed_password_str
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        
        # Email sending logic
        subject = f"Account created as role {role}"
        body = f"""
        Hi {name},
        Greetings,
        
        Here are your login credentials for your account:
        Username: {emp_id}
        Password: {default_password}
        Please log in and change your password as soon as possible.
        
        Regards,
        Admin Team
        """
        email_sent = send_email(subject, body, email)
        
        return jsonify({
            "success": True,
            "message": "Teacher added successfully" + 
                      (" and email sent!" if email_sent else " but email could not be sent."),
            "emp_id": emp_id  # Return the generated emp_id
        }), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Email already exists. Please use a different email."
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500



@app.route('/delete_teacher/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    try:
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
            return jsonify({"message": "Teacher deleted successfully!"}), 200
            
        else:
            return jsonify({"error": "Teacher not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    try:
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            return jsonify({
                "id": teacher.id,
                "name": teacher.name,
                "email": teacher.email,
                "department": teacher.department,
            }), 200
        return jsonify({"error": "Teacher not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_teacher/<int:teacher_id>', methods=['POST'])
def update_teacher(teacher_id):
    try:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return jsonify({"error": "Teacher not found"}), 404

        teacher.name = request.form.get('name')
        teacher.department = request.form.get('department')
        teacher.email = request.form.get('email')

        db.session.commit()
        return jsonify({"success": True, "message": "Teacher updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/teachers', methods=['GET'])
def teacher_settings():
    return render_template('teacher_settings.html')

@app.route('/get_student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = Student.query.get(student_id)
        if student:
            return jsonify({
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "gender": student.gender,
                "dob": student.dob,
                "department": student.department
            }
            ), 200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        student.name = request.form.get('name')
        student.email = request.form.get('email')
        student.gender = request.form.get('gender')
        student.dob = request.form.get('dob')
        student.department = request.form.get('department')
        db.session.commit()
        return jsonify({"success": True, "message": "Student updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_students', methods = ['GET'])
def get_students():
    try:
        students = Student.query.all()
        student_list = [
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "gender": student.gender
            }
            for student in students
        ]
        return jsonify(student_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/student_management/')
def student_management():
   
    return render_template('pages/student_management.html')
    

    

@app.route('/question_bank')
def question_bank():
    return render_template('pages/question_bank.html') 


@app.route('/add_student', methods= ['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        department = request.form.get('department')
        dob = request.form.get('dob')
        reg_no = request.form.get('reg_no')

        role = "Student"

        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_str = hashed_password.decode('utf-8')

        try:
            new_student = Student(name = name, email = email, gender = gender, password = hashed_password_str,
                                   department= department, dob=dob, reg_number=reg_no)
            db.session.add(new_student)
            db.session.commit()

            subject = f" Account created as role {role}"
            body = f"""
            Hi {name},

            Greetings,
            
            Here are your login credentials for your account:

            Username: {email}
            Password: {default_password}

            Please log in and change your password as soon as possible.

            Regards,
            Admin Team
            """

            email_sent = send_email(subject, body, email)
            return jsonify({
                "success": True,
                "message": "Student added successfully" + 
                        (" and email sent!" if email_sent else " but email could not be sent.")
            }), 200
    
        except IntegrityError:
            db.session.rollback()
            return jsonify({
                "success": False,
                "error": "Email already exists. Please use a different email."
            }), 400
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
        

@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Student deleted successfully"
                }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Student not found"
                }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
            }), 500



@app.route('/admin_setting/')
def admin_setting():
    try:
        admin = Admin.query.first()
    except Exception as e:
        flash(f"Error fetching admin: {str(e)}", "danger")
    return render_template('pages/admin_setting.html', name = admin.name, email = admin.email)

@app.route("/admin_dashboard")
def admin_dashboard():
    teacher_count = Teacher.query.count()
    student_count = Student.query.count()
    return render_template("pages/admin_dashboard.html", teacher_count= teacher_count, student_count=student_count)

@app.route('/teacher_management/')
def teacher_management():
    try:
        admin = Admin.query.first()
    except Exception as e:
        flash(f"Error fetching admin: {str(e)}", "danger")
    return render_template('pages/teacher_management.html')

@app.route('/course_management/')
def course_management():
    try:
        admin = Admin.query.first()
    except Exception as e:
        flash(f"Error fetching admin: {str(e)}", "danger")
    return render_template('pages/course_management.html')

@app.route("/teacher_dashboard/")
def teacher_dashboard():
    return render_template("pages/teacher_dashboard.html")

@app.route("/student_dashboard/")
def student_dashboard():
    return render_template("pages/student_dashboard.html")


@app.route('/download_csv_template')
def download_csv_template():
    csv_template = "name,gender,email,reg_number,dob,department\n"
    response = Response(csv_template, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=student_template.csv'
    return response



@app.route('/upload_students', methods=['POST'])
def upload_students():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            # Read CSV file
            stream = file.stream.read().decode('utf-8')
            csv_reader = csv.DictReader(stream.splitlines())

            added_students = []
            errors = []

            for row in csv_reader:
                try:
                    name = row.get('name')
                    email = row.get('email')
                    gender = row.get('gender')
                    department = row.get('department')
                    dob = row.get('dob')
                    reg_number = row.get('reg_number')

                    # Hash default password
                    hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    # Add new student to the database
                    new_student = Student(
                        name=name,
                        email=email,
                        gender=gender,
                        password=hashed_password,
                        department=department,
                        dob=dob,
                        reg_number=reg_number
                    )
                    db.session.add(new_student)
                    db.session.commit()  # Commit after each student is added

                    # Send email with login details
                    subject = "Your Account Has Been Created"
                    body = f"""
                    Hi {name},

                    Your account has been created successfully.

                    Here are your login credentials:
                    Username: {email}
                    Password: {default_password}

                    Please log in and change your password as soon as possible.

                    Regards,
                    Admin Team
                    """

                    if send_email(subject, body, email):
                        added_students.append(name)
                    else:
                        errors.append(f"Failed to send email to {email}")

                except IntegrityError:
                    db.session.rollback()
                    errors.append(f"Duplicate email: {row.get('email')}")
                except Exception as e:
                    errors.append(f"Error in row {row}: {str(e)}")

            return jsonify({
                "success": True,
                "message": f"Added {len(added_students)} students successfully.",
                "errors": errors
            }), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": False, "error": "Invalid file format. Only .csv files are allowed."}), 400

@app.route('/view_question_banks', methods=['GET'])
def view_question_bank():
    try:
        question_bank = Question_Banks.query.all()
        data = [
            {
                "id": q.id,
                "name": q.name,
                "difficulty": q.difficulty if hasattr(q, 'difficulty') else "Unknown"
            }
            for q in question_bank
        ]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": "Failed to retrieve question bank"}), 500



@app.route('/view_question_bank/<int:id>', methods=['GET'])
def view_question_bank_by_id(id):
    try:
        # Fetch the question bank details by ID
        question_bank = Question_Banks.query.get(id)
        if not question_bank:
            return jsonify({"error": "Question Bank not found"}), 404

        # Fetch all questions associated with the question bank
        questions = Questions.query.filter_by(question_bank_id=id).all()

        # Prepare question bank details
        question_bank_data = {
            "id": question_bank.id,
            "name": question_bank.name,
            "difficulty": question_bank.difficulty,
            "total_questions": len(questions),
        }

        # Prepare associated questions
        questions_data = []
        for question in questions:
            questions_data.append({
                "id": question.id,
                "question": question.question,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "correct_answer": question.correct_answer
            })

        # Return both as a JSON response
        return jsonify({
            "question_bank": question_bank_data,
            "questions": questions_data
        })
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app.route('/view_question_bank.html')
def view_question_bank_page():
    return render_template('pages/view_question_bank.html')




@app.route('/download_questionbank_template')
def download_questionbank_template():
    csv_template = "question,option1,option2,option3,option4,correct_answer\n"
    response = Response(csv_template, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=question_bank_template.csv'
    return response

# Endpoint to upload .csv file
@app.route('/upload_question_bank', methods=['POST'])
def upload_question_bank():
    try:
        question_bank_name = request.form.get('question_name')
        difficulty = request.form.get('difficulty')
        file = request.files.get('file')

        if not question_bank_name or not difficulty:
            return jsonify({'error': 'Question bank name and difficulty level are required'}), 400

        question_bank = Question_Banks.query.filter_by(name=question_bank_name, difficulty=difficulty).first()

        if not question_bank:
            question_bank = Question_Banks(name=question_bank_name, difficulty=difficulty)
            db.session.add(question_bank)
            db.session.flush()  

        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            # stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            stream = io.StringIO(file.stream.read().decode("utf-8", errors='replace'), newline=None)

            csv_reader = csv.DictReader(stream)

            required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_answer']
            if not all(column in csv_reader.fieldnames for column in required_columns):
                return jsonify({'error': 'CSV file missing required columns'}), 400

            for row in csv_reader:
                question = Questions(
                    question=row['question'],
                    option1=row['option1'],
                    option2=row['option2'],
                    option3=row['option3'],
                    option4=row['option4'],
                    correct_answer=row['correct_answer'],
                    question_bank_id=question_bank.id
                )
                db.session.add(question)

        db.session.commit()
        # return jsonify({'message': 'Question bank and questions added successfully'}), 201
        flash('Question bank and questions added successfully', 'success')
        return redirect(url_for('question_bank'))
    

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
