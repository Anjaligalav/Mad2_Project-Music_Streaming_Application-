from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from marshmallow import fields
from datetime import datetime
from sqlalchemy import event

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

#---------------------------------------------User---------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.Text, nullable=False,unique = True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), default="User")  # Default role is "User"
    last_visit_time = db.Column(db.DateTime)
    album = db.relationship("Album",backref = "album")
    song = db.relationship("Songs",backref = "User")

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

@event.listens_for(User, 'after_update')
def update_last_visit_time(mapper, connection, target):
    target.last_visit_time = datetime.now()

class Userschema(ma.Schema):
    class Meta():
        fields = ('id','username','email','role')

user_shema = Userschema()
user_shemas = Userschema(many=True)
#----------------------Album-------------------------------------------------
class Album(db.Model):
    a_id = db.Column(db.Integer, autoincrement = True ,primary_key = True)
    a_name = db.Column(db.String(30), nullable = False)
    artist = db.Column(db.String(30), nullable = False)
    genre = db.Column(db.String(30), nullable = False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    songs = db.relationship("Songs", backref = "company")

    def __init__(self,a_name,artist,genre,user):
        self.a_name=a_name
        self.artist=artist
        self.genre=genre
        self.user=user

class Albumschema(ma.Schema):
    class Meta():
        fields=('a_id','a_name','artist','genre','user')
    
album_schema = Albumschema()
album_schemas = Albumschema(many=True)

#---------------------------------Songs-----------------------------------------------
class Songs(db.Model):
    s_id = db.Column(db.Integer, autoincrement = True ,primary_key = True)
    s_name = db.Column(db.String(30), nullable = False)
    lyrics = db.Column(db.Text,nullable = False)
    date = db.Column(db.Date,nullable = False)
    rating = db.Column(db.Integer,default=0)
    songMP3 = db.Column(db.Text,nullable=False)
    rate = db.relationship("Rating",backref = "song")
    album_id = db.Column(db.Integer, db.ForeignKey("album.a_id"))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self,s_name,lyrics,date,rating,songMP3,album_id,user):
        self.s_name=s_name
        self.lyrics=lyrics
        self.date=date
        self.rating=rating
        self.songMP3=songMP3
        self.album_id=album_id
        self.user=user
    
class Songschema(ma.Schema):
    class Meta():
        fields=('s_id','s_name','lyrics','date','rating','songMP3','album_id','user')
    
song_schema = Songschema()
song_schemas = Songschema(many=True)

#---------------------------------------PlayList-----------------------------------------------
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable = False)
    name = db.Column(db.String(100),nullable = False)
    song_ids = db.Column(db.String)

    def __init__(self,username,name,song_ids):
        self.username=username
        self.name=name
        self.song_ids=song_ids

class PlayListschema(ma.Schema):
    class Meta():
        fields =('id','username','name','song_ids')

play_schema = PlayListschema()
play_schemas = PlayListschema(many=True)


#------------------------------------Rating----------------------------------------------------
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer,nullable = False)
    rating = db.Column(db.Integer,default=0)
    s_id = db.Column(db.Integer, db.ForeignKey("songs.s_id"))

    def __init__(self,u_id,rating,s_id):
        self.u_id = u_id
        self.rating=rating
        self.s_id=s_id

class Ratingschema(ma.Schema):
    class Meta():
        fields = ('id','u_id','rating','s_id')
    
rating_schema=Ratingschema()
rating_schemas = Ratingschema(many=True)

    
        