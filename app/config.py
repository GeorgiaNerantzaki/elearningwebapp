# -*- encoding: utf-8 -*-

import os, random, string

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
  
   
   #secret_key configuration
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))     

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)
#uses SQLite dbms
    USE_SQLITE  = True 


    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:
            
           
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format()(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            ) 

            USE_SQLITE  = False

        except Exception as e:

            print('> Error:     DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')    
#database configuaretion
    if USE_SQLITE:

        
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    
class ProductionConfig(Config):
    DEBUG = False

    
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True



config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
