import os.path
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(find_dotenv())

engine = create_engine(f'{os.environ.get("DBMS")}://{os.environ.get("DB_USER")}:'
                       f'{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:'
                       f'{os.environ.get("DB_PORT")}/'
                       f'{os.environ.get("DB_NAME")}', echo=False)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
