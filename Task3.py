from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

'''
connection = sqlite3.connect('blog.sqlite')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS sections (id integer primary key AUTOINCREMENT, 
title varchar(200), description varchar(200), date int)""")
connection.commit()
connection.close()
'''

@app.route('/')
def start_page():
    return 'Hello user'


@app.route('/info/')
def info_page():
    '''
    Main page with all data in SQLite
    Use this page after redirect each action
    Also use index html for templates
    '''
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sections")
    sections = cursor.fetchall()
    connection.close()
    return render_template('index.html', sections=sections)


@app.route('/add/', methods=('GET', 'POST'))
def add_page():
    '''
    When we in GET, we use form with input data
    for our POST, then this data we check is it empty or not
    and after this we use SQLite with INSERT for our input values
    '''
    if request.method == 'GET':
        return '''<form method="POST">Enter the title and description: <input name="title">, 
        <input name="description"><input type="submit"></form>'''
    else:
        added_title = request.form['title']
        added_description = request.form['description']
        if not added_title and not added_description:
            return 'You don`t enter the title and description'
        if not added_title:
            return 'You don`t enter the title'
        if not added_description:
            return 'You don`t enter the description'

        else:
            connection = sqlite3.connect('blog.sqlite')
            cursor = connection.cursor()
            values = (added_title, added_description)
            cursor.execute("""INSERT INTO sections (title, description, date) 
            VALUES(?, ?, '15/07')""", values)
            connection.commit()
            connection.close()
            return redirect('/info')


@app.route('/edit/', methods=('GET', 'POST'))
def edit_page():
    '''
    When we in GET, we use form with input data
    for our POST, then this data we check is it empty or not
    and after this we use SQLite with UPDATE for our input values 
    '''
    if request.method == 'GET':
        return '''<form method="POST">Enter the id, title, description: <input name="id">, <input name="title">,
        <input name="description"><input type="submit"></form>'''
    else:
        id = request.form['id']
        updated_title = request.form['title']
        updated_description = request.form['description']
        if not id:
            return 'You don`t enter the id or error id'
        else:
            connection=sqlite3.connect('blog.sqlite')
            cursor = connection.cursor()
            if not updated_title:
                values = (updated_description, id)
                cursor.execute("""UPDATE sections SET description = ?
                            WHERE id = ?""", values)
                connection.commit()
                connection.close()
                return redirect('/info')
            if not updated_description:
                values = (updated_title, id)
                cursor.execute("""UPDATE sections SET title = ?
                            WHERE id = ?""", values)
                connection.commit()
                connection.close()
                return redirect('/info')
            else:
                values = (updated_title, updated_description, id)
                cursor.execute("""UPDATE sections SET title = ?, description = ?
                WHERE id = ?""", values)
                connection.commit()
                connection.close()
                return redirect('/info')


@app.route('/delete/', methods=('GET', 'POST'))
def delete_page():
    '''
    When we in GET, we use form with input data
    for our POST, then this data we check is it empty or not
    and after this we use SQLite with DELETE for our input value
    '''
    if request.method == 'GET':
        return '<form method="POST">Enter the id: <input name="id"><input type="submit"></form>'
    else:
        id = request.form['id']
        if not id:
            return 'You don`t enter the id'
        else:
            connection = sqlite3.connect('blog.sqlite')
            cursor = connection.cursor()
            values = (id)
            cursor.execute("DELETE FROM sections WHERE id = ?", values)
            connection.commit()
            connection.close()
            return redirect('/info')


if __name__ == '__main__':
    app.run(debug=True)
