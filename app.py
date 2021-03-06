from flask import Flask, render_template, request, redirect, url_for, jsonify
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
import pyperclip
import psutil

import time
import json
from datetime import datetime
from multiprocessing import Process, Value
from hashlib import sha256
import signal
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clippy.db'

db = SQLAlchemy(app)

@dataclass
class ClipboardItem(db.Model):
    id: int
    text: str
    length: int
    location: str
    date: str

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
            print("Copying Text...")
            add(text)
        time.sleep(0.5)

@app.route('/')
def index():
    # items = ClipboardItem.query.all()
    items = ClipboardItem.query.order_by(ClipboardItem.date.desc()).all()
    # json_items = jsonify(items)

    return render_template('index.html', items=items)
    # json_data = jsonify(items)
    # return jsonify(json_data.get_data(as_text=True))

@app.route('/json')
def post_json():
    # items = ClipboardItem.query.all()
    items = ClipboardItem.query.order_by(ClipboardItem.date.desc()).all()
    return jsonify(items)


def add(text):
    for _ in db.session.execute("SELECT * FROM clipboard_item WHERE text =:text", {"text":text }):
        # db.session.execute("DELETE FROM clipboard_item WHERE text =:text", {"text":text })
        print("Action Blocked: Entry Exists...")
        break
    else:
        print('Inserting Entry...')
        dummy = ClipboardItem(text=text, length=len(text), location="null", date=datetime.now())
        db.session.add(dummy)
        db.session.commit()

    # dummy = ClipboardItem(text=text, length=len(text), location="null", date=datetime.now())
    # db.session.add(dummy)
    # db.session.commit()

@app.route('/deleteAll', methods=['POST'])
def removeAll():
    print("Deleting All Entries...")
    db.session.execute('DELETE FROM clipboard_item')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/itemAction', methods=['POST'])
def item_actions():
    if request.method == "POST":
        # I. Delete Individual Item
        if request.form.get('action') and request.form.get('action')[:10] == 'deleteitem':
            print("Deleting Entry ID {} ...".format(request.form.get('action')[10:]))
            db.session.execute("DELETE FROM clipboard_item where id =:id", {"id":int(request.form.get('action')[10:]) })

        # II. Delete Selected Items
        elif request.form.getlist("copy_id"):
            print("Deleting Selected Entries...")
            print(request.form.getlist("copy_id"))
            ClipboardItem.query.filter(ClipboardItem.id.in_(request.form.getlist("copy_id"))).delete(synchronize_session=False)
    
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/toggle')
def toggle_listen():
    if p.status() == "stopped":
        print("Resuming Listen...")
        p.resume()
    else:
        print("Pausing Listen...")
        p.suspend()
    return redirect(url_for('index'))

def signal_handler(sig, frame):
    print("Closing Application...")
    if p and p.status() == "stopped":
        p.resume()
    sys.exit(0)

if __name__ == "__main__":
    listener = Process(target=listen, args=(pyperclip.paste().strip(),))
    listener.start()
    signal.signal(signal.SIGINT, signal_handler)
    p = psutil.Process(listener.pid)
    app.run(debug=True, use_reloader=False)
    listener.join()