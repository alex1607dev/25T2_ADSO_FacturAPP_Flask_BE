from flask import Blueprint, request, jsonify
from src.models.factura import Factura
from datetime import datetime

factura_bp = Blueprint('factura', __name__)

@factura_bp.route('/', methods=['GET'])
def get_all_factura():
    factura = Factura.get()
    facturas_list = []
    for factura in factura:
        facturas_list.append({
            'id': factura.id,
            'fecha': factura.fecha,
            'id_cliente': factura.id_cliente,
            'id_usuario': factura.id_usuario,
            'sub_total': factura.sub_total,
            'iva': factura.iva,
            'total': factura.total
        })

    return jsonify(facturas_list), 200

@factura_bp.route('/<int:id>', methods=['GET'])
def get_factura(id):
    factura = Factura.get_by_id(id)
    if factura:
        factura_data = {
            'id': factura.id,
            'fecha': factura.fecha,
            'id_cliente': factura.id_cliente,
            'id_usuario': factura.id_usuario,
            'sub_total': factura.sub_total,
            'iva': factura.iva,
            'total': factura.total
        }
        return jsonify(factura_data), 200
    else:
        return jsonify({'message': 'Factura no encontrada'}), 404

@factura_bp.route('/', methods=['POST'])
def create_factura():
    data = request.get_json()
    factura = Factura(
        fecha = data['fecha'],
        id_cliente = data['id_cliente'],
        id_usuario = data['id_usuario'],
        sub_total = data['sub_total'],
        iva = data['iva'],
        total = data['total']
    )

    try:
        factura.iva = float(factura.iva)
        if factura.iva < 0:
            return jsonify({'message': 'El iva de la factura no puede ser negativo'}), 400
    except (ValueError, TypeError):
            return jsonify({'message': 'El iva de la factura debe ser un numero valido'}), 400
    
    try:
        factura.total = float(factura.total)
        if factura.total < 0:
            return jsonify({'message': 'El total de la factura no puede ser negativo'}), 400
    except (ValueError, TypeError):
            return jsonify({'message': 'El total de la factura debe ser un numero valido'}), 400
            

    if factura.fecha.strip()== '':
        return jsonify({'message': 'La fecha de la factura es obligatoria'}), 400
    if factura.id_cliente <= 0:
        return jsonify({'message': 'El id cliente de la factura debe ser mayor a cero'}), 400
    if factura.id_usuario <= 0:
        return jsonify({'message': 'El id usuario de la factura debe ser mayor a cero'}), 400
    if factura.sub_total < 0:
        return jsonify({'message': 'El subtotal de la factura no puede ser negativo'}), 400
    if factura.iva < 0:
        return jsonify({'message': 'El iva de la factura no puede ser negativo'}), 400
    if factura.total <= 0:
        return jsonify({'message': 'El total de la factura debe ser mayor a cero'}), 400
    

    factura.save()
    return jsonify({'message':'Factura creada exitosamente'}), 201


@factura_bp.route('/<int:id>', methods=['PUT'])
def update_factura(id):
    # 1. Verificar si la factura existe
    factura_existente = Factura.get_by_id(id)
    if not factura_existente:
        return jsonify({'message': 'Factura no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    # 2. Validar presencia de todos los campos requeridos en el JSON
    campos_requeridos = ['fecha', 'id_cliente', 'id_usuario', 'sub_total', 'iva', 'total']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'message': f'El campo "{campo}" es obligatorio'}), 400

    # 3. Validaciones de tipos de datos y reglas de negocio

    # Validar Relaciones (IDs enteros y positivos)
    try:
        id_cliente = int(data['id_cliente'])
        id_usuario = int(data['id_usuario'])
        if id_cliente <= 0 or id_usuario <= 0:
            return jsonify({'message': 'Los IDs de cliente y usuario deben ser mayores a cero'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'Los IDs de cliente y usuario deben ser números enteros válidos'}), 400

    # Validar y formatear Fecha (YYYY-MM-DD o YYYY-MM-DD HH:MM:SS según guardes en tu BD)
    fecha_str = str(data['fecha']).strip()
    try:
        # Intentamos primero con formato de solo fecha, cámbialo a '%Y-%m-%d %H:%M:%S' si guardas la hora
        fecha_valida = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'La fecha debe tener un formato válido AAAA-MM-DD'}), 400

    # Validar Valores Financieros (Floats no negativos)
    try:
        sub_total = float(data['sub_total'])
        iva = float(data['iva'])
        total = float(data['total'])
        
        if sub_total < 0:
            return jsonify({'message': 'El subtotal de la factura no puede ser negativo'}), 400
        if iva < 0:
            return jsonify({'message': 'El IVA de la factura no puede ser negativo'}), 400
        if total <= 0:
            return jsonify({'message': 'El total de la factura debe ser mayor a cero'}), 400
            
    except (ValueError, TypeError):
        return jsonify({'message': 'Los valores de subtotal, IVA y total deben ser números válidos'}), 400

    # Validación lógica/matemática (Opcional pero muy recomendada)
    # Tolerancia por posibles decimales flotantes (0.01)
    if abs((sub_total + iva) - total) > 0.01:
        return jsonify({'message': 'Inconsistencia en los montos: el subtotal más el IVA no coincide con el total'}), 400

    # 4. Asignar los nuevos valores si todo es correcto
    factura_existente.fecha = fecha_valida
    factura_existente.id_cliente = id_cliente
    factura_existente.id_usuario = id_usuario
    factura_existente.sub_total = sub_total
    factura_existente.iva = iva
    factura_existente.total = total

    try:
        factura_existente.save()
        return jsonify({'message': 'Factura actualizada exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al actualizar la factura en la base de datos', 'error': str(e)}), 500

@factura_bp.route('/<int:id>', methods=['DELETE'])
def delete_factura(id):
    factura = Factura.get_by_id(id)
    if factura:
        factura.delete()
        return jsonify({'message': 'Factura eliminada exitosamente'}), 200
    else:
        return jsonify({'message': 'Factura no encontrada'}), 404

