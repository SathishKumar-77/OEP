from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from models import *
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
from flask_session import Session
from flask_socketio import SocketIO, emit
import logging




app = Flask(__name__)
app.secret_key = "your_secret_key"  
socketio = SocketIO(app, cors_allowed_origins="*")  


# App Configuration
app.config.from_object(config)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)


db.init_app(app)

migrate = Migrate(app, db)

mail = Mail(app)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def home():
    return redirect(url_for("login"))





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
    
   
        # Query the User model for the provided role and username
        user = User.query.filter_by(role=role, username=username).first()
        

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # session['username'] = user.name
            session['role'] = user.role
            session['user_id'] = user.id
            session.permanent = True

            user_id = session.get('user_id') 
               
            print("AFter login user id is:", user_id)

            # Redirect based on role
            return redirect(url_for(f"{role.lower()}_dashboard", user_id= user_id))

        flash('Invalid credentials or role', 'danger')
        return redirect(url_for('login'))

    return render_template('pages/login.html')



@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))




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
        
        last_teacher = Teacher.query.order_by(Teacher.id.desc()).first()
        if last_teacher and last_teacher.emp_id:
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
            email=email
            
        )
        new_teacher_password = User(
            username=emp_id,
            password=hashed_password_str,
            role="Teacher"

        )
        
        db.session.add(new_teacher)
        db.session.add(new_teacher_password)
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


@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        # Form data
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        department = request.form.get('department')
        dob = request.form.get('dob')
        reg_no = request.form.get('reg_no')
        role = "Student"

        # Generate hashed password
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        hashed_password_str = hashed_password.decode('utf-8')

        # Create new student record
        new_student = Student(
            name=name,
            email=email,
            gender=gender,
            department=department,
            dob=dob,
            reg_number=reg_no
        )
        
        # Create new user record for login
        new_student_user = User(
            username=reg_no,  # Using registration number as username
            password=hashed_password_str,
            role="Student"
        )
        
        db.session.add(new_student)
        db.session.add(new_student_user)
        db.session.commit()
        
        # Email sending logic
        subject = f"Account created as role {role}"
        body = f"""
        Hi {name},
        Greetings,
        
        Here are your login credentials for your account:
        Username: {reg_no}
        Password: {default_password}
        Please log in and change your password as soon as possible.
        
        Regards,
        Admin Team
        """
        email_sent = send_email(subject, body, email)
        
        return jsonify({
            "success": True,
            "message": "Student added successfully" + 
                      (" and email sent!" if email_sent else " but email could not be sent."),
            "reg_no": reg_no  # Return the registration number for reference
        }), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": "Email or registration number already exists. Please use different values."
        }), 400
        
    except Exception as e:
        db.session.rollback()
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
    if 'role' not in session or session['role'] != 'Admin':
        flash("Please log in to access the portal", "danger")
        return redirect(url_for('login'))
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
    if 'role' not in session or session['role'] != 'Teacher':
        flash("Please log in to access the portal", "danger")
        return redirect(url_for('login'))
    return render_template('pages/teacher_dashboard.html')
    # return render_template("pages/teacher_dashboard.html")

@app.route("/student_dashboard/")
def student_dashboard():
    if 'role' not in session or session['role'] != 'Student':
        flash("Please log in to access the portal", "danger")
        return redirect(url_for('login'))
    return render_template('pages/student_dashboard.html')
    # return render_template("pages/student_dashboard.html")


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
    



@app.route('/event_calendar/')
def event_calendar():
    return render_template('pages/event_calendar.html')





