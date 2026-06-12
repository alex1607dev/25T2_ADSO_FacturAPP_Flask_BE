from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship 
from src.models import Base, session

class Detalle_Factura(Base):  

    __tablename__ = 'detalle_factura'

    id = Column(Integer, primary_key=True)
    id_factura = Column(Integer, ForeignKey('factura.id'), nullable=False)
    id_producto = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Float, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)

    def __init__(self, id_factura, id_producto, cantidad, precio_unitario, sub_total):
        self.id_factura = id_factura
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.sub_total = sub_total
        
    def save(self):
        session.add(self)
        session.commit()

    def get():
        detalle_facturas = session.query(Detalle_Factura).all()
        return detalle_facturas
    
    def get_by_id(id):
        detalle_facturas = session.query(Detalle_Factura).filter_by(id=id).first()
    
    def delete(self):
        session.delete(self)
        session.commit()    