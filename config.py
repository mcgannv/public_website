import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, os.getenv("DATABASE"))}'
    SQLALCHEMY = False
