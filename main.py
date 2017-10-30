from flask import Flask, request, redirect, render_template,session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:1234@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdkkjdlaslkdjfllsjakdjlksjk'

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blogpost', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password



class Blogpost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

@app.before_request
def require_login():
    allowed_routes=['login','validate_input','index','blogpost']                                           #user does not need to log in to see these routes
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/index', methods=['POST','GET'])
def index():    #show a list of all users which links to their blog posts!
    bloggers = User.query.all()
    return render_template('index.html', bloggers=bloggers)

@app.route('/signup', methods=['POST','GET'])
def validate_input():
    if request.method == 'POST':
        username = request.form['username']
        username_error = ''
        password = request.form['password']
        password_error = ''
        verify = request.form['verify']
        verify_error = ''

        if " " in username or len(username) < 3 or len(username)> 20:
            username_error = 'Not a valid username'
            username = ''
        else:
            username = username

        if " " in password:
            password_error = 'Not a valid password'
        if len(password) < 3 or len(password)> 20:
            password_error='Not a valid password'
        if verify != password:
            verify_error="passwords do not match - please re-enter"
        else:
            password = password

        if not username_error and not password_error and not verify_error:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            else:
                flash ('User already exists','error')    
        else:
            return render_template('signup.html',username_error=username_error,
                password_error=password_error,verify_error=verify_error, 
                username=username,
                password='')

    return render_template('signup.html') 

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()   
        if user and user.password == password:                  #if the user exists and the password for that user is correct then
            session['username'] = username                      #start a session for that user and
            return redirect('/newpost')                         #redirect them to the page to enter a new blog post
        if user and user.password != password:                  #if the user exists and the password for that user is not correct then
            flash('Password is incorrect!', 'error')            #show an error message that the password is not correct
        else:                                                   #if the two cases above do not apply, the user does not exist (is None) so
            flash('User does not exist', 'error')               #show an error message that the user does not exist and
    return render_template('login.html')                        #redirect the errors to the login page

@app.route('/blog', methods=['POST', 'GET'])
def blogpost():
    if "id" in request.args:                            #id 
        id = request.args['id']         #sets the variable id = requests an item "id" from the dictionary args
        posts = Blogpost.query.filter_by(id=id).first() #set the variable posts to return the id - first one
        posts = [posts]                         #turns variable posts into a list (for the blogmain template page)         
        return render_template('blogview.html', title="Blogz" ,posts = posts) #returns the template blogmain.html with blog title and the posts variable value
    elif "username" in request.args:
       user_id=request.args['username'] 
       posts = Blogpost.query.filter_by(owner_id=user_id).all()
       return render_template('blogview.html', title = "Blogz",posts=posts)
    else:                                                 #if the try statement does not work, this will execute
        posts = Blogpost.query.all()                        # returns a list of all the blogs
        users = User.query.all()
        return render_template('blogmain.html',title="Blogz", posts = posts, users=users)  #returns template blogmain.html with a list of all blogs
    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    blog_owner= User.query.filter_by(username=session['username']).first()

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
            new_post = Blogpost(blog_title, blogpost,blog_owner)   #if no errors, the following is executed
            db.session.add(new_post)                    #creates a "staging" of the blogpost entry
            db.session.commit()                         #commits the entry to the database
            id = new_post.id                            #creates variable id from the new_post to use in the redirect stmt
            posts = [new_post]                          #turns the variable posts in into a list, which is iterable

            owner = [blog_owner]                        #turns variable owner into iterable list
            return redirect('/blog?id='+str(id))        #to redirect to the main blog page and display the individual blog
            return render_template('blogview.html', id=id, title = "Blogz", posts = posts)     #returns to main blog page -want to display the individual blog page

    return render_template('newpost.html')          #returns the newpost templ.ate

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/index')


if __name__ == '__main__':
    app.run()