@app.route('/event_create', methods=['GET', 'POST'])
def event_create():
    try:
        event_id = request.args.get('id')
        event_date_str = request.args.get('date')

        if event_id and event_date_str:
            event = Event.query.filter_by(id=event_id, event_date=event_date_str).first()
            if event:
                return {
                    "title": event.title,
                    "description": event.description,
                    "event_date": event.event_date.strftime('%Y-%m-%d'),
                    "type": event.event_type
                }
            return {"error": "Event not found"}, 404

        user_id = session.get('user_id')
        if not user_id:
            flash('User not found', 'danger')
            return redirect(url_for('login'))

        event_date = None
        if event_date_str:
            try:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", "danger")
                # Pass question_banks even on error
                question_banks = Question_Banks.query.all()
                return render_template('pages/event_create.html', question_banks=question_banks)
        
        if request.method == 'POST':
            event = Event(
                title=request.form['title'],
                description=request.form['description'],
                event_type=request.form['event_type'],
                visibility=request.form['visibility'],
                years=','.join(request.form.getlist('years[]')) if request.form.getlist('years[]') else None,
                departments=','.join(request.form.getlist('departments[]')) if request.form.getlist('departments[]') else None,
                semesters=','.join(request.form.getlist('semesters[]')) if request.form.getlist('semesters[]') else None,
                courses=','.join(request.form.getlist('courses[]')) if request.form.getlist('courses[]') else None,
                created_by=user_id,
                status='published',
                event_date=event_date
            )
            db.session.add(event)
            db.session.flush()

            if event.id is None:
                print("❌ Event ID is still None! Something is wrong.")
                flash("Error creating event. Please try again.", "danger")
                db.session.rollback()
                question_banks = Question_Banks.query.all()
                return render_template('pages/event_create.html', question_banks=question_banks)

            if event.event_type.lower() == 'exam_schedule':
                exam_duration = request.form.get('exam_duration')
                question_bank_id = request.form.get('question_bank_id')
                if not exam_duration or not question_bank_id:
                    flash("Please specify exam duration and select a question bank for the exam schedule.", "danger")
                    db.session.rollback()
                    question_banks = Question_Banks.query.all()
                    return render_template('pages/event_create.html', question_banks=question_banks)

                exam = Exam(
                    event_id=event.id,
                    question_bank_id=int(question_bank_id),
                    exam_duration=int(exam_duration)
                )
                db.session.add(exam)
                print(f"✅ Exam linked to event ID: {event.id} with duration: {exam_duration} minutes and question bank ID: {question_bank_id}")

            db.session.commit()
            print(f"✅ Event successfully created with ID: {event.id}")

            try:
                notifications = []
                teachers = User.query.filter_by(role='Teacher').all()
                print(f"🔍 Found {len(teachers)} teachers.")
                if not teachers:
                    print("❌ No teachers found! Skipping teacher notifications.")
                else:
                    for teacher in teachers:
                        print(f"📌 Creating notification for teacher ID: {teacher.id}")
                        notification = Notification(
                            user_id=teacher.id,
                            title=event.title,
                            event_date=event.event_date.strftime('%Y-%m-%d') if event.event_date else None,
                            type=event.event_type
                        )
                        notifications.append(notification)

                if event.visibility == 'all':
                    students = User.query.filter_by(role='Student').all()
                    print(f"🔍 Found {len(students)} students.")
                    if not students:
                        print("❌ No students found! Skipping student notifications.")
                    else:
                        for student in students:
                            print(f"📌 Creating notification for student ID: {student.id}")
                            notification = Notification(
                                user_id=student.id,
                                title=event.title,
                                event_date=event.event_date.strftime('%Y-%m-%d') if event.event_date else None,
                                type=event.event_type
                            )
                            notifications.append(notification)

                if notifications:
                    db.session.bulk_save_objects(notifications)
                    db.session.commit()
                    print("✅ Notifications inserted successfully.")

                    event_data = {
                        'title': event.title,
                        'event_date': event.event_date.strftime('%Y-%m-%d') if event.event_date else None,
                        'type': event.event_type,
                        'id': event.id
                    }
                    socketio.emit('new_event_notification', event_data, namespace='/teachers')
                    print("📡 Emitted notification to /teachers namespace")
                    if event.visibility == 'all':
                        socketio.emit('new_event_notification', event_data, namespace='/students')
                        print("📡 Emitted notification to /students namespace")
                else:
                    print("⚠️ No notifications to insert.")

            except Exception as e:
                db.session.rollback()
                print(f"❌ Notification insertion error: {str(e)}")
                flash(f"Notification error: {str(e)}", "danger")

            flash('Event created and notifications sent successfully', "success")
            return redirect(url_for('event_calendar'))

    except Exception as e:
        db.session.rollback()
        print(f"❌ Something went wrong: {str(e)}")
        flash(f"Error: {str(e)}", "danger")
        question_banks = Question_Banks.query.all()
        return render_template('pages/event_create.html', question_banks=question_banks)

    # Normal GET request
    question_banks = Question_Banks.query.all()
    return render_template('pages/event_create.html', question_banks=question_banks)


# @socketio.on('connect', namespace='/teachers')
# def handle_teacher_connect():
#     print('A teacher connected')

# @socketio.on('disconnect', namespace='/teachers')
# def handle_teacher_disconnect():
#     print('A teacher disconnected')


@app.route('/get_notifications')
def get_notifications():
    user_id = session.get('user_id')  # Assuming you store the user_id in the session
    if not user_id:
        return jsonify([])
    print("After getting notification user id  is:", user_id)

    notifications = Notification.query.filter_by(user_id=user_id).all()
    print("After getting notification is:", notifications)
    notifications_data = [{
        'id': notification.id,
        'title': notification.title,
        'event_date': notification.event_date,
        'type': notification.type,
        'read': notification.read
    } for notification in notifications]


    return jsonify(notifications_data)


@app.route('/delete_notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted successfully'})


@app.route('/get-events')
# @login_required
def get_events():
    # Fetch events from database
    events = Event.query.all()
    
    # Format events for FullCalendar
    calendar_events = []
    for event in events:
        # Get event color based on type
        color = {
            'exam_schedule': '#dc3545',  # red
            'timetable': '#0d6efd',      # blue
            'announcement': '#198754',    # green
            'assignment': '#ffc107',      # yellow
            'results': '#6f42c1'         # purple
        }.get(event.event_type, '#6c757d')  # default gray
        
        # Format event for calendar
        calendar_events.append({
            'id': event.id,
            'title': event.title,
            'start': event.event_date.isoformat(),
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'description': event.description,
                'type': event.event_type,
                'departments': event.departments,
                'years': event.years,
                'semesters': event.semesters,
                'courses': event.courses
            }
        })
    
    return jsonify(calendar_events)


