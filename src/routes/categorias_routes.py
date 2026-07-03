from flask import Blueprint, request, jsonify
from src.models.categorias import Categorias


categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
def get_all_categorias():
    categorias = Categorias.get()
    categorias_list = []
    for categoria in categorias:
        categorias_list.append({
            'id': categoria.id_categoria,
            'nombre': categoria.nombre_categoria
        })
    return jsonify(categorias_list), 200


@categorias_bp.route('/<int:id>', methods=['GET'])
def get_categorias(id):
    categorias = Categorias.get_by_id(id)
    if categorias:
        categorias_data = {
            'id': categorias.id_categoria,
            'nombre': categorias.nombre_categoria
        }
        return jsonify(categorias_data), 200
    else:
        return jsonify({'message': 'Categoria no encontrada'}), 404

@categorias_bp.route('/', methods=['POST'])
def create_categorias():
    data = request.get_json()
    categorias = Categorias(
    nombre_categoria = data['nombre_categoria']
    )

    if Categorias.nombre.strip()== '':
        return jsonify({'message': 'El nombre de la categoría es obligatorio'}), 400

    if len(categorias.nombre) > 50:
        return jsonify({'message': 'El nombre de la categoría no puede superar los 50 caracteres'}), 400
    
    categorias.save()
    return jsonify({'message':'Categoria creada exitosamente'}), 201


@categorias_bp.route('/<int:id>', methods=['PUT'])
def update_categoria(id):
    # 1. Verificar si la categoría existe en la base de datos
    categoria = Categorias.get_by_id(id)
    if not categoria:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    # 2. Validar que el campo requerido esté presente en el JSON
    if 'nombre_categoria' not in data:
        return jsonify({'message': 'El campo "nombre_categoria" es obligatorio'}), 400

    nombre_limpio = str(data['nombre_categoria']).strip()

    # 3. Validaciones de reglas de negocio
    if nombre_limpio == '':
        return jsonify({'message': 'El nombre de la categoría no puede estar vacío'}), 400

    if len(nombre_limpio) > 50:
        return jsonify({'message': 'El nombre de la categoría no puede superar los 50 caracteres'}), 400

    # 4. Asignar el nuevo valor y guardar
    categoria.nombre_categoria = nombre_limpio

    try:
        categoria.save()
        return jsonify({'message': 'Categoría actualizada exitosamente'}), 200
    except Exception as e:
        # Por si tienes un índice único en la base de datos y el nombre ya existe
        return jsonify({'message': 'Error al actualizar la categoría', 'error': str(e)}), 500

@categorias_bp.route('/<int:id>', methods=['DELETE'])
def delete_categorias(id):
    categorias = Categorias.get_by_id(id)
    if categorias:
        categorias.delete()
        return jsonify({'message': 'Categoria eliminada exitosamente'}), 200
    else:
        return jsonify({'message': 'Categoria no encontrada'}), 404 