from flask import Blueprint, request, jsonify
from src.models.detalle_factura import Detalle_Factura

detalle_factura_bp = Blueprint('detalle_factura', __name__)

@detalle_factura_bp.route('/', methods=['GET'])
def get_all_detalle_factura():
    detalle_factura = Detalle_Factura.get()
    detalle_factura_list = []
    for detalle_factura in detalle_factura:
        detalle_factura_list.append({
            'id': detalle_factura.id,
            'id_factura': detalle_factura.id_factura,
            'id_producto': detalle_factura.id_producto,
            'cantidad': detalle_factura.cantidad,
            'precio_unitario': detalle_factura.precio_unitario,
            'sub_total': detalle_factura.sub_total,
        })

    return jsonify(detalle_factura_list), 200    

@detalle_factura_bp.route('/<int:id>', methods=['GET'])
def get_detalle_factura(id):
    detalle_factura = Detalle_Factura.get_by_id(id)
    if detalle_factura:
        detalle_factura_data = {
            'id': detalle_factura.id,
            'id_factura': detalle_factura.id_factura,
            'id_producto': detalle_factura.id_producto,
            'cantidad': detalle_factura.cantidad,
            'precio_unitario': detalle_factura.precio_unitario,
            'sub_total': detalle_factura.sub_total,
        }
        return jsonify(detalle_factura_data), 200
    else:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404

@detalle_factura_bp.route('/', methods=['POST'])
def create_detalle_factura():
    data = request.get_json()
    detalle_factura = Detalle_Factura(
        id_factura = data['id_factura'],
        id_producto = data['id_producto'],
        cantidad = data['cantidad'],
        precio_unitario = data['precio_unitario'],
        sub_total = data['sub_total']
    )

    try:
        detalle_factura.cantidad = float(detalle_factura.cantidad)
        if detalle_factura.cantidad < 0:
            return jsonify({'message': 'La cantidad de la factura no puede ser negativa'}), 400
    except (ValueError, TypeError):
            return jsonify({'message': 'La cantidad de la factura debe ser un numero valido'}), 400
    
    try:
        detalle_factura.precio_unitario = float(detalle_factura.precio_unitario)
        if detalle_factura.precio_unitario < 0:
            return jsonify({'message': 'El precio unitario de la factura no puede ser negativo'}), 400
    except (ValueError, TypeError):
            return jsonify({'message': 'El precio unitario de la factura debe ser un numero valido'}), 400
    
    try:
        detalle_factura.sub_total = float(detalle_factura.sub_total)
        if detalle_factura.sub_total < 0:
            return jsonify({'message': 'El subtotal de la factura no puede ser negativo'}), 400
    except (ValueError, TypeError):
            return jsonify({'message': 'El subtotal de la factura debe ser un numero valido'}), 400
    

    detalle_factura.save()
    return jsonify({'message':'Detalle de factura creado exitosamente'}), 201

@detalle_factura_bp.route('/<int:id>', methods=['PUT'])
def update_detalle_factura(id):
    # 1. Verificar si el detalle de factura existe
    detalle_existente = Detalle_Factura.get_by_id(id)
    if not detalle_existente:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    # 2. Validar presencia de todos los campos requeridos en el JSON
    campos_requeridos = ['id_factura', 'id_producto', 'cantidad', 'precio_unitario', 'sub_total']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'message': f'El campo "{campo}" es obligatorio'}), 400

    # 3. Validaciones de tipos de datos y reglas de negocio

    # Validar Relaciones (IDs enteros y positivos)
    try:
        id_factura = int(data['id_factura'])
        id_producto = int(data['id_producto'])
        if id_factura <= 0 or id_producto <= 0:
            return jsonify({'message': 'Los IDs de factura y producto deben ser mayores a cero'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'Los IDs de factura y producto deben ser números enteros válidos'}), 400

    # Validar Valores Numéricos y Financieros (Floats no negativos)
    try:
        cantidad = float(data['cantidad'])
        precio_unitario = float(data['precio_unitario'])
        sub_total = float(data['sub_total'])
        
        if cantidad <= 0:
            return jsonify({'message': 'La cantidad del detalle debe ser mayor a cero'}), 400
        if precio_unitario < 0:
            return jsonify({'message': 'El precio unitario no puede ser negativo'}), 400
        if sub_total < 0:
            return jsonify({'message': 'El subtotal no puede ser negativo'}), 400
            
    except (ValueError, TypeError):
        return jsonify({'message': 'La cantidad, precio unitario y subtotal deben ser números válidos'}), 400

    # Validación lógica/matemática: cantidad * precio_unitario == sub_total
    # Usamos abs() y un margen de tolerancia (0.01) para evitar problemas de redondeo con floats
    if abs((cantidad * precio_unitario) - sub_total) > 0.01:
        return jsonify({'message': 'Inconsistencia en los montos: el subtotal no coincide con el producto de cantidad por precio unitario'}), 400

    # 4. Asignar los nuevos valores si todo está correcto
    detalle_existente.id_factura = id_factura
    detalle_existente.id_producto = id_producto
    detalle_existente.cantidad = cantidad
    detalle_existente.precio_unitario = precio_unitario
    detalle_existente.sub_total = sub_total

    try:
        detalle_existente.save()
        return jsonify({'message': 'Detalle de factura actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el detalle de la factura en la base de datos', 'error': str(e)}), 500

@detalle_factura_bp.route('/<int:id>', methods=['DELETE'])
def delete_detalle_factura(id):
    detalle = Detalle_Factura.get_by_id(id)
    if detalle:
        detalle.delete()
        return jsonify({'message': 'Detalle de factura eliminado exitosamente'}), 200
    else:
        return jsonify({'message': 'Detalle de factura no encontrado'}), 404