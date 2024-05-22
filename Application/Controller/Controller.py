from Application.Model import *
from flask import session


def validateUser(userName , Password):
    for i in getUsers().all():
        if i.userName == userName and i.Password == Password:
            return True
    return False

def validateCreator(userName , Password):
    for i in getUsers().all():
        if i.userName == userName and i.Password == Password:
            return i.Status
    return False

def validateAdmin(userName , Password):
    for i in getAdmins().all():
        if i.userName == userName and i.Password == Password:
            return True
    return False

def isAvailable(userName):
    for i in getUsers().all():
        if i.userName == userName:
            return False
    return True

def isLogged():
    if 'user' in session:
        return True
    return False

def validate(text):
    for i in text:
        if not(i.isalnum() or i == ' '):
            return False
    return True

def addUser(userName , Password):
    exec(insert(Users).values(userName = userName , Password = Password , Status = 0))

def dict_u(objs):
    li = []
    for i in objs:
        d = {"userId" :i.userId , "userName" : i.userName,
            "Views" : i.Views , "Status" : i.Status}
        li.append(d)
    return li

def dict_s(objs):
    li = []
    for i in objs:
        d = {"songId" : i.songId , "songName" : i.songName,
             "userId" : i.userId , "songRating" : i.songRating,
             "totalRates" : i.totalRates , "totalListens" : i.totalListens,
             "Language" : i.Language}
        li.append(d)
    return li

def dict_l(objs):
    li = []
    for i in objs:
        d = {"lyricsId" : i.lyricsId , "lyricsName" : i.lyricsName,
             "userId" : i.userId , "lyricsRating" : i.lyricsRating,
             "totalRates" : i.totalRates , "totalReads" : i.totalReads,
             "Language" : i.Language}
        li.append(d)
    return li

def dict_p(objs):
    li = []
    for i in objs:
        d = {"playlistId" : i.playlistId , "playlistName" : i.playlistName,
             "userId" : i.userId , "Songs" : i.Songs}
        li.append(d)
    return li

def dict_a(objs):
    li = []
    for i in objs:
        d = {"albumId" : i.albumId , "albumName" : i.albumName,
             "userId" : i.userId , "albumRating" : i.albumRating,
             "Genre" : i.Genre , "Songs" : i.Songs,
             "totalRates" : i.totalRates , "totalListens" : i.totalListens}
        li.append(d)
    return li

def dict_r(objs):
    li = []
    for i in objs:
        li.append({ "ratingId" : i.ratingId , "userId" : i.userId ,
        "objectId" : i.objectId , "Rating" : i.Rating,
        "ratingType" : i.ratingType
        })
    return li