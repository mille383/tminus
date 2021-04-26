from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import Post

# Testing - 
# Development - 
# Production - 

# file-watcher

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        p = Post(email='derekh@codingtemple.com', body=request.form.get('body_text'))
        db.session.add(p)
        db.session.commit()
        flash('Blog post created successfully')
        return redirect(url_for('home'))
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')