from employee_flask_api import app, db
from employee_flask_api.models import Employee, employee_schema, employees_schema, User, check_password_hash
from flask import jsonify, request, render_template, redirect, url_for

# Import for Flask Login #day2
from flask_login import login_required, login_user, current_user, logout_user

# import for PyJWT (Json Web Token) #day2
import jwt

from employee_flask_api.forms import UserForm, LoginForm



#Endpoint for Creating patients #day2
@app.route('/employees/create', methods = ['POST'])
def create_employee():
    name = request.json['full_name']
    gender = request.json['gender']
    address = request.json['address']
    ssn = request.json['ssn']
    blood_type = request.json['blood_type']
    email = request.json['email']

    employee = Employee(name, gender, address, ssn, blood_type, email)

    db.session.add(employee)
    db.session.commit()

    results = employee_schema.dump(employee)
    return jsonify(results)

# Endpoint for ALL patients
@app.route('/employees', methods = ['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify(employees_schema.dump(employees))

# Endpoint for ONE patient based on their ID #day2 
@app.route('/employees/<id>', methods = ['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    results = employee_schema.dump(employee)
    return jsonify(results)

# Endpoint for updating patient data  #day2
@app.route('/employees/update/<id>', methods = ['POST', 'PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    
    #Update info below #day2
    employee.name = request.json['full_name']
    employee.gender = request.json['gender']
    employee.address = request.json['address']
    employee.ssn = request.json['ssn']
    employee.blood_type = request.json['blood_type']
    employee.email = request.json['email']

    db.session.commit()
    
    return employee_schema.jsonify(employee)



# Endpoint for deleting patient data  #day2
@app.route('/employees/delete/<id>', methods = ['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)

    db.session.delete(employee)
    db.session.commit()

    result = employee_schema.dump(employee)
    return jsonify(result)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users/register', methods = ['GET','POST'])
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data 

        user = User(name,email,password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', user_form = form)

@app.route('/user/login', methods = ['GET', "POST"])
def login():
    form = LoginForm()
    email - form.email.data
    password = form.password.data
    
    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        login_user(logged_user)
        return redirect(url_for('get_key'))
    return render_template('login.html', login_form = form)

@app.route('/users/getkey', methods = ['GET'])
def get_key():
    token = jwt.encode({'public_id': current_user.id, 'email':current_user.email},app.config['SECRET_KEY'])
    user = User.query.filter_by(email = current_user.email).first()
    user.token = token 

    db.session.add(user)
    db.session.commit()
    results = token.decode('utf-8')
    return render_template('token.html', token = results)