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


@categorias_bp.route('/<int:id>', methods=['DELETE'])
def delete_categorias(id):
    categorias = Categorias.get_by_id(id)
    if categorias:
        categorias.delete()
        return jsonify({'message': 'Categoria eliminada exitosamente'}), 200
    else:
        return jsonify({'message': 'Categoria no encontrada'}), 404 