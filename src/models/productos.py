from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import Base, session
from sqlalchemy.orm import relationship

class Productos(Base):  
    __tablename__ = 'productos'  

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False)
    Descripcion = Column(String(300), unique=True, nullable=False)
    cantidad_inventario = Column(float, nullable=False)
    precio_unitario = Column(float, nullable=False)
    unidad_medida = Column(String(3), nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'), nullable=False)

    def __init__(self, codigo, Descripcion, cantidad_inventario, precio_unitario, unidad_medida, id_categoria):
        self.codigo = codigo
        self.Descripcion = Descripcion
        self.cantidad_inventario = cantidad_inventario
        self.precio_unitario = precio_unitario
        self.unidad_medida = unidad_medida
        self.id_categoria = id_categoria
        
    def save(self):
        session.add(self)
        session.commit()

    def get():
        productos = session.query(Productos).all()
        return productos
    
    def get_by_id(id):
        productos = session.query(Productos).filter_by(id=id).first()
    
    def delete(self):
        session.delete(self)
        session.commit()
