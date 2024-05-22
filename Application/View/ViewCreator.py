from Application.Controller.ControllerCreator import *
from flask import current_app as app
from flask import render_template as render
from flask import redirect , request , url_for
from flask import session


#Endpoints
@app.route('/Creator')
def Creator():
    session['user'] = creatorUserObject(session['user']['userName'])
    return render(
        'creatorDashboard.html',
        user = session['user']
        )

@app.route('/Creator/Add/Song' , methods = ["GET" , "POST"])
def AddSong():
    if request.method == "POST":
        songName = request.form['songName']
        Language = request.form['Language']
        if not (validate(songName) and validate(Language)):
            return render(
                        'addsong.html',
                        user = session['user'],
                        message = 'Name and Language fields can contain',
                        message2= 'Alphabets,numbers and spaces only'
                        )
        file = request.files['file']
        try:
            file1 = request.files['file1']
        except:
            file1 = None
        addSong(songName , file ,file1 , Language)
        return render(
            'messageTemplate.html',
            message = 'Successfully Added',
            link = 'home'
        )
    return render(
        'addsong.html',
        user = session['user']
    )

@app.route('/Creator/Add/Lyrics' , methods = ["GET","POST"])
def AddLyrics():
    if request.method == "POST":
        lyricsName = request.form['lyricsName']
        Language = request.form['Language']
        if not (validate(lyricsName) and validate(Language)):
            return render(
                        'addlyrics.html',
                        user = session['user'],
                        message = 'Name and Language fields can contain',
                        message2= 'Alphabets,numbers and spaces only'
                        )
        file = request.files['file']
        addLyrics(lyricsName , file , Language)
        return render(
            'messageTemplate.html',
            message = 'Successfully Added',
            link = 'home'
        )
    return render(
        'addlyrics.html',
        user = session['user']
    )

@app.route('/Creator/Add/Album' , methods = ["GET","POST"])
def AddAlbum():
    if request.method == "POST":
        albumName = request.form['albumName']
        if not validate(albumName):
            return render(
                'addAlbumPlaylist.html',
                user = session['user'],
                message = 'Name can contain Alphabets,',
                message1= 'numbers and spaces only'
            )
        Genre = request.form['Genre']
        if not validate(Genre):
            return render(
                'addAlbumPlaylist.html',
                user = session['user'],
                message = 'Genre can contain Alphabets,',
                message1= 'numbers and spaces only'
            )
        songs = request.form.getlist('songs')
        if len(songs) < 2:
            return render(
                'addAlbumPlaylist.html',
                user = session['user'],
                message = 'Choose 2 or more songs'
            )
        addAlbum(albumName , Genre , songs)
        return render(
            'messageTemplate.html',
            message = "successfully Created",
            link = "home"
        )
    return render(
        'addAlbumPlaylist.html',
        user = session['user']
    )

@app.route('/User/Edit/Album/<albumName>' , methods = ["POST"])
def editAlbum(albumName):
    albumId = request.form['albumId']
    if request.form['from'] == 'home':
        item = None
        for i in session['user']['albums']:
            if i['albumId'] == int(albumId):
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
        EditAlbum(albumId ,'|'.join([str(i) for i in songs])  , '' , '')
        return render(
            'edit.html',
            item = item,
            Type = 'Album',
            user = session['user']
        )
    songs = request.form['dat'].replace(',','|')
    name = request.form['albumName']
    genre = request.form['Genre']
    EditAlbum(albumId , songs , name , genre)
    return render(
        'messageTemplate.html',
        message = 'Successfully Edited',
        link = 'home'
    )

@app.route('/User/Edit/Song/<songName>' , methods = ["POST"])
def editSong(songName):
    songId = request.form['songId']
    if request.form['from'] == 'home':
        item = None
        for i in session['user']['songs']:
            if i['songId'] == int(songId):
                item = i
                break
        return render(
            'edit.html',
            item = item,
            Type = 'Song',
            user = session['user']
        )
    name = request.form['songName']
    lang = request.form['Language']
    EditSong(songId , name , lang)
    return render(
        'messageTemplate.html',
        message = 'Successfully Edited',
        link = 'home'
    )

@app.route('/User/Edit/Lyrics/<lyricsName>' , methods = ["POST"])
def editLyrics(lyricsName):
    lyricsId = request.form['lyricsId']
    if request.form['from'] == 'home':
        item = None
        for i in session['user']['lyrics']:
            if i['lyricsId'] == int(lyricsId):
                item = i
                break
        return render(
            'edit.html',
            item = item,
            Type = 'Lyrics',
            user = session['user']
        )
    name = request.form['lyricsName']
    lang = request.form['Language']
    EditLyrics(lyricsId , name , lang)
    return render(
        'messageTemplate.html',
        message = 'Successfully Edited',
        link = 'home'
    )

@app.route('/Creator/Song')
def CreatorSongs():
    return render(
        'song.html',
        user = session['user'],
    )

@app.route('/Creator/Lyrics')
def CreatorLyrics():
    return render(
        'lyrics.html',
        user = session['user']
    )

@app.route('/Creator/Album')
def CreatorAlbums():
    return render(
        'album.html',
        user = session['user']
    )

@app.route('/Creator/Register')
def register():
    exec(make_creator_request())
    session.pop('temp' , None)
    return render(
        'messageTemplate.html',
        message = "Successfully Made Request",
        link = 'home'
    )
