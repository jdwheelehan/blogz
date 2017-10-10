from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.String(240))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body

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
            new_post = Blog(title_name, body_name)
            db.session.add(new_post)
            db.session.commit()
            new_id = str(new_post.id)
            return redirect('/blog?id='+new_id)
        else:
            return render_template('newpost.html', title = title_name, body = body_name, 
                title_error = title_error, body_error = body_error,)
    
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()