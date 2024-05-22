from Application.Controller.Controller import *
import os


def adminUserObject(userName):
    details = getAdmins().filter_by(userName = userName).first()
    users = getUsers().all()
    creators = getUsers().filter(Users.Status >= 1).all()
    lenCreators = len(creators)
    temp = dict_u(creators)
    creators = [[],[]]
    for i in temp:
        if i['Status'] == 1:
            creators[0].append(i)
        elif i['Status'] == 2:
            creatorSongs = getSongs().filter_by(userId = int(i['userId'])).all()
            creatorLyrics = getLyrics().filter_by(userId = int(i['userId'])).all()
            creatorAlbums = getAlbums().filter_by(userId = int(i['userId'])).all()
            i['songs'] = len(creatorSongs)
            i['lyrics'] = len(creatorLyrics)
            i['albums'] = len(creatorAlbums)
            i['totalViews'] = sum([i.totalListens for i in creatorSongs] + 
                                    [i.totalListens for i in creatorAlbums] +
                                    [i.totalReads for i in creatorLyrics])
            creators[1].append(i)
    songs = getSongs().all()
    lyrics = getLyrics().all()
    albums = getAlbums().all()
    return dict(userType = "Admin",userName = details.userName,
                users = dict_u(users),creators = creators,songs = dict_s(songs),
                lyrics = dict_l(lyrics),albums = dict_a(albums) ,
                 len = [
                    len(users) , lenCreators , len(songs) , len(lyrics) , len(albums)
                    ]
                )

def addAdmin(userName,Password):
    query = insert(Admin).values(userName = userName , Password = Password)
    exec(query)

def remUser(userName):
    query = delete(Users).where(Users.userName == userName)
    exec(query)
    session['user'] = adminUserObject(session['user']['userName'])

def remCreator(userName):
    query = update(Users).where(Users.userName == userName).values(Status = 1)
    exec(query)
    session['user'] = adminUserObject(session['user']['userName'])

def appCreator(userName):
    query = update(Users).where(Users.userName == userName).values(Status = 2)
    exec(query)
    session['user'] = adminUserObject(session['user']['userName'])

def remSong(songId):
    query = delete(Songs).where(Songs.songId == songId)
    myfile = f".\\Static\\Songs\\{songId}"
    if os.path.isfile(myfile+'.mp3'):
        os.remove(myfile+".mp3")
    if os.path.isfile(myfile+'.txt'):
        os.remove(myfile+'.txt')
    exec(query)

def remLyrics(lyricsId):
    query = delete(Lyrics).where(Lyrics.lyricsId == lyricsId)
    myfile = f".\\Static\\Lyrics\\{lyricsId}"
    if os.path.isfile(myfile+'.txt'):
        os.remove(myfile+".txt")
    exec(query)

def remAlbum(albumId):
    query = delete(Albums).where(Albums.albumId == albumId)
    exec(query)
