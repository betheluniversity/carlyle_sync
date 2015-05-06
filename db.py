import sqlalchemy
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

USERNAME = 'INSERT_USERNAME_HERE'
PASSWORD = 'INSERT_PASSWORD_HERE'
PORT = 'INSERT_PORT_HERE'
HOST = 'INSERT_HOST_HERE'
SERVICE_NAME = 'INSERT_SERVICE_NAME_HERE'

def get_connection():
    #This will cause problems in the future if we want to use more than one class to map DB's
    #sqlalchemy.orm.clear_mappers()

    engine = sqlalchemy.create_engine("oracle+cx_oracle://" + USERNAME + ":" + PASSWORD + "@(DESCRIPTION = (LOAD_BALANCE=on)\
         (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = " + HOST + ")(PORT = " + PORT + "))\
         (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = " + SERVICE_NAME + ")))", echo=False)

    metadata = MetaData(engine)
    session = sessionmaker(bind=engine)()

    return engine, metadata, session
