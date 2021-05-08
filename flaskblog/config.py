import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'Hass33naahMaan$1234.5678.90$Ja0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://recon_db_user:Ver$Go0d_99_Us3r@192.168.1.151/recon_dev_db?charset=utf8mb4'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = 'alok1000@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_PASSWORD = 'Gudiya1Darling'
