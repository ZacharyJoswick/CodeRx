import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:CodeRxYourDailyDoseOfCode@db/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask security config
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.environ.get('PASSWORD_SALT') or "a_very_salty_salt"

    SECURITY_EMAIL_SENDER = 'admin@coderx.io'
    MAIL_SERVER = 'mail.privateemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'admin@coderx.io'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'

    # LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']
    # LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # POSTS_PER_PAGE = 25