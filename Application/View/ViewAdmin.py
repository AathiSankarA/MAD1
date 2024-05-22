from Application.Controller.ControllerAdmin import *
from Application.Controller.ControllerCreator import creatorUserObject
from flask import current_app as app
from flask import render_template as render
from flask import redirect , request , url_for
from flask import session


#Endpoints
@app.route('/Login/Admin' , methods = ["POST" , "GET"])
def adminLogin():
    if request.method == "POST":
        userName = request.form['userName']
        Password = request.form['Password']
        if not (validate(userName) and validate(Password) and ' ' not in userName and ' ' not in Password):
            return render(
                'login.html',
                destination = 'adminLogin',
                message = 'username/password can',
                message2 = 'only contain alphabets'
                )
        if validateAdmin(userName , Password):
            session['user'] = adminUserObject(userName)
            return redirect(
                url_for(
                    'Admin'
                )
            )
        else:
            return render(
                'login.html',
                destination = 'adminLogin',
                message = 'Invalid Credentials'
                )
    elif request.method == "GET":
        return render(
            'login.html',
            destination = 'adminLogin'
            )

@app.route('/Admin')
def Admin():
    session['user'] = adminUserObject(session['user']['userName'])
    return render(
        'adminDashboard.html',
        user = session['user']
        )

@app.route('/Admin/Users')
def User():
    return render(
        'user.html',
        user = session['user']
    )

@app.route('/Admin/Creators')
def Creators():
    return render(
        'creator.html',
        user = session['user']
    )

@app.route('/Admin/Songs')
def Songs():
    return render(
        'song.html',
        user = session['user']
    )

@app.route('/Admin/Lyrics')
def Lyrics():
    return render(
        'lyrics.html',
        user = session['user']
    )

@app.route('/Admin/Albums')
def Albums():
    return render(
        'album.html',
        user = session['user']
    )

@app.route('/Admin/Add/' , methods = ["GET","POST"])
def AddAdminUser():
    if request.method == "POST":
        userName = request.form['userName']
        Password = request.form['Password']
        if (validate(userName) and validate(Password) and ' ' not in userName and ' ' not in Password):
            addAdmin(userName,Password)
            return render(
                'messageTemplate.html',
                message = 'Successfully Created',
                message2 = 'New Admin User',
                link = 'home'
            )
        return render(
            'addadmin.html',
            user = session['user'],
            message = 'username/password can contain',
            message2 = 'alphabets and numbers'
        )
    return render(
            'addadmin.html',
            user = session['user'],
        )

#APIs
@app.route('/Admin/Reomve/User/<userName>' , methods = ["POST"])
def removeUser(userName):
    remUser(userName)
    return redirect(
        url_for(
            'User'
        )
    )

@app.route('/Admin/Approve/Creator/<userName>' , methods = ["POST"])
def approveCreator(userName):
    appCreator(userName)
    return redirect(
        url_for(
            'Creators'
        )
    )

@app.route('/Admin/Remove/Creator/<userName>' , methods = ["POST"])
def removeCreator(userName):
    remCreator(userName)
    return redirect(
        url_for(
            'Creators'
        )
    )

@app.route('/Admin/Add/Admin/<userName>/<Password>')
def AddAdmin(userName , Password):
    addAdmin(userName,Password)
    return redirect(
        url_for('Admin')
    )

#common to both admins and creators
@app.route('/Admin/Remove/Song/<songName>' , methods = ["POST"])
def removeSong(songName):
    songId = request.form['songId']
    remSong(songId)
    if session['user']['userType'] == 'Admin':
        session['user'] = adminUserObject(session['user']['userName'])
        return redirect(
            url_for(
                'Songs'
            )
        )
    elif session['user']['userType'] == 'Creator':
        session['user'] = creatorUserObject(session['user']['userName'])
        return redirect(
            url_for(
                'Songs'
            )
        )

@app.route('/Admin/Remove/Lyrics/<lyricsName>' , methods = ["POST"])
def removeLyrics(lyricsName):
    lyricsId = request.form['lyricsId']
    remLyrics(lyricsId)
    if session['user']['userType'] == 'Admin':
        session['user'] = adminUserObject(session['user']['userName'])
        return redirect(
            url_for(
                'Lyrics'
            )
        )
    elif session['user']['userType'] == 'Creator':
        session['user'] = creatorUserObject(session['user']['userName'])
        return redirect(
            url_for(
                'CreatorLyrics'
            )
        )

@app.route('/Admin/Remove/Album/<albumName>' , methods = ["POST"])
def removeAlbum(albumName):
    albumId = request.form['albumId']
    remAlbum(albumId)
    if session['user']['userType'] == 'Admin':
        session['user'] = adminUserObject(session['user']['userName'])
        return redirect(
            url_for(
                'Albums'
            )
        )
    elif session['user']['userType'] == 'Creator':
        session['user'] = creatorUserObject(session['user']['userName'])
        return redirect(
            url_for(
                'Albums'
            )
        )
