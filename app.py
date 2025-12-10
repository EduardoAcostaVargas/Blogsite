from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

user_posts = db.Table('user_posts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    liked_posts = db.relationship('Post', secondary=user_posts, backref=db.backref('liked_by', lazy='dynamic'))
    
   
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    commenter = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
   
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


with app.app_context():
    db.create_all()

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

        
        new_post = Post(title=title, author=author, content=content)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('Blogs'))

    return render_template('addBlog.html')

@app.route('/Blogs', methods=['GET'])
def Blogs():
    blogs = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blogs.html', blogs=blogs)

@app.route('/addComment/<int:blog_id>', methods=['POST'])
def add_comment(blog_id):
    commenter = request.form.get('commenter', 'Anonymous').strip()
    comment_text = request.form.get('comment', '').strip()
    
    if not comment_text:
        return "Comment cannot be empty!", 400
    
    post = Post.query.get_or_404(blog_id)
    
    new_comment = Comment(text=comment_text, commenter=commenter, post_id=blog_id)
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('Blogs'))

@app.route('/database')
def database():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('database.html', posts=posts, comments=comments, users=users)

@app.route('/deletePost/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('database'))

@app.route('/deleteComment/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('database'))

@app.route('/clearDatabase')
def clear_database():
    Comment.query.delete()
    Post.query.delete()
    User.query.delete()
    db.session.commit()
    return redirect(url_for('database'))

if __name__ == '__main__':
    app.run(debug=True)