from flask import Flask, render_template, request, redirect, session
from db import conn, cursor
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "school_secret_key"




# =========================================================
# Home Page
# =========================================================
@app.route("/")
def home():
    return render_template("index.html")




# =========================================================
# Registration Page Open
# =========================================================
@app.route("/register")
def register():
    return render_template("register.html")




# =========================================================
# Save User in MySQL -----------> Register Page
# =========================================================
@app.route("/register_user", methods=["POST"])
def register_user():

    fullname = request.form["fullname"]
    email = request.form["email"]
    password = request.form["password"]

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return "Email Already Registered"
    

    cursor.execute ("""
        INSERT INTO users
        (fullname,email,password)
        VALUES(%s,%s,%s)
        """,
        (fullname,email,password)
    )
        
    conn.commit()

    return redirect("/success")




# =========================================================
# Success Page
# =========================================================
@app.route("/success")
def success():
    return render_template("success.html")





# =========================================================
# Login Page
# =========================================================
@app.route("/login")
def login():
    return render_template("login.html")




# =========================================================
# LogIn Process
# =========================================================
@app.route("/login_user", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user :
        session["user"] = user["fullname"]
        return redirect("/dashboard")

    return "Invalid Email or Password"





# =========================================================
# Dashboard Page
# =========================================================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    cursor.execute(
        "SELECT COUNT(*) AS total FROM students"
    )
    student_count = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) AS total FROM teachers"
    )
    teacher_count = cursor.fetchone()["total"]

    return render_template(
        "dashboard.html",
        username=session["user"],
        student_count=student_count,
        teacher_count=teacher_count
    )






# =========================================================
# Students Page
# =========================================================
@app.route("/students")
def students():

    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM students")

    students_data = cursor.fetchall()

    return render_template(
        "students.html",
        students=students_data
    )



# =========================================================
# Add Student
# =========================================================
@app.route("/add_student", methods=["POST"])
def add_student():

    student_id = request.form["student_id"]
    name = request.form["name"]
    class_name = request.form["class"]
    phone = request.form["phone"]
    dob = request.form["dob"]


    cursor.execute("""
            INSERT INTO students
            (student_id,name,class_name,phone,dob)
            VALUES(%s,%s,%s,%s,%s)
        """,
        (student_id, name, class_name, phone, dob)
    )

    conn.commit()

    return redirect("/students")



# =========================================================
# =========================================================
@app.route("/delete_student/<int:id>")
def delete_student(id):

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    conn.commit()

    return redirect("/students")







# =========================================================
# Teachers Page
# =========================================================
@app.route("/teachers")
def teachers():

    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM teachers")

    teachers_data = cursor.fetchall()

    return render_template(
        "teachers.html",
        teachers=teachers_data
    )



# =========================================================
# =========================================================
@app.route("/add_teacher", methods=["POST"])
def add_teacher():

    teacher_id = request.form["teacher_id"]
    name = request.form["name"]
    subject_name = request.form["subject"]
    class_name = request.form["class"]
    email = request.form["email"]

    query = """
    INSERT INTO teachers
    (teacher_id,name,subject_name,class_name,email)
    VALUES(%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            teacher_id,
            name,
            subject_name,
            class_name,
            email
        )
    )

    conn.commit()

    return redirect("/teachers")



# =========================================================
# =========================================================
@app.route("/delete_teacher/<int:id>")
def delete_teacher(id):

    cursor.execute(
        "DELETE FROM teachers WHERE id=%s",
        (id,)
    )

    conn.commit()

    return redirect("/teachers")






# =========================================================
# Time Table
# =========================================================
@app.route("/timetable")
def timetable():

    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM timetable")

    timetable_data = cursor.fetchall()

    return render_template(
        "timetable.html",
        timetable=timetable_data
    )



# =========================================================
# Add Time Table
# =========================================================
@app.route("/add_timetable", methods=["POST"])
def add_timetable():

    day_name = request.form["day_name"]
    period1 = request.form["period1"]
    period2 = request.form["period2"]
    period3 = request.form["period3"]
    period4 = request.form["period4"]
    period5 = request.form["period5"]
    period6 = request.form["period6"]

    query = """
    INSERT INTO timetable
    (day_name,period1,period2,period3,period4,period5,period6)
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            day_name,
            period1,
            period2,
            period3,
            period4,
            period5,
            period6
        )
    )

    conn.commit()

    return redirect("/timetable")


# =========================================================
# Delete Time Table
# =========================================================
@app.route("/delete_timetable/<int:id>")
def delete_timetable(id):

    cursor.execute(
        "DELETE FROM timetable WHERE id=%s",
        (id,)
    )

    conn.commit()

    return redirect("/timetable")






# =========================================================
# Logout
# =========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



app.run(debug=True)