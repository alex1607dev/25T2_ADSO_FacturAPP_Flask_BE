from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from src.models import Base, session

class Factura(Base):  
    __tablename__ = 'factura'

    id = Column(Integer, primary_key=True)
    id_factura = Column(Integer, unique = True, nullable=False)
    fecha = Column(Date, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    sub_total = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    id_detalle_factura = Column(Integer, ForeignKey('detalle_factura.id'), nullable=False)

    def __init__(self, id_factura, fecha, id_cliente, id_usuario, sub_total, iva, total, id_detalle_factura):
        self.id_factura = id_factura
        self.fecha = fecha
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.sub_total = sub_total
        self.iva = iva
        self.total = total
        self.id_detalle_factura = id_detalle_factura
        
    def save(self):
        session.add(self)
        session.commit()

    def get():
        facturas = session.query(Factura).all()
        return facturas
    
    def get_by_id(id):
        facturas = session.query(Factura).filter_by(id=id).first()
    
    def delete(self):
        session.delete(self)
        session.commit()    