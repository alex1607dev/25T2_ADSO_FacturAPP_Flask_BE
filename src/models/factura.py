from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Base, session
from src.models.detalle_factura import Detalle_Factura


class Factura(Base):  
    __tablename__ = 'factura'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    sub_total = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    def __init__(self, fecha, id_cliente, id_usuario, sub_total, iva, total,):
        self.fecha = fecha
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.sub_total = sub_total
        self.iva = iva
        self.total = total
        
    def save(self):
        session.add(self)
        session.commit()

    def get():
        facturas = session.query(Factura).all()
        return facturas
    
    def get_by_id(id):
        facturas = session.query(Factura).filter_by(id=id).first()
        return facturas
    
    def delete(self):
        session.delete(self)
        session.commit()    