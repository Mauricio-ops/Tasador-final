from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from decouple import config
import datetime
import requests
import joblib

modelo = joblib.load('modelo-todo.sav')

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'
app.config['MYSQL_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = config('MYSQL_DB')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configurar la clave secreta para mensajes flash
app.secret_key = 'clave_secreta'

mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('index.html',map_api_key=app.config['MAP_API'])

@app.route('/historial')
def historial():
    comunas = obtener_comuna_tasaciones()
    tasaciones = obtener_direccion_tasaciones()
    return render_template('historial.html', tasaciones=tasaciones, comunas=comunas,map_api_key=app.config['MAP_API'])

@app.route('/calcular_tasacion', methods=['POST'])
def calcular_tasacion():
    try:
        if request.method == 'POST':
            # Obtener los datos del formulario sin transformarlos
            comuna = request.form.get('comuna')
            region = request.form.get('region')
            area_total = float(request.form.get('area_total'))
            area_construida = float(request.form.get('area_construida'))
            condicion = request.form.get('condicion')
            estacionamientos = request.form.get('estacionamientos')
            banos = request.form.get('baños')
            operacion = request.form.get('operacion')
            dormitorio = request.form.get('dormitorio')
            tipo_propiedad = request.form.get('tipo_propiedad')
            # Obtener la longitud y la latitud del formulario
            longitud = request.form.get('longitud')
            latitud = request.form.get('latitud')

            # Guardar los datos sin transformar en la base de datos
            id = guardar_datos_en_base_de_datos(comuna, region, area_total, area_construida, condicion, estacionamientos, banos, operacion, dormitorio, tipo_propiedad, longitud, latitud)

            # Crear un diccionario con los datos para enviar a la API
            datos_para_api = {
                'comuna': comuna,
                'region': region,
                'area_total': area_total,
                'area_construida': area_construida,
                'condicion': condicion,
                'estacionamientos': estacionamientos,
                'banos': banos,
                'operacion': operacion,
                'dormitorio': dormitorio,
                'tipo_propiedad': tipo_propiedad,
                'longitud': longitud,
                'latitud': latitud
            }
            
            # Realizar la solicitud POST a la API
            api_url = 'http://127.0.0.1:5000/api/tasacion'  # Reemplaza con la URL correcta de tu API
            response = requests.post(api_url, json=datos_para_api)
            
            # Obtener la respuesta de la API en formato JSON
            api_response = response.json()
            
            # Obtener el valor predicho de la API
            valor_predicho_api = api_response.get('valor_predicho', None)
            
            # Actualizar la base de datos con el valor predicho
            if valor_predicho_api is not None:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE datos_propiedad SET valor_predicho = %s WHERE id = %s", (valor_predicho_api, id))
                mysql.connection.commit()
                cur.close()

            # Formatear el mensaje de respuesta
            mensaje_respuesta = f'<p style="font-family: \'Nunito\', sans-serif; text-align: center; color: #333; margin: 20px 0; font-size: 24px;"> {api_response["mensaje_respuesta"]} </p>'
            
            # Devolver la respuesta en formato JSON
            return jsonify({'mensaje_respuesta': mensaje_respuesta})
    except Exception as e:
        # Si hay un error en la predicción, mostrar un mensaje de error personalizado en el div "mensaje"
        mensaje_error = f'<p style="font-family: \'Nunito\', sans-serif; text-align: center; color: red; margin: 20px 0; font-size: 24px;">Error en la predicción: {str(e)}</p>'
        return jsonify({'mensaje_respuesta': mensaje_error})

def guardar_datos_en_base_de_datos(comuna, region, area_total, area_construida, condicion, estacionamientos, banos, operacion, dormitorio, tipo_propiedad, longitud, latitud):
    direccion = request.form.get('direccion')
    fecha_ingreso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO datos_propiedad (direccion, comuna, region, area_total, area_construida, condicion, estacionamientos, baños, operacion, dormitorio, tipo_propiedad, fecha_ingreso, longitud, latitud) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (direccion, comuna, region, area_total, area_construida, condicion, estacionamientos, banos, operacion, dormitorio, tipo_propiedad, fecha_ingreso, longitud, latitud))
    mysql.connection.commit()
    id = cur.lastrowid  # Obtener el ID del registro recién insertado
    cur.close()
    return id


def obtener_comuna_tasaciones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT comuna FROM datos_propiedad")
    comunas  = cur.fetchall()
    cur.close()
    return comunas

def obtener_direccion_tasaciones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT direccion FROM datos_propiedad")
    tasaciones  = cur.fetchall()
    cur.close()
    return tasaciones

def obtener_detalles_tasacion(direccion=None, comuna=None):
    # La función ahora acepta dirección y comuna como parámetros opcionales
    cur = mysql.connection.cursor()
    
    if direccion:
        cur.execute("SELECT * FROM datos_propiedad WHERE direccion = %s", (direccion,))
    elif comuna:
        cur.execute("SELECT * FROM datos_propiedad WHERE comuna = %s", (comuna,))
    else:
        return []  # Si no se proporciona ni dirección ni comuna, devolvemos una lista vacía
    
    detalles_tasacion = cur.fetchall()
    cur.close()
    return detalles_tasacion

@app.route('/detalles_tasacion', methods=['POST'])
def detalles_tasacion():
    direccion = request.form.get('direccion')
    comuna = request.form.get('comuna')

    # Obtener más detalles de la tasación según la dirección desde la base de datos
    detalles = obtener_detalles_tasacion(direccion=direccion, comuna=comuna)
    return jsonify({'detalles': detalles})

def obtener_direcciones_tasaciones_por_comuna(comuna):
    cur = mysql.connection.cursor()
    cur.execute("SELECT direccion FROM datos_propiedad WHERE comuna = %s", (comuna,))
    direcciones = cur.fetchall()
    cur.close()
    return direcciones

@app.route('/obtener_direcciones_por_comuna', methods=['POST'])
def obtener_direcciones_por_comuna():
    comuna = request.form.get('comuna')
    direcciones = obtener_direcciones_tasaciones_por_comuna(comuna)
    return jsonify({'direcciones': direcciones})

def obtener_detalles_completos_tasacion(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM datos_propiedad WHERE id = %s", (id,))
        detalles_tasacion = cur.fetchall()
        cur.close()

        if detalles_tasacion:
            # Si se encuentran detalles, devolver la información en formato JSON
            return jsonify({'detalles': detalles_tasacion})
        else:
            # Si no se encuentran detalles, devolver un mensaje indicando eso
            return jsonify({'mensaje': 'No se encontraron detalles para la tasación con ID {}'.format(id)}), 404
    except Exception as e:
        # Manejar cualquier error que pueda ocurrir
        return jsonify({'error': str(e)}), 500

# Agregar la nueva ruta
@app.route('/detalles_completos_tasacion/<int:id>', methods=['GET'])
def detalles_completos_tasacion(id):
    return obtener_detalles_completos_tasacion(id)


if __name__ == '__main__':
    app.config['MAP_API'] = config('MAP_API')
    app.run(host='0.0.0.0', port=3000, debug=True)
