from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:abc123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdkkjdlaslkdjfllsjakdjlksjk'


class Blogpost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/blog', methods=['POST', 'GET'])
def blogpost():
    #displays all the blog posts
    if request.method == 'POST':    #this does not do anything because this route is always GET
        title = request.form['title'] 
        body = request.form['body']
        blog_post = Blogpost(title, body)
    
     
    try:                            #try the following argument and will execute if it works, if not, it will go to except stmt
        id = request.args['id']         #sets the variable id = requests an item "id" from the dictionary args
        posts = Blogpost.query.filter_by(id=id).first() #set the variable posts to return the id - first one
        posts = [posts]                                 #turns variable posts into a list (for the templates page)
        return render_template('blogmain.html', title="Build a Blog",posts = posts) #returns the template blogmain.html with title Build a Blog, and the posts variable value
    except:                                                 #if the try statement does not work, this will execute
        posts = Blogpost.query.all()                        # returns a list of all the blogs
        return render_template('blogmain.html',title="Build a Blog", posts = posts)  #returns template blogmain.html with a list of all blogs
    

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':                #if request method is POST, the following statements are executed
        blog_title = request.form['title']      #sets the variable blog_title from the template
        blogpost = request.form['body']         #sets the variable blogpost from the template
        # Verify title and body are not empty
        #if either is empty return an error message
        #redirect ? to post to new post page        
        if blog_title == "":                    #if no title is entered, error message is returned
           session['blog_title'] = blog_title
           flash("Please fill in the title",'error')
        if blogpost == "":                      # if no body is entered, error message is returned
            session['blogpost']= blogpost       
            flash("Please fill in the body",'error')
            return redirect('/newpost')        #redirects to /newpost page
        else:     
            new_post = Blogpost(blog_title, blogpost)   #if no errors, the following is executed
            db.session.add(new_post)                    #creates a "staging" of the blogpost entry
            db.session.commit()                         #commits the entry to the database

    return render_template('newpost.html')          #returns the newpost template



    
if __name__ == '__main__':
    app.run()