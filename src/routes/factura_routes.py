from flask import Blueprint, request, jsonify
from src.models import session
from src.models.factura import Factura
from src.models.detalle_factura import Detalle_Factura
from src.models.productos import Productos
from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from datetime import datetime

factura_bp = Blueprint('factura', __name__)

IVA_TASA = 0.19


@factura_bp.route('/', methods=['GET'])
def get_all_factura():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get ('per_page', default=5, type=int)

    factura, total = Factura.paginate(page=page, per_page=per_page)

    total_page = (total + per_page - 1) // per_page # calcular el número total de páginas

    return jsonify({
        'data': [factura.to_dict() for factura in factura],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_page': total_page,
            'has_next': page < total_page,
            'has_prev': page > 1
        } 
    }), 200
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
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    for campo in ['fecha', 'id_cliente', 'id_usuario', 'detalles']:
        if campo not in data:
            return jsonify({'message': f'El campo "{campo}" es obligatorio'}), 400

    # --- Fecha ---
    try:
        fecha = datetime.strptime(str(data['fecha']).strip(), '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'La fecha debe tener un formato válido AAAA-MM-DD'}), 400

    # --- Cliente y usuario ---
    try:
        id_cliente = int(data['id_cliente'])
        id_usuario = int(data['id_usuario'])
    except (ValueError, TypeError):
        return jsonify({'message': 'Los IDs de cliente y usuario deben ser números enteros válidos'}), 400

    if id_cliente <= 0 or id_usuario <= 0:
        return jsonify({'message': 'Los IDs de cliente y usuario deben ser mayores a cero'}), 400

    if not session.query(Clientes).filter_by(id=id_cliente).first():
        return jsonify({'message': 'El cliente no existe'}), 400
    if not session.query(Usuarios).filter_by(id=id_usuario).first():
        return jsonify({'message': 'El vendedor no existe'}), 400

    # --- Detalles ---
    detalles = data['detalles']
    if not isinstance(detalles, list) or len(detalles) == 0:
        return jsonify({'message': 'La factura debe tener al menos un producto'}), 400

    lineas = []          # (producto, cantidad, precio_sin_iva, sub_total_linea_sin_iva)
    reservado = {}       # cantidad total pedida por producto (por si se repite)
    sub_total = 0.0      # suma SIN IVA
    total = 0.0          # suma CON IVA (precio del producto x cantidad)

    for n, d in enumerate(detalles, start=1):
        try:
            id_producto = int(d['id_producto'])
            cantidad = float(d['cantidad'])
        except (KeyError, ValueError, TypeError):
            return jsonify({'message': f'Línea {n}: producto o cantidad no válidos'}), 400

        if id_producto <= 0 or cantidad <= 0:
            return jsonify({'message': f'Línea {n}: producto y cantidad deben ser mayores a cero'}), 400

        producto = session.query(Productos).filter_by(id=id_producto).first()
        if not producto:
            return jsonify({'message': f'Línea {n}: el producto {id_producto} no existe'}), 400

        reservado[id_producto] = reservado.get(id_producto, 0) + cantidad
        if producto.cantidad_inventario < reservado[id_producto]:
            return jsonify({
                'message': f'Stock insuficiente para "{producto.descripcion}". '
                           f'Disponible: {producto.cantidad_inventario}'
            }), 400

        # El precio del producto YA incluye IVA
        precio_con_iva = float(producto.precio_unitario)
        precio_sin_iva = round(precio_con_iva / (1 + IVA_TASA), 0)

        linea_sub = round(cantidad * precio_sin_iva, 0)        # base de la línea (sin IVA)
        linea_total = round(cantidad * precio_con_iva, 0)      # lo que paga el cliente por la línea

        sub_total += linea_sub
        total += linea_total
        lineas.append((producto, cantidad, precio_sin_iva, linea_sub))

    sub_total = round(sub_total, 0)
    total = round(total, 0)
    iva = round(total - sub_total, 0)    # garantiza sub_total + iva == total

    # --- Guardado en UNA transacción: o se guarda todo o no se guarda nada ---
    try:
        factura = Factura(
            fecha=fecha,
            id_cliente=id_cliente,
            id_usuario=id_usuario,
            sub_total=sub_total,
            iva=iva,
            total=total
        )
        session.add(factura)
        session.flush()               # genera factura.id sin confirmar todavía
        factura_id = factura.id

        for producto, cantidad, precio_sin_iva, linea_sub in lineas:
            session.add(Detalle_Factura(
                id_factura=factura_id,
                id_producto=producto.id,
                cantidad=cantidad,
                precio_unitario=precio_sin_iva,
                sub_total=linea_sub
            ))
            producto.cantidad_inventario = producto.cantidad_inventario - cantidad

        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Error al guardar la factura', 'error': str(e)}), 500

    return jsonify({'message': 'Factura creada exitosamente', 'id': factura_id}), 201


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

    # Validar y formatear Fecha (la columna es DateTime, se guarda un datetime)
    fecha_str = str(data['fecha']).strip()
    try:
        fecha_valida = datetime.strptime(fecha_str, '%Y-%m-%d')
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

    # Validación lógica/matemática (tolerancia por decimales flotantes)
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

