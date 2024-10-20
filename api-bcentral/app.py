from flask import Flask, jsonify, request
from datetime import date
import requests
import json

############################################################################################################################################################
#Inicio App con Flask
app = Flask(__name__)

# API Inicio Home
@app.route('/')
def hello_world():
    return 'Conversor de Moneda usando API Banco Central'

############################################################################################################################################################
# API Banco Central
############################################################################################################################################################
# Descripcion: consulta el valor del dolar y transforma el dolar solicitado a moneda local (CLP)
############################################################################################################################################################
@app.route("/usdtoclp", methods=['GET'])
def dolar_a_peso():
    # Configuracion de Credenciales BCENTRAL
    #base_url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    #user = "carl.aravena@duocuc.cl"
    #password = "R27029155-4"
    #fechaIni = "2024-05-03"
    #fechaFin = "2024-05-03"
    #timeseries = "F073.TCO.PRE.Z.D"
    #funcion = "GetSeries"

    # Obtener el parámetro 'param' de la URL
    param_dolar = request.args.get('usd')

    if not param_dolar.isnumeric():
        return jsonify({'error': 'El parametro no es un dato numerico, no se aceptan caracteres'}), 404

    fecha_hoy = str(date.today())

    # Configuracion URL
    url = f'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=carl.aravena@duocuc.cl&pass=R27029155-4&firstdate={fecha_hoy}&lastdate={fecha_hoy}&timeseries=F073.TCO.PRE.Z.D&function=GetSeries'

    # Realizar la solicitud GET a la API
    response = requests.get(url)
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200 and param_dolar:
        # Convertir la respuesta JSON a un diccionario de Python
        data = response.json()
        # Obtener el valor de "value" de "obs"
        valor = data["Series"]["Obs"][0]["value"]
        clp = float(valor)*float(param_dolar)
        return jsonify(
          fecha_consultada=str(fecha_hoy),
          dolar_consultado=str(param_dolar),
          valor_clp=str(clp)
        )
        #return "Valor en CLP: "+ str(clp)
    else:
        return "Error al realizar la solicitud a la API: "+ response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)