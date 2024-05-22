from Application.Controller.Controller import *
import shutil


def creatorUserObject(userName):
    user = getUsers().filter_by(userName = userName).first()
    userId = user.userId
    songs = getSongs().filter_by(userId = userId).all()
    lyrics = getLyrics().filter_by(userId = userId).all()
    albums = getAlbums().filter_by(userId = userId).all()
    return dict(
                userType = "Creator",userName = user.userName, userId = user.userId,
                songs = dict_s(songs),lyrics = dict_l(lyrics),
                albums = dict_a(albums) , len = [len(songs) , len(lyrics) , len(albums)]
                )

def addSong(songName , file , file1 , Language):
    try:
        songId = max([i.songId for i in getSongs().all()]) + 1
    except:
        songId = 1
    file.save(str(songId))
    shutil.move(str(songId),f'Static/Songs/{songId}.mp3')
    if file1:
        file1.save(str(songId))
        shutil.move(str(songId),f'Static/Songs/{songId}.txt')
    query = insert(Songs).values(
        songName = songName , Language = Language , 
        userId = session['user']['userId'] , 
        songId = songId
        )
    exec(query)

def addLyrics(lyricsName , file , Language):
    try:
        lyricsId = max([i.lyricsId for i in getLyrics().all()]) + 1
    except:
        lyricsId = 1
    file.save(str(lyricsId))
    shutil.move(str(lyricsId),f'Static/Lyrics/{lyricsId}.txt')
    query = insert(Lyrics).values(
        lyricsName = lyricsName , Language = Language , 
        userId = session['user']['userId'],
        lyricsId = lyricsId
        )
    exec(query)

def addAlbum(albumName , Genre , songs):
    try:
        albumId = max([i.albumId for i in getAlbums().all()]) + 1
        print('here')
    except:
        albumId = 1
    query = insert(Albums).values(
        albumId = albumId , albumName = albumName ,
        Genre = Genre , Songs = '|'.join(songs),
        userId = session['user']['userId']
    )
    exec(query)

def EditAlbum(albumId , songs , name , genre):
    if name == "" and genre == "":
        query = update(Albums).where(Albums.albumId == int(albumId)).values(Songs = songs)
        exec(query)
    elif name == "":
        query = update(Albums).where(Albums.albumId == int(albumId)).values(Songs = songs , Genre = gnere)
        exec(query)
    elif genre == "":
        query = update(Albums).where(Albums.albumId == int(albumId)).values(Songs = songs , albumName = name)
        exec(query)
    else:
        query = update(Albums).where(Albums.albumId == int(albumId)).values(Songs = songs , albumName = name , Genre = genre)
        exec(query)

def EditSong(songId , name , Language):
    if name == "" and Language == "":
        pass
    elif name == "":
        query = update(Songs).where(Songs.songId == int(songId)).values(Language = gnere)
        exec(query)
    elif Language == "":
        query = update(Songs).where(Songs.songId == int(songId)).values(songName = name)
        exec(query)
    else:
        query = update(Songs).where(Songs.songId == int(songId)).values(songName = name , Language = Language)
        exec(query)

def EditLyrics(lyricsId , name , Language):
    if name == "" and Language == "":
        pass
    elif name == "":
        query = update(Lyrics).where(Lyrics.lyricsId == int(lyricsId)).values(Language = gnere)
        exec(query)
    elif Language == "":
        query = update(Lyrics).where(Lyrics.lyricsId == int(lyricsId)).values(lyricsName = name)
        exec(query)
    else:
        query = update(Lyrics).where(Lyrics.lyricsId == int(lyricsId)).values(lyricsName = name , Language = Language)
        exec(query)


def make_creator_request():
    return update(Users).where(Users.userName == session['temp']).values(Status = 1)