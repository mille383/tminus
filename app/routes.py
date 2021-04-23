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
    Post._list.clear()
    p1 = Post(1, 'https://picsum.photos/1000/500', 'derekh@codingtemple.com', 'First Blog Post', 'This is the body of the First Blog Post')
    p2 = Post(2, 'https://picsum.photos/1000/500', 'samd@codingtemple.com', 'Second Blog Post', 'This is the body of the Second Blog Post')
    p3 = Post(3, 'https://picsum.photos/1000/500', 'samd@codingtemple.com', 'Third Blog Post', 'This is the body of the Third Blog Post')
    context = {
        'posts': [p.to_dict() for p in Post._list]
    }
    return render_template('blog.html', **context)