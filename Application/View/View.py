from Application.Controller.Controller import *
from Application.Controller.ControllerCreator import creatorUserObject
from Application.Controller.ControllerGuest import guestUserObject
from Application.Controller.ControllerAdmin import adminUserObject
from flask import current_app as app
from flask import render_template as render
from flask import redirect , request , url_for
from flask import session
import werkzeug

@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def _405_(e):
    return render(
        'messageTemplate.html',
        message = 'You cannot access',
        message2 = 'this page like this',
        link = 'home'
    )

#Endpoints
@app.route('/')
def root(): 
    if isLogged():
        return redirect(url_for('home'))
    return render('home.html')

@app.route('/Signup' , methods = ["POST" , "GET"])
def Signup():
    if request.method == "POST":
        userName = request.form['userName']
        Password = request.form['Password']
        if not (validate(userName) and validate(Password) and ' ' not in userName and ' ' not in Password):
            return render(
                'login.html',
                destination = 'Signup',
                message = 'username/password can contain',
                message2 = 'alphabets and numbers only'
                )
        if isAvailable(userName):
            addUser(userName,Password)
            return render(
                'messageTemplate.html',
                message = "Account Created Successfully",
                link = 'home'
            )
        return render(
            'login.html',
            destination = 'Signup',
            message = "username not avalilable"
            )    
    elif request.method == "GET":
        return render(
            'login.html',
            destination = 'Signup'
            )


#Virtual endpoints - intermediate,unstable endpoint and redirects to someother endpoint
@app.route('/reload')
def reload():
    if 'user' not in session:
        pass
    elif session['user']['userType'] == 'Admin':
        session['user'] = adminUserObject(session['user']['userName'])
    elif session['user']['userType'] == 'Creator':
        session['user'] = creatorUserObject(session['user']['userName'])
    elif session['user']['userType'] == 'Guest':
        session['user'] = guestUserObject(session['user']['userName'])

    return redirect(
                    url_for(
                        'home'
                        )
                    )

@app.route('/Logout')
def logout():
    session.pop('user',None)
    return redirect(
        url_for(
            'root'
            )
        )

@app.route('/home/')
def home():
    if not isLogged():
        return redirect(
            url_for(
                'root'
                )
            )
    return redirect(
        url_for(
            session['user']['userType']
            )
        )

