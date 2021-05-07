import sqlalchemy
from datetime import datetime


from sqlalchemy import create_engine
engine = create_engine('postgresql://reconuser1:reconuser1@localhost:5432/recon', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    companyid = Column(String(20))
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.companyid}', '{self.image_file}')"


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

print(User.__table__)