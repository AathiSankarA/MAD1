from Application.Controller.Controller import *


def guestUserObject(userName):
    details = getUsers().filter_by(userName = userName).first()
    songs = getSongs().order_by((Songs.songName)).all()
    albums = getAlbums().order_by(desc(Albums.albumRating)).all()
    playlists = getPlaylists().filter_by(userId = details.userId).all()
    rating = getRating().filter_by(userId = details.userId).all()
    lyrics = getLyrics().order_by(desc(Lyrics.lyricsRating)).all()
    session['albumViewed'] = 0
    session['names'] = []
    return dict(
                userType = "Guest",userName = details.userName,songs = dict_s(songs),
                playlists = dict_p(playlists) , userId = details.userId ,
                albums = dict_a(albums) , rating = dict_r(rating) ,lyrics = dict_l(lyrics)
                )

def updateRating(objectId , value , Type):
    query = insert(Rating).values(
        objectId = objectId , ratingType = Type ,
        Rating = value , userId = session['user']['userId']
        )
    exec(query)
    if Type == 'Song':
        song = getSongs().filter_by(songId = objectId).all()[0]
        query = update(Songs).where(
            Songs.songId == objectId
            ).values(
                songRating = (song.songRating * song.totalRates+value)/(song.totalRates+1),
                totalRates = song.totalRates+1
                )
        exec(query)
    if Type == 'Lyrics':
        lyrics = getLyrics().filter_by(lyricsId = objectId).all()[0]
        query = update(Lyrics).where(
            Lyrics.lyricsId == objectId
            ).values(
                lyricsRating = (lyrics.lyricsRating * lyrics.totalRates+value)/(lyrics.totalRates+1),
                totalRates = lyrics.totalRates+1
                )
        exec(query)
    if Type == 'Album':
        albums = getAlbums().filter_by(albumId = objectId).all()[0]
        print('ok')
        query = update(Albums).where(
            Albums.albumId == objectId
            ).values(
                albumRating = (albums.albumRating * albums.totalRates+value)/(albums.totalRates+1),
                totalRates = albums.totalRates+1
                )
        exec(query)
    session['user'] = guestUserObject(session['user']['userName'])

def updateViews(objectId , Type):
    if Type == 'Song':
        song = getSongs().filter_by(songId = objectId).all()[0]
        query = update(Songs).where(
            Songs.songId == objectId
            ).values(
                totalListens = song.totalListens + 1
                )
        exec(query)
        user = getUsers().filter_by(userId = session['user']['userId']).all()[0]
        query = update(Users).where(
            Users.userId == user.userId
            ).values(
                Views = user.Views + 1
                )
        exec(query)
    if Type == 'Lyrics':
        lyric = getLyrics().filter_by(lyricsId = objectId).all()[0]
        query = update(Lyrics).where(
            Lyrics.lyricsId == objectId
            ).values(
                totalReads = lyric.totalReads + 1
                )
        exec(query)
        user = getUsers().filter_by(userId = session['user']['userId']).all()[0]
        query = update(Users).where(
            Users.userId == user.userId
            ).values(
                Views = user.Views + 1
                )
        exec(query)
    if Type == 'Album':
        album = getAlbums().filter_by(albumId = objectId).all()[0]
        query = update(Albums).where(
            Albums.albumId == objectId
            ).values(
                totalListens = album.totalListens + 1
                )
        exec(query)
        user = getUsers().filter_by(userId = session['user']['userId']).all()[0]
        query = update(Users).where(
            Users.userId == user.userId
            ).values(
                Views = user.Views + 1
                )
        exec(query)
        session['user'] = guestUserObject(session['user']['userName'])

def addPlaylist(playlistName , songs):
    try:
        playlistId = max([i.playlistId for i in getPlaylists().all()]) + 1
    except:
        playlistId = 1
    query = insert(Playlists).values(
        playlistId = playlistId , playlistName = playlistName ,
        Songs = '|'.join(songs) , userId = session['user']['userId']
    )
    exec(query)

def DeletePlaylist(playlistId):
    query = delete(Playlists).where(Playlists.playlistId == int(playlistId))
    exec(query)

def EditPlaylist(playlistId , songs , name):
    if name == "":
        query = update(Playlists).where(Playlists.playlistId == int(playlistId)).values(Songs = songs)
        exec(query)
    else:
        query = update(Playlists).where(Playlists.playlistId == int(playlistId)).values(Songs = songs , playlistName = name)
        exec(query)

def getSearchResults(key):
    queryKey = '%'+'%'.join(key)+'%'
    songs = getSongs().filter(Songs.songName.like(queryKey)).all()
    lyrics = getLyrics().filter(Lyrics.lyricsName.like(queryKey)).all()
    albums = getAlbums().filter(Albums.albumName.like(queryKey)).all()
    ret = dict_s(songs) , dict_l(lyrics) , dict_a(albums)
    return ret
