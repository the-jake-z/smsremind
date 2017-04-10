###########################################
#       config.py
#       Stores configuration information
#   
#       Dynamically loads a config file
#       
#       Note: do not place any private
#       production key/tokens in this file. 
#       Instead, load from environment var
###########################################

import datetime, os


class Config(object):
    CONFIGURATION = "DEFAULT"
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    MONGODB_SETTINGS = {
        'db': 'smsremind',
        'host': 'localhost'
    }
    SECRET_KEY = "some really long secret key that will just get overriden"
    PORT = 8080,
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN") or None
    TWILIO_SID = os.environ.get("TWILIO_SID") or None


class ProductionConfig(Config):
    CONFIGURATION = "PRODUCTION"
    DEBUG = False
    PORT = int(os.environ.get('PORT', 5000))
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_URI', 'localhost')
    }
    SECRET_KEY = os.environ.get('SECRET_TOKEN', 'really should replace this')


class DevelopmentConfig(Config):
    CONFIGURATION = "DEVELOPMENT"
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(0, 5)


class TestingConfig(Config):
    CONFIGURATION = "TESTING"
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'db':'testdb',
        'host':'mongomock://localhost'
    }
    WTF_CSRF_ENABLED = False

