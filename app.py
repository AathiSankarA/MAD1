from flask import Flask
from Application.Model import db
from Application.Config import LocalDevelopmentConfig , LocalTestConfig
import sys


def CreateApp(name):
    app = Flask (name , template_folder = "Templates" , static_folder = "Static" )
    app.secret_key = 'HeLl0'
    app.config.from_object(LocalTestConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = CreateApp("Music")

from Application.View.View import *
from Application.View.ViewGuest import *
from Application.View.ViewAdmin import *
from Application.View.ViewCreator import *

if __name__ == "__main__":
    app.run(host="0.0.0.0")