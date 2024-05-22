from Application.Controller.ControllerGuest import *
from Application.Controller.ControllerCreator import creatorUserObject,EditAlbum
from flask import current_app as app
from flask import render_template as render
from flask import redirect , request , url_for
from flask import session


@app.route('/Login/' , methods = ["POST" , "GET"])
def userLogin():
    if request.method == "POST":
        userName = request.form['userName']
        Password = request.form['Password']
        userType = request.form['userType']
        session['temp'] = userName
        if not (validate(userName) and validate(Password) and ' ' not in userName and ' ' not in Password):
            return render(
                'login.html',
                destination = 'userLogin',
                message = 'username/password can contain',
                message2 = 'alphabets and numbers'
                )
        if validateUser(userName , Password):
            if userType == "Creator":
                Status = validateCreator(userName , Password)
                if Status == 2:
                    session['user'] = (creatorUserObject(userName))
                    return redirect(
                        url_for(
                            'Creator'
                        )
                    )
                elif Status == 1:
                    return render(
                        'messageTemplate.html',
                        message = "You are not approved yet",
                        message2 = "Try after sometime",
                        link = 'home'
                    )
                elif Status == 0:
                    return render(
                        'messageTemplate.html',
                        message = "You are not a Creator",
                        message2 = "click here to register",
                        link = 'register',
                        link2 = 'home'
                    )
                else:
                    return render(
                        'messageTemplate.html',
                        message = "Something went wrong",
                        message2 = "",
                        link = "home"
                    )
            session['user'] = (guestUserObject(userName))
            return redirect(url_for('Guest'))
        else:
            return render(
                'login.html',
                destination = 'userLogin',
                message = 'Invalid Credentials'
                )
    elif request.method == "GET":
        return render(
            'login.html',
            destination = 'userLogin'
            )

@app.route('/User' , methods = ["GET" , "POST"])
def Guest():
    session['user'] = guestUserObject(session['user']['userName'])
    if request.method == "POST":
        key = request.form['query']
        if not validate(key):
            return render(
                'guestDashboard.html',
                user = session['user'],
                search = 0,
                message = 'Search keys can contain alphabets numbers and spaces only'
                )
        return render(
            'guestDashboard.html',
            user = session['user'],
            search = 1,
            searchResults = getSearchResults(key)
            )
    return render(
        'guestDashboard.html',
        user = session['user'],
        search = 0
        )

@app.route('/User/Add/Playlist' , methods = ["GET","POST"])
def CreatePlaylist():
    if request.method == "POST":
        playlistName = request.form['playlistName']
        if not validate(playlistName):
            return render(
                'addAlbumPlaylist.html',
                user = session['user'],
                message = 'Name can contain only Alphabets,',
                message1 = 'Numbers and spaces'
            )
        songs = request.form.getlist('songs')
        if len(songs) < 2:
            return render(
                'addAlbumPlaylist.html',
                user = session['user'],
                message = 'Choose 2 or more songs'
            )
        songs = request.form['Songs'].split(',')
        addPlaylist(playlistName,songs)
        return render(
            'messageTemplate.html',
            message = 'Successfully Added',
            link = 'home'
        )
    return render(
        'addAlbumPlaylist.html',
        user = session['user']
    )

@app.route('/Play/<songName>' , methods = ["POST"])
def Player(songName):
    songId = request.form['songId']
    rated = 0
    if session['user']['userType'] == 'Guest':
        updateViews(int(songId) , 'Song')
        for i in session['user']['rating']:
            if i['objectId'] == int(songId) and i['ratingType'] == 'Song':
                rated = 1
                break
        else:
            rated = 0
    if os.path.isfile(f'./Static/Songs/{songId}.txt'):
        file = open(f'./Static/Songs/{songId}.txt')
        lyrics = file.read()
        file.close()
    else:
        lyrics = 0
    return render(
        'player.html',
        songId = str(songId),
        user = session['user'],
        songName = songName,
        rated = rated,
        lyrics = lyrics
    )

@app.route('/Read/<lyricsName>' , methods = ["POST"])
def Reader(lyricsName):
    lyricsId = request.form['lyricsId']
    rated = 0
    reader = open(f'./Static/Lyrics/{lyricsId}.txt')
    content = reader.read()
    reader.close()
    if session['user']['userType'] == 'Guest':
        updateViews(int(lyricsId) , 'Lyrics')
        for i in session['user']['rating']:
            if i['objectId'] == int(lyricsId) and i['ratingType'] == 'Lyrics':
                rated = 1
                break
        else:
            rated = 0
    return render(
        'reader.html',
        lyricsId = lyricsId,
        user = session['user'],
        lyricsName = lyricsName,
        rated = rated,
        content = content
    )

@app.route('/Play/Playlist/<playlistName>/' , methods = ["POST"])
def PlaylistMaster(playlistName):
    songs = list(map(int,request.form['Songs'].split('|')))
    d2 = []
    di = []
    for i in songs:
        for j in session['user']['songs']:
            if j['songId'] == int(i):
                di.append(j['songName'])
                d2.append(str(i))
                break
    EditPlaylist(request.form['playlistId'] , '|'.join(d2) , '')
    session['alpl'] = d2
    session['names'] = di
    return redirect(
        url_for(
            'PlaylistPlayer' ,
            playlistName = playlistName ,
            index = 1
            ),
            code = 307
    )