@app.route('/api/event_details', methods=['GET'])
def get_event_details():
    try:
        event_id = request.args.get('id')

        event_date = request.args.get('date')
        print("Event id is", event_id)
       
        
        if not event_id:
            return jsonify({"message": "Event ID is required"}), 400
            
        event = Event.query.get(event_id)
        print("Event is:", event)
        
        if not event:
            return jsonify({"message": "Event not found"}), 404
            
        return jsonify({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_date": event.event_date.strftime('%Y-%m-%d'),
            "event_type": event.event_type,
            "departments": event.departments,
            "courses": event.courses,
            "status": event.status
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error fetching event details: {str(e)}"}), 500


@app.route('/detailed_notifications/<int:notification_id>')
def detailed_notifications(notification_id):
    try:
        event_date = request.args.get('date')
        event = Event.query.get(notification_id)
        
        if not event:
            flash('Event not found', 'error')
            return redirect(url_for('home'))
            
        return render_template('pages/detailed_notifications.html', event=event)
        
    except Exception as e:
        flash('Error loading event details', 'error')
        return redirect(url_for('home'))


@app.route("/teacher_events/")
def teacher_events():
    if 'role' not in session or session['role'] != 'Teacher':
        flash("Please log in to access the portal", "danger")
        return redirect(url_for('login'))
    
    # Get all events ordered by date
    events = Event.query.order_by(Event.event_date.desc()).all()
    print(f"Found {len(events)} total events")  # Debug log
    
    # Debug log each event
    for event in events:
        print(f"Event: {event.title}, Created by: {event.created_by}, Date: {event.event_date}")
    
    return render_template('pages/teacher_events.html', events=events)

@app.route('/api/event_details')
def event_details():
    if 'role' not in session or session['role'] != 'Teacher':
        return jsonify({"error": "Unauthorized"}), 401
    
    event_id = request.args.get('id')
    if not event_id:
        return jsonify({"error": "Event ID is required"}), 400
    
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    return jsonify({
        "id": event.id,
        "title": event.title,
        "event_date": event.event_date.strftime('%Y-%m-%d') if event.event_date else None,
        "event_type": event.event_type,
        "description": event.description,
        "departments": event.departments,
        "courses": event.courses,
        "status": event.status
    })

@app.route('/api/event_visibility/<int:event_id>', methods=['POST'])
def update_event_visibility(event_id):
    if 'role' not in session or session['role'] != 'Teacher':
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        new_visibility = data.get('visibility')
        
        if not new_visibility or new_visibility not in ['all', 'teachers_only']:
            return jsonify({"error": "Invalid visibility value"}), 400
        
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        event.visibility = new_visibility
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Event visibility updated to {new_visibility}"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/attend_exam/<int:event_id>', methods=['GET','POST'])
def attend_exam(event_id):
    # Ensure student is logged in
    user_id = session.get('user_id')

    if not user_id or db.session.get(User, user_id).role != 'Student':
        flash('You must be a student to attend an exam.', 'danger')
        return redirect(url_for('login'))

    # Fetch the event and exam
    event = Event.query.get_or_404(event_id)
    if event.event_type.lower() != 'exam_schedule' or event.visibility != 'all':
        flash('This event is not an exam or not available to students.', 'danger')
        return redirect(url_for('student_events'))

    exam = Exam.query.filter_by(event_id=event_id).first_or_404()
    question_bank = Question_Banks.query.get(exam.question_bank_id)
    questions = Questions.query.filter_by(question_bank_id=exam.question_bank_id).all()

    if not questions:
        flash('No questions available for this exam.', 'warning')
        return redirect(url_for('student_events'))

    # if request.method == 'POST':
    #     answers = []
    #     for question in questions:
    #         answer = request.form.get(f'question_{question.id}')
    #         if answer:
    #             student_answer = StudentAnswer(
    #                 student_id=user_id,
    #                 exam_id=exam.id,
    #                 question_id=question.id,
    #                 selected_answer=answer
    #             )
    #             answers.append(student_answer)

    #     if answers:
    #         db.session.bulk_save_objects(answers)
    #         db.session.commit()
    #     flash('Exam submitted successfully!', 'success')
    #     return redirect(url_for('student_events'))

    return render_template('pages/attend_exam.html', 
                         event=event, 
                         exam=exam, 
                         question_bank=question_bank, 
                         questions=questions)
    
   
    

@app.route('/student_events')
def student_events():
    # Assuming student login is authenticated
    events = Event.query.all()    
    return render_template('pages/student_events.html', events=events)

# @app.route('/attend_exam/<int:event_id>', methods=['GET'])
# def attent_exam(event_id):
#     exam = Exam.query.filter_by(event_id=event_id).first_or_404()
#     event = Event.query.get_or_404(event_id)


#     return render_template('pages/attend_exam.html', event =event, exam =exam)



if __name__ == '__main__':
    socketio.run(app, debug=True)
