from flask import Flask, render_template, request, redirect
import mysql.connector


app = Flask(__name__)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="users_db"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    # Retrieve the username and password from the form submission
    username = request.form['username']
    password = request.form['password']
    
    # Perform a query to check if the username and password exist in the users table
    cursor = mydb.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    
    # If a matching user is found, redirect to the 'profile' URL
    if result:
        return redirect('/profiles?username=' + username)
    else:
        return "Invalid username or password"
    
@app.route('/campus')
def profile():  
    return render_template('campus.html')

@app.route('/profiles', methods=['GET'])
def profiles():
    username = request.args.get('username')

    cursor = mydb.cursor()
    query = "SELECT name FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    name = cursor.fetchone()[0]

    return render_template('profile.html', username=username, name=name)
