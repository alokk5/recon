import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'Hass33naahMaan$1234.5678.90$Ja0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://reconuser1:reconuser1@localhost:5432/recon'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = 'alok1000@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_PASSWORD = 'Gudiya1Darling'
