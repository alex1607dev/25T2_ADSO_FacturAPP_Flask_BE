from flask import Flask
from src.models import Base, engine
from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from src.models.productos import Productos
from src.models.factura import Factura
from src.routes import all_blueprints
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

Base.metadata.create_all(engine)

prefix = '/api/v1'
for bp in all_blueprints:
    print(bp)
    url_prefix=f'{prefix}/{bp.name}'
    print(url_prefix)
    app.register_blueprint(bp, url_prefix=url_prefix)

@app.route('/')
def salud():
    return {'estado': 'ok', 'servicio': 'facturapp-api'}, 200

print("RUTAS REGISTRADAS:", app.url_map)

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)