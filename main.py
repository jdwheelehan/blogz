from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:18701@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(240))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(username=session['username']).first()
    return redirect('/blog')


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

@app.route('/blog', methods=['POST', 'GET'])
def blog_display():
    if request.args:
        post_id = request.args.get('id')
        posts = Blog.query.filter_by(id=post_id).all()
        return render_template('display.html',posts=posts)
    else:
        posts = Blog.query.all()
        return render_template('display.html',posts=posts)



@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        title_error = ''
        body_error = ''

        if title_name == '':
            title_error = 'Please enter a title'
        if body_name == '':
            body_error = 'Please enter a post'
        
        if not title_error and not body_error:
            new_post = Blog(title_name, body_name, owner)
            db.session.add(new_post)
            db.session.commit()
            new_id = str(new_post.id)
            return redirect('/blog?id='+new_id)
        else:
            return render_template('newpost.html', title = title_name, body = body_name, 
                title_error = title_error, body_error = body_error,)
    
    return render_template('newpost.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            
            # TODO - "remember" that the user has logged in
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            # TODO - explain why login failed
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            # TODO - "remember" the user
            session['username'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

if __name__ == '__main__':
    app.run()