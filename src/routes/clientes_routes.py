from flask import Blueprint, request, jsonify
from src.models.clientes import Clientes
from datetime import datetime

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

    if clientes.nombre_completo.strip()== '':
        return jsonify({'message': 'El nombre completo del cliente es obligatorio'}), 400    
    if clientes.cedula_ciudadania <= 0:
        return jsonify({'message': 'El cedula ciudadania del cliente debe ser mayor a cero'}), 400
    if clientes.telefono <= 0:
        return jsonify({'message': 'El telefono del cliente debe ser mayor a cero'}), 400
    if clientes.direccion == '':
        return jsonify({'message': 'La direccion del cliente es obligatoria'}), 400
    if clientes.ciudad == '':
        return jsonify({'message': 'La ciudad del cliente es obligatoria'}), 400
    

    clientes.save()
    return jsonify({'message':'Cliente creado exitosamente'}), 201


@clientes_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    # 1. Verificar si el cliente existe
    cliente_existente = Clientes.get_by_id(id)
    if not cliente_existente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    # 2. Validar presencia de todos los campos requeridos en el JSON
    campos_requeridos = ['nombre_completo', 'fecha_nacimiento', 'cedula_ciudadania', 'telefono', 'direccion', 'ciudad']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'message': f'El campo "{campo}" es obligatorio'}), 400

    # 3. Validaciones de tipos de datos y reglas de negocio

    # Validar Cédula de Ciudadanía (Número entero positivo)
    try:
        cedula = int(data['cedula_ciudadania'])
        if cedula <= 0:
            return jsonify({'message': 'La cédula de ciudadanía del cliente debe ser mayor a cero'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'La cédula de ciudadanía debe ser un número entero válido'}), 400

    # Validar Teléfono (Número entero positivo)
    try:
        telefono = int(data['telefono'])
        if telefono <= 0:
            return jsonify({'message': 'El teléfono del cliente debe ser mayor a cero'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'El teléfono debe ser un número entero válido'}), 400

    # Validar y formatear Fecha de Nacimiento (YYYY-MM-DD)
    fecha_nacimiento_str = str(data['fecha_nacimiento']).strip()
    if fecha_nacimiento_str == '' or fecha_nacimiento_str.lower() == 'none':
        # Puedes decidir si permites que sea opcional (None) o si la obligas
        fecha_nacimiento_valida = None 
    else:
        try:
            # Valida que cumpla el formato ISO estándar (Año-Mes-Día)
            fecha_nacimiento_valida = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'La fecha de nacimiento debe tener el formato válido AAAA-MM-DD (ej: 1990-05-15)'}), 400

    # Limpiar cadenas de texto obligatorias
    nombre_completo = str(data['nombre_completo']).strip()
    direccion = str(data['direccion']).strip()
    ciudad = str(data['ciudad']).strip()

    if nombre_completo == '':
        return jsonify({'message': 'El nombre completo del cliente es obligatorio'}), 400
    if direccion == '':
        return jsonify({'message': 'La dirección del cliente es obligatoria'}), 400
    if ciudad == '':
        return jsonify({'message': 'La ciudad del cliente es obligatoria'}), 400

    # 4. Asignar los nuevos valores validados
    cliente_existente.nombre_completo = nombre_completo
    cliente_existente.fecha_nacimiento = fecha_nacimiento_valida
    cliente_existente.cedula_ciudadania = cedula
    cliente_existente.telefono = telefono
    cliente_existente.direccion = direccion
    cliente_existente.ciudad = ciudad

    try:
        cliente_existente.save()
        return jsonify({'message': 'Cliente actualizado exitosamente'}), 200
    except Exception as e:
        # Controlar errores de integridad (como si la cédula ya pertenece a otro cliente)
        return jsonify({'message': 'Error al actualizar el cliente en la base de datos', 'error': str(e)}), 500

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete_clientes(id):
    clientes = Clientes.get_by_id(id)
    if clientes:
        clientes.delete()
        return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Cliente no encontrado'}), 404   