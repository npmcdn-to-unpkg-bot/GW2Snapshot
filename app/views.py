from app import app
from flask import Blueprint, render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('templates/timeline.html')
