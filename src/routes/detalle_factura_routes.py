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