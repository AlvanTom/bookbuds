from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# Configure SQLAlchemy
if 'RDS_HOSTNAME' in os.environ:
    # prod env
    application.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}:{os.environ['RDS_PORT']}/{os.environ['RDS_DB_NAME']}"
else:
    # local env
    application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:6006/postgres"

application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy with the Flask app
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(application)

# Define a basic model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create all database tables
with application.app_context():
    db.create_all()

# Routes
@application.route('/')
def index():
    users = User.query.all()

    # Create HTML for the user list
    user_list = '<ul>'
    for user in users:
        user_list += f'<li>{user.username} - {user.email}</li>'
    user_list += '</ul>'
    
    # Create the complete HTML page
    html = f'''
    <html>
        <head>
            <title>Bookbuds</title>
            <style>
                body {{ font-family: 'Times New Roman'; margin: 40px; }}
                form {{ margin-bottom: 20px; }}
                input {{ margin: 5px; padding: 5px; }}
                button {{ padding: 5px 10px; }}
            </style>
        </head>
        <body>
            <h1>Welcome to Bookbuds</h1>
            
            <form action="/add_user" method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="email" name="email" placeholder="Email" required>
                <button type="submit">Add User</button>
            </form>
            
            <h2>Current Users:</h2>
            {user_list}
        </body>
    </html>
    '''
    return html

@application.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    
    if username and email:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
    
    return redirect(url_for('index'))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
