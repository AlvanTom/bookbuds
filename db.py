from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
import os
from dotenv import load_dotenv

load_dotenv()

# set URI
dburi = ''
if 'RDS_HOSTNAME' in os.environ:
    # prod env
    dburi = f"postgresql://{os.environ['RDS_USERNAME']}:{os.environ['RDS_PASSWORD']}@{os.environ['RDS_HOSTNAME']}:{os.environ['RDS_PORT']}/{os.environ['RDS_DB_NAME']}"
else:
    # local env
    dburi = "postgresql://postgres:postgres@localhost:6006/postgres"

# instantiate db
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Define a basic model
class BookClub(db.Model):
    id= mapped_column(String, primary_key=True)
    name = mapped_column(String)
    date_created = mapped_column(String)
    date_modified = mapped_column(String)
    book_title = mapped_column(String)
    reading_pace = mapped_column(Integer)
    current_chapter = mapped_column(Integer)
    chapters = mapped_column(Integer)


class Comments(db.Model):
    id= mapped_column(String, primary_key=True)
    date_created = mapped_column(String)
    user = mapped_column(String)
    comment = mapped_column(String)
    # TODO: add book_club_id
    # book_club_id = mapped_column(String, db.ForeignKey('book_club.id'))
    # book_club = db.relationship('BookClub', backref='comments')


def dbFactory(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = dburi
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db
