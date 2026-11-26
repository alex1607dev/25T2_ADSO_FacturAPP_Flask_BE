from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, func
from src.models import Base, session

class Usuarios(Base):  
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(300), nullable=False)
    usuario = Column(String(20), nullable=False)
    cedula_ciudadania = Column(Integer, unique=True, nullable=False)
    contraseña = Column(String(20), nullable=False)
    codigo_empleado = Column(String(11), nullable=False)
    rol = Column(String(20), nullable=False)

    def __init__(self, nombre_completo, usuario, cedula_ciudadania, contraseña, codigo_empleado, rol):

        self.nombre_completo = nombre_completo
        self.usuario = usuario
        self.cedula_ciudadania = cedula_ciudadania
        self.contraseña = contraseña
        self.codigo_empleado = codigo_empleado
        self.rol = rol

    def save(self):
        session.add(self)
        session.commit()

    def get():
        usuarios = session.query(Usuarios).all()
        return usuarios
    
    def get_by_id(id):
        usuarios = session.query(Usuarios).filter_by(id=id).first()
        return usuarios
    
    def delete(self):
        session.delete(self)
        session.commit()    

    def to_dict(self):
        return{column.name: getattr(self, column.name) for column in self.__table__.columns}

    def paginate (page=1, per_page=5):
        total = (session.query(func.count(Usuarios.id)).scalar())
        usuarios = session.query(Usuarios).offset((page - 1)* per_page).limit(per_page).all()
        return usuarios, total