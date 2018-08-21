import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.environ['SQL_USERNAME']
password = os.environ['SQL_PWORD']
host = os.environ['SQL_HOST']
db = os.environ['SQL_DB']

engine = create_engine('mysql+pymysql://'+ username + ':' + password + '@' + host + '/' + db)
Session = sessionmaker(bind=engine)

Base = declarative_base()
