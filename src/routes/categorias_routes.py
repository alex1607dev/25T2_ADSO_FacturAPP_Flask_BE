from flask import Blueprint, request, jsonify
from src.models.categorias import Categorias


categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
def get_all_categorias():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get ('per_page', default=5, type=int)

    categorias, total = Categorias.paginate(page=page, per_page=per_page)

    total_page = (total + per_page - 1) // per_page # calcular el número total de páginas

    return jsonify({
        'data': [categoria.to_dict() for categoria in categorias],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_page': total_page,
            'has_next': page < total_page,
            'has_prev': page > 1
        } 
    }), 200

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
    # 1. Obtener los datos del JSON una sola vez
    data = request.get_json()
    
    # Validar que el JSON no venga vacío o mal formado
    if not data:
        return jsonify({'message': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    # 2. Validar que el campo exista en el JSON
    if 'nombre_categoria' not in data:
        return jsonify({'message': 'El campo "nombre_categoria" es obligatorio'}), 400

    # 3. Extraer y limpiar el valor real
    nombre_limpio = str(data['nombre_categoria']).strip()

    # 4. Validaciones de reglas de negocio
    if nombre_limpio == '':
        return jsonify({'message': 'El nombre de la categoría no puede estar vacío'}), 400

    if len(nombre_limpio) > 50:
        return jsonify({'message': 'El nombre de la categoría no puede superar los 50 caracteres'}), 400

    # 5. Si todo está bien, crear el objeto y guardarlo
    try:
        # Nota: Si tu base de datos autoincrementa el ID, quita el id_categoria=1 aquí
        # Si necesitas forzar el ID 1, puedes pasarlo así:
        nueva_categoria = Categorias(
            nombre_categoria=nombre_limpio
        )
        nueva_categoria.save()
        return jsonify({'message': 'Categoría creada exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': 'Error al crear la categoría', 'error': str(e)}), 500


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