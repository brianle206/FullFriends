from flask import Flask, request, render_template, flash, redirect
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector('Friends')
app.secret_key = 'Top_Secret'

@app.route('/')
def index():
	# Index route, displays index.html 
	friends = mysql.fetch("SELECT * FROM friends")
	print friends
	return render_template("index.html", friends=friends)

@app.route('/friends', methods=['POST'])
def create():
	#Route to create and friends
	print request.form
	firstName = request.form['first_name']
	lastName = request.form['last_name']
	query = "INSERT INTO Friends (first_name, last_name, created_at, updated_at) VALUES ('{}','{}', NOW(), NOW())".format(firstName, lastName)
	mysql.run_mysql_query(query)
	return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
	# Where you edit friends
	print id
	friends = mysql.fetch("SELECT * FROM friends WHERE id = {}".format(id))
	
	return render_template("edit.html", friends=friends)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	#Updating friends 
	print id
	friends = mysql.fetch("SELECT * FROM friends WHERE id = {}".format(id))
	fname = request.form['fname']
	lname = request.form['lname']
	print fname
	print lname
	query = "UPDATE Friends SET first_name='{}', last_name='{}', updated_at='NOW()' WHERE id = {}".format(fname,lname,id)
	print query
	mysql.run_mysql_query(query)
	return redirect('/friends/{}/edit'.format(id))

@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
	#Deleting friends
	friends = mysql.fetch("SELECT * FROM friends where id = {}".format(id))
	query = "DELETE FROM friends WHERE id = {}".format(id)
	mysql.run_mysql_query(query)
	return redirect('/')
app.run(debug=True)