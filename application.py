from flask import Flask, request, redirect, url_for
from db import BookClub, Comments, dbFactory
import uuid
from datetime import datetime

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

db = dbFactory(application)

# Routes
@application.route('/')
def index():
    book_clubs = BookClub.query.all()
    comments = Comments.query.all()

    # Create HTML for the book clubs list
    book_club_list = '<ul>'
    for club in book_clubs:
        book_club_list += f'''
            <li>
                <strong>{club.name}</strong> - {club.book_title}
                <br>Reading Pace: {club.reading_pace} chapters/week
                <br>Current Chapter: {club.current_chapter}/{club.chapters}
                <br>Created: {club.date_created}
            </li>'''
    book_club_list += '</ul>'

    # Create HTML for the comments list
    comment_list = '<ul>'
    for comment in comments:
        comment_list += f'<li><strong>{comment.user}</strong>: {comment.comment} ({comment.date_created})</li>'
    comment_list += '</ul>'
    
    # Create the complete HTML page
    html = f'''
    <html>
        <head>
            <title>Bookbuds</title>
            <style>
                body {{ font-family: 'Times New Roman'; margin: 40px; }}
                form {{ margin-bottom: 20px; padding: 20px; border: 1px solid #ccc; border-radius: 5px; }}
                input, select {{ margin: 5px; padding: 5px; width: 200px; }}
                button {{ padding: 5px 10px; background-color: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer; }}
                button:hover {{ background-color: #45a049; }}
                .section {{ margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <h1>Welcome to Bookbuds</h1>
            
            <div class="section">
                <h2>Create a Book Club</h2>
                <form action="/add_book_club" method="POST">
                    <input type="text" name="name" placeholder="Club Name" required><br>
                    <input type="text" name="book_title" placeholder="Book Title" required><br>
                    <input type="number" name="reading_pace" placeholder="Chapters per week" required><br>
                    <input type="number" name="chapters" placeholder="Total chapters" required><br>
                    <button type="submit">Create Book Club</button>
                </form>
            </div>

            <div class="section">
                <h2>Add a Comment</h2>
                <form action="/add_comment" method="POST">
                    <input type="text" name="user" placeholder="Your Name" required><br>
                    <textarea name="comment" placeholder="Your Comment" required style="width: 200px; height: 100px;"></textarea><br>
                    <button type="submit">Add Comment</button>
                </form>
            </div>
            
            <div class="section">
                <h2>Current Book Clubs:</h2>
                {book_club_list}
            </div>

            <div class="section">
                <h2>Comments:</h2>
                {comment_list}
            </div>
        </body>
    </html>
    '''
    return html

@application.route('/add_book_club', methods=['POST'])
def add_book_club():
    name = request.form.get('name')
    book_title = request.form.get('book_title')
    reading_pace = request.form.get('reading_pace')
    chapters = request.form.get('chapters')
    
    if name and book_title and reading_pace and chapters:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_club = BookClub(
            id=str(uuid.uuid4()),
            name=name,
            book_title=book_title,
            reading_pace=int(reading_pace),
            chapters=int(chapters),
            current_chapter=1,
            date_created=current_time,
            date_modified=current_time
        )
        db.session.add(new_club)
        db.session.commit()
    
    return redirect(url_for('index'))

@application.route('/add_comment', methods=['POST'])
def add_comment():
    user = request.form.get('user')
    comment = request.form.get('comment')
    
    if user and comment:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_comment = Comments(
            id=str(uuid.uuid4()),
            user=user,
            comment=comment,
            date_created=current_time
        )
        db.session.add(new_comment)
        db.session.commit()
    
    return redirect(url_for('index'))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
