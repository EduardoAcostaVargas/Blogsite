from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/addBlog')
def addBlog():
    return render_template('addBlog.html')

@app.route('/Blogs')
def Blogs():
    return render_template('blogs.html')