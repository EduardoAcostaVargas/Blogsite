from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['POSTS'] = []  # Store blogs in memory
app.config['COMMENTS'] = {}  # Store comments by blog index

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
    blogs = app.config['POSTS']
    comments = app.config['COMMENTS']
    return render_template('blogs.html', blogs=blogs, comments=comments)

@app.route('/addComment/<int:blog_id>', methods=['POST'])
def add_comment(blog_id):
    commenter = request.form.get('commenter', 'Anonymous').strip()
    comment_text = request.form.get('comment', '').strip()
    
    if not comment_text:
        return "Comment cannot be empty!", 400
    
    # Initialize comments list for this blog if it doesn't exist
    if blog_id not in app.config['COMMENTS']:
        app.config['COMMENTS'][blog_id] = []
    
    # Add the comment
    app.config['COMMENTS'][blog_id].append({
        'commenter': commenter,
        'text': comment_text
    })
    
    return redirect(url_for('Blogs'))