from flask import Flask, request, redirect, render_template, url_for
from db import BookClub, Comments, dbFactory
import uuid
from datetime import datetime

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
    return render_template('home.html', book_clubs=book_clubs)

@application.route('/<bookclubid>/<name>')
def clubpage(bookclubid, name):
    #query info for bookclub homepage
    bookclub = db.session.execute(db.select(BookClub).filter_by(id=bookclubid)).scalar_one()
    return render_template('clubpage.html', bookclub=bookclub)

@application.route('/api/', methods=['POST'])
def create_book_club():
    form_data = request.form
    id = str(uuid.uuid4())
    club_name = form_data.get('bookclubname')
    book_title = form_data.get('booktitle')
    reading_pace = form_data.get('readingpace')
    chapters = form_data.get('chapters')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_club = BookClub(
        id=id,
        name=club_name,
        book_title=book_title,
        reading_pace=reading_pace,
        chapters=chapters,
        current_chapter=0,
        date_created=current_time,
        date_modified=current_time
    )
    db.session.add(new_club)
    db.session.commit()

    return id

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

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
