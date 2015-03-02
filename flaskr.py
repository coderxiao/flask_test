import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash
from contextlib import	closing

#conf
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create app
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])


#create database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql',mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()


@app.teardown_request
def teardown_request(e):
	db = getattr(g, 'db',None)
	if db is not None:
		db.close()
	g.db.close()



#test view
@app.route('/1')
def testview():
	#return str(dir(connect_db().execute("insert into entries (title,text) values ('test','test')")))
	#connect_db().excute("insert into entries (title,text) values ('test','test)")
	#return 'OK'
	pass


#viewfun
@app.route('/')
def show_entries():
	db = connect_db()
	cur = g.db.execute('select  title ,text from entries order by id desc')
	entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html',entries=entries)


@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title ,text) values (? ,?)',[request.form['title'],request.form['text']])
	g.db.commit()
	flash('OK')
	return redirect(url_for('show_entries'))


@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'forbid uname'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'error password'
		else:
			session['logged_in'] = True
			flash = 'login sucessful'
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('logged out')
	return redirect(url_for('show_entries'))


if __name__ == '__main__':
	app.run()