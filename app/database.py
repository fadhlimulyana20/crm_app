from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# import numpy
from psycopg2.extensions import register_adapter, AsIs
from urllib.parse import quote_plus


DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = quote_plus(os.environ.get('DATABASE_PASSWORD', 'password'))
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5433')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'irt')
DATABASE_DRIVER = os.environ.get('DATABASE_DRIVER', 'postgres')

if DATABASE_DRIVER == 'postgres':
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
elif DATABASE_DRIVER == 'mysql':
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
elif DATABASE_DRIVER == 'mssql':
    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server"
elif DATABASE_DRIVER == 'sqlite':
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_NAME}.db"   

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enable this when using numpy data types with PostgreSQL
# def addapt_numpy_float64(numpy_float64):
#     return AsIs(numpy_float64)

# def addapt_numpy_int64(numpy_int64):
#     return AsIs(numpy_int64)

# register_adapter(numpy.float64, addapt_numpy_float64)
# register_adapter(numpy.int64, addapt_numpy_int64)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()