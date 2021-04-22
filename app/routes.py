from app import app

# Testing - 
# Development - 
# Production - 

# file-watcher

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/contact')
def contact():
    return "This is the contact page!"

@app.route('/blog')
def blog():
    return 'This is the new blog page!'