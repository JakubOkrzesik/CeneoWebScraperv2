from flask import render_template
from app import app

@app.route('/')
@app.route('/index/<name>')
def index(name='czifkif'):
    return render_template('index.html', text=name)