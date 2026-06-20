from sqlalchemy import Column, Integer, String
from src.models import Base, session

class Categorias(Base):  
    __tablename__ = 'categorias'        

    id_categoria = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(50), nullable=False)

    def __init__(self, nombre_categoria):
        self.nombre_categoria = nombre_categoria

    def save(self):
        session.add(self)
        session.commit()

    def get():
        categorias = session.query(Categorias).all()
        return categorias
    
    def get_by_id(id):
        categorias = session.query(Categorias).filter_by(id_categoria=id).first()
        return categorias
    
    def delete(self):
        session.delete(self)
        session.commit()