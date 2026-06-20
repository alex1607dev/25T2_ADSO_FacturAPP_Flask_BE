from .productos_routes import productos_bp
from .categorias_routes import categorias_bp
from .clientes_routes import clientes_bp
from .usuarios_routes import usuarios_bp
from .factura_routes import factura_bp
from .detalle_factura_routes import detalle_factura_bp

all_blueprints = [
    productos_bp,
    categorias_bp,
    clientes_bp,
    usuarios_bp,
    factura_bp,
    detalle_factura_bp
]

