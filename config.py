import os

from dotenv import load_dotenv

from webapp.util.functions import create_and_connect

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or '111111'
    main_db_url = f'sqlite:///{os.path.join(basedir, "database.db")}'
    pizza_db_url = f'sqlite:///{os.path.join(basedir, "pizza.db")}'

    create_and_connect(main_db_url)
    create_and_connect(pizza_db_url)

    SQLALCHEMY_DATABASE_URI = main_db_url
    SQLALCHEMY_BINDS = {
        'pizza': pizza_db_url
    }
    SQLALCHEMY = False