@app.route('/Play/Playlist/<playlistName>/index-<int:index>' , methods = ["POST"])
def PlaylistPlayer(playlistName , index):
    def getName(songId):
        for i in session['user']['songs']:
            if i['songId'] == songId:
                return i['songName']
    songId = str(session['alpl'][index-1])
    songName = getName(int(songId))
    rated = 0
    if session['user']['userType'] == 'Guest':
        updateViews(int(songId) , 'Song')
        for i in session['user']['rating']:
            if i['objectId'] == int(songId) and i['ratingType'] == 'Song':
                rated = 1
                break
        else:
            rated = 0
    if os.path.isfile(f'./Static/Songs/{songId}.txt'):
        file = open(f'./Static/Songs/{songId}.txt')
        lyrics = file.read()
        file.close()
    else:
        lyrics = 0
    return render(
        'player.html',
        songId = str(songId),
        user = session['user'],
        AlbumPlaylist = 1,
        playlistName = playlistName ,
        index = index,
        names = session['names'],
        Length = len(session['alpl']),
        songName = songName,
        rated1 = -1,
        lyrics = lyrics
    )

@app.route('/Play/Albums/<albumName>/init' , methods = ["POST"])
def AlbumMaster(albumName):
    songs = list(map(int,request.form['Songs'].split('|')))
    albumId = request.form['albumId']
    d2 = []
    di = []
    for i in songs:
        for j in session['user']['songs']:
            if j['songId'] == int(i):
                di.append(j['songName'])
                d2.append(str(i))
                break
    EditAlbum(albumId , '|'.join(d2) , '' , '')
    session['alpl'] = [int(i) for i in d2] , albumId , di
    if session['user']['userType'] == 'Guest' and session['albumViewed'] == 0:
        updateViews(albumId,'Album')
        session['albumViewed'] = 1
    return redirect(
        url_for(
            'AlbumPlayer' ,
            albumName = albumName ,
            index = 1,
            ),
            code = 307
    )

@app.route('/Play/Albums/<albumName>/index-<int:index>' , methods = ["POST"])
def AlbumPlayer(albumName , index):
    def getName(songId):
        for i in session['user']['songs']:
            if i['songId'] == songId:
                return i['songName']
    songId = str(session['alpl'][0][index-1])
    songName = getName(int(songId))
    rated = 0
    albumId = request.form['albumId']
    if session['user']['userType'] == 'Guest':
        for i in session['user']['rating']:
            if i['objectId'] == int(albumId) and i['ratingType'] == 'Album':
                rated = 1
                break
        else:
            rated = 0
    if os.path.isfile(f'./Static/Songs/{songId}.txt'):
        file = open(f'./Static/Songs/{songId}.txt')
        lyrics = file.read()
        file.close()
    else:
        lyrics = 0
    return render(
        'player.html',
        songId = str(songId),
        user = session['user'],
        AlbumPlaylist = 1,
        albumId = session['alpl'][1],
        albumName = albumName ,
        names = session['alpl'][2],
        index = index,
        Length = len(session['alpl'][0]),
        songName = songName,
        rated1 = rated,
        lyrics = lyrics,
    )

@app.route('/User/Edit/Playlist/<playlistName>' , methods = ["POST"])
def editPlaylist(playlistName):
    playlistId = request.form['playlistId']
    if request.form['from'] == 'home':
        item = None
        for i in session['user']['playlists']:
            if i['playlistId'] == int(playlistId):
                item = i
                break
        songs_ = list(map(int,item['Songs'].split('|')))
        songs = []
        for i in songs_:
            for j in session['user']['songs']:
                if j['songId'] == int(i):
                    songs.append(i)
                    break
        item['Songs'] = songs
        EditPlaylist(playlistId , '|'.join([str(i) for i in songs]) , '')
        return render(
            'edit.html',
            item = item,
            Type = 'Playlist',
            user = session['user']
        )
    songs = request.form['dat'].replace(',','|')
    name = request.form['playlistName']
    EditPlaylist(playlistId , songs , name)
    return render(
        'messageTemplate.html',
        message = 'Successfully Edited',
        link = 'home'
    )

@app.route('/User/Delete/Playlist/<playlistName>' , methods = ["POST"])
def deletePlaylist(playlistName):
    DeletePlaylist(request.form['playlistId'])
    return render(
        'messageTemplate.html',
        message = 'Successfully Deleted',
        link = 'home'
    )

@app.route('/User/Rate/<Type>', methods = ["POST"])
def rate(Type):
    if Type == 'Song':
        songId = request.form['songId']
        songName = request.form['songName']
        value = int(request.form['rating'])
        if value == 0:
            pass
        else:
            updateRating(songId , value , 'Song')
        return redirect(
            url_for(
                'Player' ,
                songName = songName
                ),
                code = 307
        )
    if Type == 'Lyrics':
        lyricsId = request.form['lyricsId']
        lyricsName = request.form['lyricsName']
        value = int(request.form['rating'])
        if value == 0:
            pass
        else:
            updateRating(lyricsId , value , 'Lyrics')
        return redirect(
            url_for(
                'Reader' ,
                lyricsName = lyricsName
                ),
                code = 307
        )
    if Type == 'Album':
        url = request.form['url']
        value = int(request.form['rating'])
        albumId = request.form['albumId']
        if value == 0:
            pass
        else:
            updateRating(albumId, value , 'Album')
        return redirect(
            url,
            code = 307
        )