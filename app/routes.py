from app import app
from flask import render_template

# Testing - 
# Development - 
# Production - 

# file-watcher

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')