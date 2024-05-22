from os import path
currentDir = path.abspath(path.dirname(__file__))


class Config():
    DEBUG = False
    SQLITEDB_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITEDB_DB_DIR = path.join(currentDir,'../Database')
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path.join(SQLITEDB_DB_DIR,"applicationDatabase.sqlite3")
    DEBUG = True

class LocalTestConfig(Config):
    SQLITEDB_DB_DIR = path.join(currentDir,'../Database')
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+path.join(SQLITEDB_DB_DIR,"applicationDatabase.sqlite3")
    DEBUG = False