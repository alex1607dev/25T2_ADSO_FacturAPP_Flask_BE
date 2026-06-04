from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from src.models import Base, session

class Clientes(Base):  
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(300), nullable=False)
    fecha_nacimiento = Column(Date (10), nullable=False)
    cedula_ciudadania = Column(Integer(11), unique=True, nullable=False)
    telefono = Column(Integer(10), nullable=False)
    direccion = Column(String(300), nullable=False)
    ciudad = Column(String(100), nullable=False)

    def __init__(self, nombre_completo, fecha_nacimiento, cedula_ciudadania, telefono, direccion, ciudad):

        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.cedula_ciudadania = cedula_ciudadania
        self.telefono = telefono
        self.direccion = direccion
        self.ciudad = ciudad
        
    def save(self):
        session.add(self)
        session.commit()

    def get():
        clientes = session.query(Clientes).all()
        return clientes
    
    def get_by_id(id):
        clientes = session.query(Clientes).filter_by(id=id).first()
    
    def delete(self):
        session.delete(self)
        session.commit()