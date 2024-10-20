from flask import Flask, jsonify, request
import requests
import pyodbc
import json

############################################################################################################################################################
# CONFIGURACION AZURE SQL SERVER NO TOCAR
############################################################################################################################################################
SERVER = 'srvferremas.database.windows.net' # Server example
DATABASE = 'ferremas'
USERNAME = 'ferremasadmin'
PASSWORD = 'Integracion.2024'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};Server=tcp:{SERVER},1433;Database={DATABASE};Uid={USERNAME};Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

############################################################################################################################################################
#Inicio App con Flask
app = Flask(__name__)

# API Inicio Home
@app.route('/')
def hello_world():
    return 'CRUD de Producto con integracion a Azure SQL Server'

############################################################################################################################################################

# Get Producto acepta /all /id?= /marca?=
############################################################################################################################################################
@app.route("/producto", methods=['GET'])
def get_producto():
    print("inicie la funcion get_producto")
    #Inicia Conexión a SQL
    connection = pyodbc.connect(connectionString)
    print("realice la concexion pyodbc connect")
    #Inicia Cursor
    cursor = connection.cursor()
    print("realice la carga del cursor")
    # CAPTURA DE PARAMETROS
    # obtiene todos los Productos
    if 'all' in request.args:
        print("entre al all")
        cursor.execute('SELECT [codigo_producto],[marca],[codigo_marca],[nombre],[categoria] FROM dbo.producto')
    # obtiene solo el Producto del id solicitado
    elif 'id' in request.args:
        id = request.args.get('id')
        cursor.execute('SELECT [codigo_producto],[marca],[codigo_marca],[nombre],[categoria] FROM dbo.producto WHERE codigo_producto = ?', id)
    # obtiene todos los Productos de una Marca solicitada
    elif 'marca' in request.args:
        marca = request.args.get('marca')
        cursor.execute('SELECT [codigo_producto],[marca],[codigo_marca],[nombre],[categoria] FROM dbo.producto WHERE marca = ?', marca)
    # Si se invoca cualquier otro metodo de producto lanza error
    else:
        print("entre al error")
        return jsonify({'error': 'Parámetro incorrecto'}), 400

    # Obtiene los Registros
    data = cursor.fetchall()
    # Cierra el Cursor
    cursor.close()
    # Cierra Conexión
    connection.close()

    # Formatea los resultados en JSON
    json_data = []
    for row in data:
        table_row = {
            'Codigo del producto': row[0],
            'Marca': row[1],
            'Codigo Marca': row[2],
            'Nombre del Producto': row[3],
            'Categoria': row[4]
        }
        json_data.append(table_row)

    return jsonify(json_data)
############################################################################################################################################################

# Update Producto recibe json con atributos de la tabla producto
############################################################################################################################################################
@app.route('/producto', methods=['PUT'])
def update_producto():
    try:
        # Se obtiene json con datos para actualizar
        data = request.get_json()
        # Se valida si vienen datos en el json sino envia error
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400

        # Se obtiene el codigo del producto
        id = data.get('codigo_producto')
        # En caso de que no venga el codigo del producto envia error
        if not id:
            return jsonify({'error': 'Se necesita un CODIGO_PRODUCTO para actualizar los datos'}), 400

        # Verificar si el ID existe en la base de datos
        #Inicia Conexión a SQL
        connection = pyodbc.connect(connectionString)
        #Inicia Cursor
        cursor = connection.cursor()
        #Define la consulta para buscar el codigo del producto que se esta intentando actualizar
        cursor.execute('SELECT COUNT(*) FROM dbo.producto WHERE codigo_producto = ?', id)
        #Asigna el recuento a la variable count para saber cuantos productos existen
        count = cursor.fetchone()[0]
        # Cierra el cursor
        cursor.close()
        # Cierra Conexión
        connection.close()

        # Verifica si el ID del producto fue encontrado en la base de datos
        if count == 0:
            return jsonify({'error': 'El CODIGO_PRODUCTO del producto no existe'}), 404


        # Logica que ejecuta la actualización en la base de datos del producto
        #Inicia Conexión a SQL
        connection = pyodbc.connect(connectionString)
        #Inicia Cursor
        cursor = connection.cursor()
        #Define la Consulta para actualizar la tabla producto [codigo_producto],[marca],[codigo_marca],[nombre],[categoria]
        cursor.execute('UPDATE dbo.producto SET [marca]=?, [codigo_marca]=?, [nombre]=?, [categoria]=?  WHERE [codigo_producto]=?', (data['marca'], data['codigo_marca'], data['nombre'], data['categoria'], id))
        #Realiza el commit de la actualización para confirmar los cambios
        connection.commit()
        # Cierra el cursor
        cursor.close()
        # Cierra Conexión
        connection.close()

        # Responde correctamente que se ingreso el producto
        return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Se produjo un error al actualizar los datos: {}'.format(str(e))}), 500
