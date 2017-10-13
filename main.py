from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1024))

    def __init__(self, title, body):
        self.title = title
        self.body = body


    

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        blog_title = request.form['title']
        if  not blog_name or not blog_title:
            flash('Fill in Body', 'body')
            
            flash('Provide Blog title', 'title')
            return render_template ('newpost.html')   

        new_blog = Blog(blog_title,blog_name)
        db.session.add(new_blog)
        db.session.commit()
        blogID = str(new_blog.id)
        return redirect("/blog?id="+blogID)
        
    else:
        return render_template ('newpost.html')


@app.route('/blog', methods=['GET'])
def main():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if blog_id:
        blog_post = Blog.query.filter(Blog.id == blog_id).first()
        return render_template('blog.html', blog = blog_post)
    else:
        return render_template("main.html",  posts=blogs)


     
    




#verify form fields
#redirect to main
#show errors




#@app.route('/delete-task', methods=['POST'])
#def delete_task():

    #task_id = int(request.form['task-id'])
    #task = Task.query.get(task_id)
    #task.completed = True
    #db.session.add(task)
    #db.session.commit()

    #return redirect('/')


if __name__ == '__main__':
    app.run()
