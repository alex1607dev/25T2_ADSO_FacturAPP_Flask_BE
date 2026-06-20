from flask import Blueprint, request, jsonify
from src.models.factura import Factura

factura_bp = Blueprint('factura', __name__)

@factura_bp.route('/', methods=['GET'])
def get_all_factura():
    factura = Factura.get()
    facturas_list = []
    for factura in factura:
        facturas_list.append({
            'id': factura.id,
            'fecha_': factura.fecha,
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
            'fecha_': factura.fecha,
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
            

    if Factura.fecha.strip()== '':
        return jsonify({'message': 'La fecha de la factura es obligatoria'}), 400
    if Factura.id_cliente <= 0:
        return jsonify({'message': 'El id cliente de la factura debe ser mayor a cero'}), 400
    if Factura.id_usuario <= 0:
        return jsonify({'message': 'El id usuario de la factura debe ser mayor a cero'}), 400
    if Factura.sub_total <= 0:
        return jsonify({'message': 'El subtotal de la factura debe ser mayor a cero'}), 400
    if Factura.iva <= 0:
        return jsonify({'message': 'El iva de la factura debe ser mayor a cero'}), 400
    if Factura.total <= 0:
        return jsonify({'message': 'El total de la factura debe ser mayor a cero'}), 400
    

    factura.save()
    return jsonify({'message':'Factura creada exitosamente'}), 201

