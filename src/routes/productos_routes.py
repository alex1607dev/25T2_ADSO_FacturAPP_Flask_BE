from flask import Blueprint, request, jsonify
from src.models.productos import Productos


productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def get_all_productos():
    productos = Productos.get()
    productos_list = []
    for producto in productos:
        productos_list.append({
            'id': producto.id,
            'codigo': producto.codigo,
            'descripcion': producto.descripcion,
            'cantidad_inventario': producto.cantidad_inventario,
            'precio_unitario': producto.precio_unitario,
            'unidad_medida': producto.unidad_medida,
            'id_categoria': producto.id_categoria
        })
    return jsonify(productos_list), 200

@productos_bp.route('/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Productos.get_by_id(id)
    print(id)
    print(producto)
    if producto:
        producto_data = {
            'id': producto.id,
            'codigo': producto.codigo,
            'descripcion': producto.descripcion,
            'cantidad_inventario': producto.cantidad_inventario,
            'precio_unitario': producto.precio_unitario,
            'unidad_medida': producto.unidad_medida,
            'id_categoria': producto.id_categoria
        }
        return jsonify(producto_data), 200
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404

@productos_bp.route('/', methods=['POST'])
def create_producto():
    data = request.get_json()
    producto = Productos(
        codigo = data['codigo'],
        descripcion = data['descripcion'],
        cantidad_inventario = data['cantidad_inventario'],
        precio_unitario = data['precio_unitario'],
        unidad_medida = data['unidad_medida'],
        id_categoria = data['id_categoria']
    )

    try:
        float(producto.precio_unitario)
        print("valid number")
    except ValueError:
        return jsonify({'message': 'El precio unitario del producto debe ser un numero valido'}), 400
    if producto.descripcion == '':
        return jsonify({'message': 'La descripcion del producto es obligatoria'}), 400
    if producto.cantidad_inventario <= 0:
        return jsonify({'message': 'La cantidad de inventario no puede ser menor a cero'}), 400
    if producto.precio_unitario <= 0:
        return jsonify({'message': 'El precio unitario del producto debe ser mayor a cero'}), 400
    if producto.unidad_medida == '':
        return jsonify({'message': 'La unidad de medida del producto es obligatoria'}), 400
    if producto.id_categoria == '':
        return jsonify({'message': 'La categoria del producto es obligatoria'}), 400
    

    producto.save()
    return jsonify({'message':'Producto creado exitosamente'}), 201
