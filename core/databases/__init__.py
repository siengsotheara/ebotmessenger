from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, func
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, encoding='utf-8', echo=False)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
