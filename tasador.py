from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Cargar el modelo entrenado
modelo = joblib.load('prueba-modelo-rf.sav')

# Diccionarios de mapeo para las transformaciones
transformacion_dict = {
    'comuna': {
        'concon': 0,
        'limache': 1,
        'quillota': 2,
        'quilpue': 3,
        'valparaiso': 4,
        'villa alemana': 5,
        'viña del mar': 6
    },
    'region': {
        'valparaiso': 5
    },
    'operacion': {
        'venta': 0,
        'arriendo': 1
    },
    'condicion': {
        'nuevo': 0,
        'usado': 1,
        'remodelada': 2
    },
    'tipo_propiedad': {
        'casa': 0,
        'departamento': 1
    }
}

@app.route('/api/tasacion', methods=['POST'])
def tasacion():
    try:
        # Obtener los datos en formato JSON desde la solicitud
        data = request.get_json()

        # Realizar las transformaciones de datos
        datos_transformados = {
            'comuna': transformar_dato(data['comuna'], transformacion_dict['comuna']),
            'region': transformar_dato(data['region'], transformacion_dict['region']),
            'operacion': transformar_dato(data['operacion'], transformacion_dict['operacion']),
            'condicion': transformar_dato(data['condicion'], transformacion_dict['condicion']),
            'tipo_propiedad': transformar_dato(data['tipo_propiedad'], transformacion_dict['tipo_propiedad']),
            'dormitorio': data['dormitorio'],
            'banos': data['banos'],
            'estacionamientos': data['estacionamientos'],
            'area_total': data['area_total'],
            'area_construida': data['area_construida'],
            'longitud': data['longitud'],
            'latitud': data['latitud']
        }

        # Realizar la predicción usando el modelo cargado
        valor_predicho = predict(modelo, datos_transformados)
        

        # Formatear el mensaje de respuesta
        mensaje_respuesta = f'La tasación estimada es de: {valor_predicho} UF'
        
        # Devolver la respuesta en formato JSON
        return jsonify({'mensaje_respuesta': mensaje_respuesta, 'valor_predicho': valor_predicho})

    except Exception as e:
        mensaje_error = f'Error en la predicción: {str(e)}'
        return jsonify({'mensaje_respuesta': mensaje_error, 'valor_predicho': None})

# Función para realizar la predicción
def predict(modelo, datos):
    try:
        # Preparar los datos para la predicción en el mismo orden que se usó durante el entrenamiento
        datos_prediccion = [
            [datos['dormitorio'], datos['banos'], datos['estacionamientos'], datos['operacion'], datos['tipo_propiedad'],
             datos['region'], datos['comuna'], datos['area_total'], datos['area_construida'], datos['condicion'],
             datos['longitud'], datos['latitud']]
        ]

        # Realizar la predicción
        valor_predicho = modelo.predict(datos_prediccion)

        return round(valor_predicho[0], 2)  # Redondear el valor de predicción a 2 decimales

    except Exception as e:
        return f"Error en la predicción: {str(e)}"

# Función para transformar datos a números
def transformar_dato(dato, dato_dict):
    return dato_dict.get(dato.lower(), -1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    