############################################################################################################################################################

# Delete Producto recibe json con atributos de la tabla producto
############################################################################################################################################################
@app.route('/producto', methods=['DELETE'])
def delete_producto():
    try:
        id = request.args.get('id')
        if not id:
            return jsonify({'error': 'Se necesita un CODIGO_PRODUCTO para eliminar los datos'}), 400

        # Verificar si el ID existe en la base de datos
        #Inicia Conexión a SQL
        connection = pyodbc.connect(connectionString)
        #Inicia Cursor
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM dbo.producto WHERE codigo_producto = ?', id)
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.close()
            return jsonify({'error': 'El CODIGO_PRODUCTO del producto no existe'}), 404

        # Ejecutar el borrado en la base de datos
        cursor.execute('DELETE FROM dbo.producto WHERE codigo_producto = ?', id)
        connection.commit()
        # Cierra el cursor
        cursor.close()
        # Cierra Conexión
        connection.close()

        return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Se produjo un error al eliminar los datos: {}'.format(str(e))}), 500
############################################################################################################################################################

############################################################################################################################################################

# Add Producto recibe json con datos del producto que se desea agregar
############################################################################################################################################################
@app.route("/producto", methods=['POST'])
def add_producto():

    try:
        # Se obtiene json con datos para actualizar
        data = request.get_json()
        # Se valida si vienen datos en el json sino envia error
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para insertar'}), 400

        # Se obtiene el codigo del producto
        id = data.get('codigo_producto')
        # En caso de que no venga el codigo del producto envia error
        if not id:
            return jsonify({'error': 'Se necesita un CODIGO_PRODUCTO para actualizar los datos'}), 400

        # Verificar si el ID existe en la base de datos
        #Inicia Conexión a SQL
        connection = pyodbc.connect(connectionString)
        #Inicia Cursor
        cursor = connection.cursor()
        #Define la consulta para buscar el codigo del producto que se esta intentando actualizar
        cursor.execute('SELECT COUNT(*) FROM dbo.producto WHERE codigo_producto = ?', id)
        #Asigna el recuento a la variable count para saber cuantos productos existen
        count = cursor.fetchone()[0]
        # Cierra el cursor
        cursor.close()
        # Cierra Conexión
        connection.close()

        # Verifica si el ID del producto fue encontrado en la base de datos
        if count != 0:
            return jsonify({'error': 'El CODIGO_PRODUCTO del producto ya existe'}), 404

        # Logica que ejecuta la actualización en la base de datos del producto
        #Inicia Conexión a SQL
        connection = pyodbc.connect(connectionString)
        #Inicia Cursor
        cursor = connection.cursor()

        marca = data.get('marca')
        codigo = data.get('codigo_marca')
        nombre = data.get('nombre')
        categoria = data.get('categoria')
        #Define la Consulta para actualizar la tabla producto [codigo_producto],[marca],[codigo_marca],[nombre],[categoria]
        cursor.execute('INSERT INTO dbo.producto (codigo_producto, marca, codigo_marca, nombre, categoria) VALUES (?, ?, ?, ?, ?)', (id, marca, codigo, nombre, categoria))
        #Realiza el commit de la actualización para confirmar los cambios
        connection.commit()
        # Cierra el cursor
        cursor.close()
        # Cierra Conexión
        connection.close()

        # Responde correctamente que se ingreso el producto
        return jsonify({'mensaje': 'Producto insertado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Se produjo un error al insertar los datos: {}'.format(str(e))}), 500
############################################################################################################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)