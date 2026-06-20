from flask import Blueprint, request, jsonify
from src.models.clientes import Clientes

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
def get_all_clientes():
    clientes = Clientes.get()
    clientes_list = []
    for cliente in clientes:
        clientes_list.append({
            'id': cliente.id,
            'nombre_completo': cliente.nombre_completo,
            'fecha_nacimiento': cliente.fecha_nacimiento,
            'cedula_ciudadania': cliente.cedula_ciudadania,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'ciudad': cliente.ciudad
        })
    return jsonify(clientes_list), 200

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_clientes(id):
    clientes = Clientes.get_by_id(id)
    if clientes:
        clientes_data = {
            'id': clientes.id,
            'nombre_completo': clientes.nombre_completo,
            'fecha_nacimiento': clientes.fecha_nacimiento,
            'cedula_ciudadania': clientes.cedula_ciudadania,
            'telefono': clientes.telefono,
            'direccion': clientes.direccion,
            'ciudad': clientes.ciudad
        }
        return jsonify(clientes_data), 200
    else:
        return jsonify({'message': 'Cliente no encontrado'}), 404

@clientes_bp.route('/', methods=['POST'])
def create_clientes():
    data = request.get_json()
    clientes = Clientes(
        nombre_completo = data['nombre_completo'],
        fecha_nacimiento = data['fecha_nacimiento'],
        cedula_ciudadania = data['cedula_ciudadania'],
        telefono = data['telefono'],
        direccion = data['direccion'],
        ciudad = data['ciudad']
    )

    if Clientes.nombre_completo.strip()== '':
        return jsonify({'message': 'El nombre completo del cliente es obligatorio'}), 400    
    if Clientes.cedula_ciudadania <= 0:
        return jsonify({'message': 'El cedula ciudadania del cliente debe ser mayor a cero'}), 400
    if Clientes.telefono <= 0:
        return jsonify({'message': 'El telefono del cliente debe ser mayor a cero'}), 400
    if Clientes.direccion == '':
        return jsonify({'message': 'La direccion del cliente es obligatoria'}), 400
    if Clientes.ciudad == '':
        return jsonify({'message': 'La ciudad del cliente es obligatoria'}), 400
    

    clientes.save()
    return jsonify({'message':'Cliente creado exitosamente'}), 201

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_clientes(id):
    clientes = Clientes.get_by_id(id)
    if clientes:
        clientes.delete()
        return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Cliente no encontrado'}), 404   