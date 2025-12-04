from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['POSTS'] = []  # Store blogs in memory

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/addBlog', methods=['GET', 'POST'])
def addBlog():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not author or not content:
            return "All fields are required!", 400

        # Save the blog post
        app.config['POSTS'].insert(0, {
            'title': title,
            'author': author,
            'content': content
        })
        
        # Redirect to blogs page after successful submission
        return redirect(url_for('Blogs'))

    return render_template('addBlog.html')

@app.route('/Blogs', methods=['GET', 'POST'])
def Blogs():
    blogs = app.config['POSTS']  # Pass stored blogs to template
    return render_template('blogs.html', blogs=blogs)