from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def get_all_usuarios():
    usuarios = Usuarios.get()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario.id,
            'nombre_completo': usuario.nombre,
            'usuario': usuario.usuario,
            'cedula_ciudadania': usuario.cedula_ciudadania,
            'contraseña': usuario.contraseña,
            'codigo_empleado': usuario.codigo_empleado,
            'rol': usuario.rol
        })
    return jsonify(usuarios_list), 200

@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuarios(id):
    usuarios = Usuarios.get_by_id(id)
    if usuarios:
        usuarios_data = {
            'id': usuarios.id,
            'nombre_completo': usuarios.nombre,
            'usuario': usuarios.usuario,
            'cedula_ciudadania': usuarios.cedula_ciudadania,
            'contraseña': usuarios.contraseña,
            'codigo_empleado': usuarios.codigo_empleado,
            'rol': usuarios.rol
        }
        return jsonify(usuarios_data), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404

@usuarios_bp.route('/', methods=['POST'])
def create_usuarios():
    data = request.get_json()
    usuarios = Usuarios(
        nombre = data['nombre'],
        usuario = data['usuario'],
        cedula_ciudadania = data['cedula_ciudadania'],
        contraseña = data['contraseña'],
        codigo_empleado = data['codigo_empleado'],
        rol = data['rol']
    )

    if Usuarios.nombre.strip()== '':
        return jsonify({'message': 'El nombre del usuario es obligatorio'}), 400
    if Usuarios.usuario.strip()== '':
        return jsonify({'message': 'El usuario del usuario es obligatorio'}), 400
    if Usuarios.cedula_ciudadania <= 0:
        return jsonify({'message': 'El cedula ciudadania del usuario debe ser mayor a cero'}), 400
    if Usuarios.contraseña.strip()== '':
        return jsonify({'message': 'La contraseña del usuario es obligatoria'}), 400
    if Usuarios.codigo_empleado.strip()== '':
        return jsonify({'message': 'El codigo empleado del usuario es obligatorio'}), 400
    if Usuarios.rol.strip()== '':
        return jsonify({'message': 'El rol del usuario es obligatorio'}), 400
    

    usuarios.save()
    return jsonify({'message':'Usuario creado exitosamente'}), 201

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuarios(id):
    usuarios = Usuarios.get_by_id(id)
    if usuarios:
        usuarios.delete()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404   