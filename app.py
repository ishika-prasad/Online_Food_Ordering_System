from flask import Flask, render_template, request
import pymysql
from flask_wtf import RecaptchaField, FlaskForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "secretkey"

app.config["RECAPTCHA_PUBLIC_KEY"] = "*****"
app.config["RECAPTCHA_PRIVATE_KEY"] = "*****"

class Database:
    def __init__(self):
        host = "localhost"
        user = "*****"
        password = "*****"
        db = "onlinefoodorderingdb"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def employee_list(self):
        self.cur.execute("SELECT * FROM employee LIMIT 20")
        result = self.cur.fetchall()
        return result

    def order_details(self):
        self.cur.execute("SELECT * FROM order_details LIMIT 20")
        result = self.cur.fetchall()
        return result

    def orders_table(self):
        self.cur.execute("SELECT * FROM orders_table LIMIT 20")
        result = self.cur.fetchall()
        return result

    def payment_list(self):
        self.cur.execute("SELECT * FROM payment LIMIT 20")
        result = self.cur.fetchall()
        return result

    def restaurant_table(self):
        self.cur.execute("SELECT * FROM restaurant_table LIMIT 20")
        result = self.cur.fetchall()
        return result

class captcha_form(FlaskForm):
    recaptcha = RecaptchaField()

@app.route('/employee')
def employee():
    def db_query():
        db = Database()
        emps = db.employee_list()
        return emps
    res = db_query()
    return render_template('employee.html', result=res, content_type='application/json', row='row')

@app.route('/order_details')
def order_details():
    def db_query():
        db = Database()
        ord_details = db.order_details()
        return ord_details
    res = db_query()
    return render_template('order_details.html', result=res, content_type='application/json', row='row')

@app.route('/orders_table')
def order_table():
    def db_query():
        db = Database()
        ord_table = db.orders_table()
        return ord_table
    res = db_query()
    return render_template('orders_table.html', result=res, content_type='application/json', row='row')

@app.route('/payment')
def payment():
    def db_query():
        db = Database()
        pay = db.payment_list()
        return pay
    res = db_query()
    return render_template('payment.html', result=res, content_type='application/json', row='row')

@app.route('/restaurant_table')
def restaurant_table():
    def db_query():
        db = Database()
        restnt_table = db.restaurant_table()
        return restnt_table
    res = db_query()
    return render_template('restaurant_table.html', result=res, content_type='application/json', row='row')

@app.route('/admin_access_tables')
def start_page():
    return render_template('admin_tables.html')

@app.route('/customer_access_tables')
def customer_page():
    return render_template('customer_tables.html')

@app.route('/')
def sign_up():
    form = captcha_form()
    return render_template('signup.html', form=form)

@app.route('/login')
def login():
    form = captcha_form()
    return render_template('login.html', form=form)

@app.route('/request_order')
def requestOrder():
    return render_template('request_order.html')

@app.route('/order_detail', methods=['POST', 'GET'])
def orderDetail():
    fullname=request.form['fullname']
    email=request.form['email']
    phone=request.form['phone']
    address=request.form['address']
    city=request.form['city']
    state=request.form['state']
    country=request.form['country']
    zipcode=request.form['zipcode']
    food=request.form['food']
    return render_template('order_detail.html', name=fullname, email=email, phone=phone, address=address,
                           city=city, state=state, country=country, zipcode=zipcode, food=food)