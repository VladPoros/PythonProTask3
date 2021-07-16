from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)


def BD(execute):
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute(execute)
    sections = cursor.fetchall()
    connection.close()
    return render_template('index.html', sections=sections)

def BD_amend (execute, values):
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute(execute, values)
    connection.commit()
    connection.close()
    return redirect('/info')

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
    return BD("SELECT * FROM sections")


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
        if not added_title or not added_description:
            return 'You don`t enter the title or description'
        else:
            values = (added_title, added_description)
            return BD_amend("""INSERT INTO sections (title, description, date) 
            VALUES(?, ?, '15/07')""", values)


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
            if not updated_title:
                values = (updated_description, id)
                return BD_amend("""UPDATE sections SET description = ?
                            WHERE id = ?""", values)
            if not updated_description:
                values = (updated_title, id)
                return BD_amend("""UPDATE sections SET title = ?
                            WHERE id = ?""", values)
            else:
                values = (updated_title, updated_description, id)
                return BD_amend("""UPDATE sections SET title = ?, description = ?
                WHERE id = ?""", values)


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
            values = (id)
            return BD_amend("DELETE FROM sections WHERE id = ?", values)


if __name__ == '__main__':
    app.run(debug=True)