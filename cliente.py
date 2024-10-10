import requests
from requests.auth import HTTPBasicAuth
def obtener_usuarios():
    response = requests.get('http://localhost:5000/usuarios')
    if response.status_code == 200:
        usuarios = response.json()
        print("Usuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("Error al obtener usuarios") # Muestra un mensaje de error si la solicitud falla

def crear_usuario(nombre):
    nuevo_usuario={"nombre": nombre}
    response=requests.post('http://localhost:5000/usuarios', json=nuevo_usuario)
    if response.status_code==201:
        print("Usuario creado correctamente:", response.json())
    else:
        print("Error al crear un nuevo usuario")
def validar_usuario_agregado(nombre):
    usuarios=obtener_usuarios
    for usuario in usuarios:
        if usuario['nombre'].lower()==nombre.lower():
            print(f"usuario'{nombre}' fue agregado correctamente con ID: {usuario['id']}")
            return True
    print(f"error: el usuario '{nombre}' no fue encontrado en la lista")  

def buscar_usuario_por_id(id):
    response = requests.get(f'http://localhost:5000/usuarios/{id}')
    if response.status_code == 200:
        usuario = response.json()
        print(f"Usuario encontrado: ID = {usuario['id']}, Nombre = {usuario['nombre']}")
    elif response.status_code == 404:
        print(f"Error: Usuario con ID {id} no encontrado")
    else:
        print("Error en la solicitud")  

def eliminar_usuario_por_id(id, username, password):
    response = requests.delete(f'http://localhost:5000/usuarios/{id}', auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        print(response.json()["mensaje"])
    elif response.status_code == 404:
        print(f"Error: Usuario con ID {id} no encontrado")
    elif response.status_code == 401:
        print("Autenticación fallida: credenciales incorrectas")
    else:
        print("Error en la solicitud")

if __name__ == '__main__':
    obtener_usuarios() # Ejecuta la función al iniciar el script
    nombre_usuario = "Lombana"
    usuario_creado = crear_usuario(nombre_usuario)
    if usuario_creado:
        print("Validando si el usuario fue agregado correctamente...")
        validar_usuario_agregado(nombre_usuario)
    obtener_usuarios()
    buscar_usuario_por_id(1)
    buscar_usuario_por_id(3)
    eliminar_usuario_por_id(16, "admin", "admin123")
    obtener_usuarios()
