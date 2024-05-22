from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select,insert,update
from sqlalchemy import desc,delete
import os

db = SQLAlchemy()


#Tables

class Admin(db.Model):
    __tablename__ = "Admin"
    userName = db.Column(db.String , nullable = False , primary_key = True)
    Password = db.Column(db.String , nullable = False)

class Users(db.Model):
    __tablename__ = "Users"
    userId = db.Column(db.Integer , primary_key = True)
    userName = db.Column(db.Integer , nullable = False , unique = True)
    Password = Password = db.Column(db.String , nullable = False)
    Status = db.Column(db.Integer , nullable = False)
    Views = db.Column(db.Integer , nullable = False , default = 0)
    

class Songs(db.Model):
    __tablename__ = "Songs"
    songId = db.Column(db.Integer , primary_key = True)
    songName = db.Column(db.String , nullable = False)
    userId = db.Column(db.Integer , db.ForeignKey("Users.userId"))
    songRating = db.Column(db.Float , default = 0)
    totalRates = db.Column(db.Integer , default = 0)
    totalListens = db.Column(db.Integer , default = 0)
    Language = db.Column(db.String)

class Lyrics(db.Model):
    __tablename__ = "Lyrics"
    lyricsId = db.Column(db.Integer , primary_key = True)
    lyricsName = db.Column(db.String , nullable = False)
    userId = db.Column(db.Integer , db.ForeignKey("Users.userId"))
    lyricsRating = db.Column(db.Float , default = 0)
    totalRates = db.Column(db.Integer , default = 0)
    totalReads = db.Column(db.Integer , default = 0)
    Language = db.Column(db.String)

class Playlists(db.Model):
    __tablename__ = "Playlists"
    playlistId = db.Column(db.Integer , primary_key = True)
    playlistName = db.Column(db.String , nullable = False)
    userId = db.Column(db.Integer , db.ForeignKey("Users.userId"))
    Songs = db.Column(db.String)

class Albums(db.Model):
    __tablename__ = "Albums"
    albumId = db.Column(db.Integer , primary_key = True)
    albumName = db.Column(db.String , nullable = False)
    Genre = db.Column(db.String , nullable = False)
    userId = db.Column(db.Integer , db.ForeignKey("Users.userId"))
    Songs = db.Column(db.String)
    albumRating = db.Column(db.Float , default = 0)
    totalRates = db.Column(db.Integer , default = 0)
    totalListens = db.Column(db.Integer , default = 0) 

class Rating(db.Model):
    __tablename__ = "Rating"
    ratingId = db.Column(db.Integer , primary_key = True)
    userId = db.Column(db.Integer , db.ForeignKey("Users.userId"))
    objectId = db.Column(db.Integer , nullable = False)
    Rating = db.Column(db.Integer)
    ratingType = db.Column(db.String)


#functions

#get
def getUsers():
    return Users.query

def getAdmins():
    return Admin.query

def getSongs():
    return Songs.query

def getPlaylists():
    return Playlists.query

def getLyrics():
    return Lyrics.query

def getAlbums():
    return Albums.query

def getRating():
    return Rating.query

#execute
def exec(query):
    db.session.execute(query)
    db.session.commit()


