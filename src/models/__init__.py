from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

engine = create_engine("mysql+pymysql://root:root@localhost:3306/facturapp_25T2_py?charset=utf8mb4")

conection = engine.connect()

sesion = sessionmaker(bind=engine)

session = sesion()

Base = declarative_base()
Base.metadata.bind = engine