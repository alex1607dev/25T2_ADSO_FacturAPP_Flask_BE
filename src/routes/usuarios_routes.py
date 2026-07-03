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
            'nombre_completo': usuario.nombre_completo,
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
            'nombre_completo': usuarios.nombre_completo,
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
        nombre_completo = data['nombre_completo'],
        usuario = data['usuario'],
        cedula_ciudadania = data['cedula_ciudadania'],
        contraseña = data['contraseña'],
        codigo_empleado = data['codigo_empleado'],
        rol = data['rol']
    )

    if usuarios.nombre_completo.strip()== '':
        return jsonify({'message': 'El nombre del usuario es obligatorio'}), 400
    if usuarios.usuario.strip()== '':
        return jsonify({'message': 'El usuario del usuario es obligatorio'}), 400
    if usuarios.cedula_ciudadania <= 0:
        return jsonify({'message': 'El cedula ciudadania del usuario debe ser mayor a cero'}), 400
    if usuarios.contraseña.strip()== '':
        return jsonify({'message': 'La contraseña del usuario es obligatoria'}), 400
    if usuarios.codigo_empleado.strip()== '':
        return jsonify({'message': 'El codigo empleado del usuario es obligatorio'}), 400
    if usuarios.rol.strip()== '':
        return jsonify({'message': 'El rol del usuario es obligatorio'}), 400
    

    usuarios.save()
    return jsonify({'message':'Usuario creado exitosamente'}), 201

@usuarios_bp.route('/<int:id>', methods=['PUT'])
def update_usuario(id):
    # 1. Verificar si el usuario existe
    usuario_existente = Usuarios.get_by_id(id)
    if not usuario_existente:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    # 2. Validar presencia de todos los campos requeridos
    campos_requeridos = ['nombre_completo', 'usuario', 'cedula_ciudadania', 'contraseña', 'codigo_empleado', 'rol']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'message': f'El campo "{campo}" es obligatorio'}), 400

    # 3. Validaciones de tipos de datos y reglas de negocio
    
    # Validar cédula de ciudadanía (Debe ser un número entero válido y positivo)
    try:
        cedula = int(data['cedula_ciudadania'])
        if cedula <= 0:
            return jsonify({'message': 'La cédula de ciudadanía debe ser mayor a cero'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'La cédula de ciudadanía debe ser un número entero válido'}), 400

    # Limpiar espacios en blanco de los strings
    nombre_completo = str(data['nombre_completo']).strip()
    username = str(data['usuario']).strip()
    password = str(data['contraseña']).strip()
    codigo_emp = str(data['codigo_empleado']).strip()
    rol = str(data['rol']).strip()

    # Validar que ningún string obligatorio quede vacío tras el strip
    if nombre_completo == '':
        return jsonify({'message': 'El nombre del usuario es obligatorio'}), 400
    if username == '':
        return jsonify({'message': 'El nombre de usuario (login) es obligatorio'}), 400
    if password == '':
        return jsonify({'message': 'La contraseña del usuario es obligatoria'}), 400
    if codigo_emp == '':
        return jsonify({'message': 'El código de empleado es obligatorio'}), 400
    if rol == '':
        return jsonify({'message': 'El rol del usuario es obligatorio'}), 400

    # Opcional: Validar roles permitidos si manejas un sistema estricto (ej. Administrador, Cajero)
    # roles_permitidos = ['Administrador', 'Cajero', 'Vendedor']
    # if rol not in roles_permitidos:
    #     return jsonify({'message': 'El rol especificado no es válido'}), 400

    # 4. Asignar nuevos valores
    usuario_existente.nombre_completo = nombre_completo
    usuario_existente.usuario = username
    usuario_existente.cedula_ciudadania = cedula
    usuario_existente.contraseña = password  # Nota: Idealmente aquí aplicarías un hash (ej. bcrypt)
    usuario_existente.codigo_empleado = codigo_emp
    usuario_existente.rol = rol

    try:
        usuario_existente.save()
        return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
    except Exception as e:
        # Captura errores de base de datos como nombres de usuario o cédulas duplicadas
        return jsonify({'message': 'Error al actualizar el usuario', 'error': str(e)}), 500

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def delete_usuarios(id):
    usuarios = Usuarios.get_by_id(id)
    if usuarios:
        usuarios.delete()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404   