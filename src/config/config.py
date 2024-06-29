import os
import pytz
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SECRET_KEY = "8#y6wf4@t5$s#5r&l#6*kksb(-%omp4gvk(7g73(=pk-h&zjqb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1h

load_dotenv(find_dotenv())

ENVIRON = os.environ.get('ENVIRON')
KAFKA_HOST = os.environ.get('KAFKA_HOST')
TOPIC_KAFKA_PRODUCT = os.environ.get('TOPIC_PRODUCTS')
CONSUMER_KAFKA_PRODUCT = os.environ.get('CONSUMER_GROUP')
TIMEZONE = pytz.timezone(os.environ.get('TIMEZONE'))
TIMEZONE_STR = pytz.timezone(os.environ.get('TIMEZONE'))
USERNAME_API = os.environ.get('USERNAME_API')
PASSWORD_API = os.environ.get('PASSWORD_API')
DATABASE = os.environ.get('DATABASE')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_URL = "postgresql://{}:{}@{}/{}".format(DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE)
ENGINE_VERT = create_engine(DATABASE_URL, pool_size=3, max_overflow=20)
SESSION_VERT = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE_VERT)

Base = declarative_base()


def get_db_vert():
    db = SESSION_VERT()
    try:
        yield db
    except Exception as e:
        print(f"Error during a transaction: {e}")
        db.rollback()
    finally:
        db.close()


ORIGIN_CORS = [
    "*"
]
