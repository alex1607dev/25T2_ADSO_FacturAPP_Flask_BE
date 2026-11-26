from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

engine = create_engine("mysql+pymysql://avnadmin:AVNS_1E5bYEeUSB76M6vs2Z5@mysql-1109fd1d-alex16075961-80c9.f.aivencloud.com:25074/defaultdb?charset=utf8mb4")

conection = engine.connect()

sesion = sessionmaker(bind=engine)

session = sesion()

Base = declarative_base()
Base.metadata.bind = engine