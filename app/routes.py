from app import app
from flask import render_template
from app.models import Post

# Testing - 
# Development - 
# Production - 

# file-watcher

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    context = {
        'help': 'yes',
        'page': 124567,
        'yellow': 'jaune'
    }
    return render_template('contact.html', **context)

@app.route('/blog')
def blog():
    context = {
        'posts': [p.to_dict() for p in Post.query.all()]
    }
    return render_template('blog.html', **context)