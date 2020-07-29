from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pyperclip

import time
from datetime import datetime
# import threading
from multiprocessing import Process, Value
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clippy.db'

db = SQLAlchemy(app)

class ClipboardItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(9999), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(2083))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())


def get_hash(text):
    return sha256(text.encode('utf-8')).hexdigest()

def listen(text):
    while True:
        check = pyperclip.paste().strip()
        if check != text:
            text = check
            add(text)
            print(text)
        time.sleep(0.5)

@app.route('/')
def index():
    items = ClipboardItem.query.all()
    # threading.Thread(target=listen).start()

    return render_template('index.html', items=items)

def add(text):
    for _ in db.session.execute("SELECT * FROM clipboard_item WHERE text LIKE '{}'".format(text)):
        db.session.execute("DELETE FROM clipboard_item WHERE text LIKE '{}'".format(text))
        print("Updating Entry...")
        break
    else:
        print('Inserting Entry...')

    dummy = ClipboardItem(text=text, length=len(text), location="null", date=datetime.now())
    db.session.add(dummy)
    db.session.commit()

@app.route('/deleteAll', methods=['POST'])
def removeAll():
    db.session.execute('DELETE FROM clipboard_item')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def remove():
    text = request.form['entry_id']
    db.session.execute("DELETE FROM clipboard_item where text LIKE '{}'".format(text))
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == "__main__":
    listener = Process(target=listen, args=(pyperclip.paste().strip(),))
    listener.start()
    app.run(debug=True, use_reloader=False)
    listener.join()