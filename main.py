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
    try:                            #try the following argument and will execute if it works, if not, it will go to except stmt
        id = request.args['id']         #sets the variable id = requests an item "id" from the dictionary args
        posts = Blogpost.query.filter_by(id=id).first() #set the variable posts to return the id - first one
        posts = [posts]                         #turns variable posts into a list (for the blogmain template page)         
        return render_template('blogview.html', title="Build a Blog" ,posts = posts) #returns the template blogmain.html with blog title and the posts variable value
    except:                                                 #if the try statement does not work, this will execute
        posts = Blogpost.query.all()                        # returns a list of all the blogs
        return render_template('blogmain.html',title="Build a Blog", posts = posts)  #returns template blogmain.html with a list of all blogs
    

@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':                #if request method is POST, the following statements are executed
        blog_title = request.form['title']      #sets the variable blog_title from the template
        blogpost = request.form['body']         #sets the variable blogpost from the template
        if blog_title == "" and blogpost == "":
            flash("Please fill in the title and body", 'error')
            return render_template('newpost.html')
        if blog_title == "":                    #if no title is entered, error message is returned
            flash("Please fill in the title",'error')
            return render_template('newpost.html', body = blogpost)
        if blogpost == "":                      # if no body is entered, error message is returned
            # session['blogpost']= blogpost       
            flash("Please fill in the body",'error')
            return render_template('newpost.html', title = blog_title)
        else:
            new_post = Blogpost(blog_title, blogpost)   #if no errors, the following is executed
            db.session.add(new_post)                    #creates a "staging" of the blogpost entry
            db.session.commit()                         #commits the entry to the database
            id = new_post.id                            #creates variable id from the new_post to use in the redirect stmt
            posts = [new_post]                          #turns the variable posts in into a list, which is iterable
            return redirect('/blog?id='+str(id))        #to redirect to the main blog page and display the individual blog
            return render_template('blogview.html', id=id, title = "Build a Blog", posts = posts)     #returns to main blog page -want to display the individual blog page

    return render_template('newpost.html')          #returns the newpost templ.ate
    
    
    
if __name__ == '__main__':
    app.run()