from __future__ import with_statement

import os
import sqlite3
from flask import Flask, jsonify, request, session, g, redirect, url_for,\
    abort, render_template, flash


from contextlib import closing



# configuration
DATABASE = "./db/flask_db.db"
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.debug=True

import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.load_cert_chain(certfile="localhost.crt", keyfile='localhost.key')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])




@app.route('/post/<int:post_id>')
def show_post(post_id):
    return "Post %d" % post_id

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s ' % username


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return subpath


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    return jsonify({'class_id' : 'IMAGE_NET_XXX', 'class_name':'Cat'})


'''
데이터베이스 생성 :
그냥 아래로 터미널에서 실행해도 되고,

    sqlite3 db/flask_db.db < schema.sql

아래와 같이 코드로 생성할 수도 있다.
'''
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            sqlstr = f.read().decode('utf-8')
            db.cursor().executescript(sqlstr)
        db.commit()


"""
우리는 현재 사용중인 데이터베이스 커넥션을 특별하게 저장한다.
Flask 는 g 라는 특별한 객체를 우리에게 제공한다.
이 객체는 각 함수들에 대해서 오직 한번의 리퀘스트에 대해서만 유효한 정보를 저장하하고 있다.
쓰레드환경의 경우 다른 객체에서 위와 같이 사용 할경우 작동이 보장되지 않기 때문에 결코 사용해서는 안된다.
"""
@app.before_request
def before_request():
    print("before_request")
    g.db=connect_db()


@app.teardown_request
def teardown_request(exception):
    print("teardown_request")
    g.db.close()



"""
step 5 : 뷰 함수들

"""

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=["POST"])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values(?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))






if __name__ == '__main__':
    app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)