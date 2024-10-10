from flask import Flask, jsonify, request, make_response
from functools import wraps

app = Flask(__name__)

# Base de datos simulada de usuarios
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "María"}
    ]
}

# Datos de usuario para la autenticación básica (credenciales)
USUARIOS_VALIDOS = {
    "admin": "admin123"  # Usuario y contraseña
}

# Función para requerir autenticación básica en rutas
def autenticacion_basica(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        auth = request.authorization
        if not auth or not verificar_credenciales(auth.username, auth.password):
            return make_response("No autorizado", 401, {"WWW-Authenticate": "Basic realm='Login requerido'"})
        return f(*args, **kwargs)
    return funcion_decorada

# Verifica las credenciales del usuario
def verificar_credenciales(username, password):
    return USUARIOS_VALIDOS.get(username) == password

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos["usuarios"])

# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    nuevo_usuario = request.get_json()
    if "nombre" not in nuevo_usuario or not nuevo_usuario["nombre"].strip():
        return jsonify({"error": "El campo 'nombre' es obligatorio y no puede estar vacío"}), 400
    
    # Verificar que el nombre no esté duplicado
    for usuario in base_datos["usuarios"]:
        if usuario["nombre"].lower() == nuevo_usuario["nombre"].lower():
            return jsonify({"error": f"El nombre '{nuevo_usuario['nombre']}' ya está en uso"}), 400

    nuevo_id = len(base_datos["usuarios"]) + 1
    usuario = {"id": nuevo_id, "nombre": nuevo_usuario["nombre"]}
    base_datos["usuarios"].append(usuario)
    return jsonify(usuario), 201

# Ruta para buscar un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario_por_id(id):
    for usuario in base_datos["usuarios"]:
        if usuario["id"] == id:
            return jsonify(usuario)
    return jsonify({"error": f"Usuario con ID {id} no encontrado"}), 404

# Ruta para eliminar un usuario por ID (protegida con autenticación básica)
@app.route('/usuarios/<int:id>', methods=['DELETE'])
@autenticacion_basica
def eliminar_usuario(id):
    for usuario in base_datos["usuarios"]:
        if usuario["id"] == id:
            base_datos["usuarios"].remove(usuario)
            return jsonify({"mensaje": f"Usuario con ID {id} eliminado correctamente"}), 200
    return jsonify({"error": f"Usuario con ID {id} no encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000)
