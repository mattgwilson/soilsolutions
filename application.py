from flask import Flask
from flask import request
from flask import render_template
import sqlite3

application = Flask(__name__)


@application.route('/')
def handle_splash():
    return render_template('splash.html')


@application.route('/test')
def test():
    conn = sqlite3.connect('soilsolutions205.db')
    c = conn.cursor()
    create_table()
    c.execute('''INSERT OR IGNORE INTO soil_data (id,moisture,water) VALUES(?,?,?)''', ('test','test','test'))
    conn.commit()
    conn.close()
    return 'Test'


@application.route('/input', methods=['POST'])
def handle_input():
    if not request.form['moisture'] or not request.form['water'] or not request.form['id']:
        return 'Invalid parameters', 418
    conn = sqlite3.connect('soilsolutions205.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO soil_data (id,moisture,water) VALUES(?,?,?)''', (request.form['id'], request.form['moisture'], request.form['water']))
    c.execute('''UPDATE soil_data SET moisture=? WHERE id=?''', (request.form['moisture'], request.form['id']))
    c.execute('''UPDATE soil_data SET water=? WHERE id=?''', (request.form['water'], request.form['id']))
    conn.commit()
    conn.close()
    return 'Success', 200


@application.route('/get', methods=['GET'])
def handle_get():
    if not request.args['id']:
        return 'Invalid parameters', 418
    conn = sqlite3.connect('soilsolutions205.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM soil_data WHERE id=? LIMIT 1''', (request.args['id'],))
    data = c.fetchone()
    conn.close()
    if data:
        return render_template('dataview.html', id=data[0], moisture=data[1], water=data[2])
    return 'No data'


def create_table():
    try:
        conn = sqlite3.connect('soilsolutions205.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE soil_data (id text, moisture text, water text)''')
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        pass

"""Help from John Gibson(Wustl class of 2020) was used in the writing of this code)"""


if __name__ == '__main__':
    application.run()
