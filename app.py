# Imports
import json
import os
import time, threading
from datetime import timedelta
import sys
import math
import requests
from flask import Flask, request, render_template, send_file, make_response, current_app
import argparse
from functools import update_wrapper
import requests
import time
import string
from flask_cors import CORS
import gspread
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('sismoAPI-cfab23253d15.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1a-rZqtPUvHn-73sZEb7Epn4R9ouTiMfjPOysB-4hLYA')
worksheet = sh.worksheet("Encontrados")
encontrados = worksheet.get_all_values()
worksheet2 = sh.worksheet("Desaparecidos")
desaparecidos = worksheet.get_all_values()

# for i in range(len(magiclist)):
#   for i2 in range(len(magiclist[i])):
#       print(magiclist[i][i2])
#       i2+=1
#   i+=1
def buscarEncontrados(param):
    listaEncontrados = []
    for i in range(len(encontrados)):
        ratio = fuzz.partial_ratio(param,encontrados[i][0])
        if (ratio>75):
            listaEncontrados.append(encontrados[i][0])
        i+=1
    return listaEncontrados

def buscarDesaparecidos(param):
    listaDesaparecidos = []
    for i in range(len(desaparecidos)):
        ratio = fuzz.partial_ratio(param,desaparecidos[i][0])
        if (ratio>75):
            listaDesaparecidos.append(desaparecidos[i][0])
        i+=1
    return listaDesaparecidos


def set_globvar():              # setear variables globales
    global desaparecidos
    desaparecidos = 1
    global encontrados
    encontrados = 1

def getsheet():  #valores globales para no tener que estar haciendo llamadas tan seguido, es tardado
    gc = gspread.authorize(credentials)
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1a-rZqtPUvHn-73sZEb7Epn4R9ouTiMfjPOysB-4hLYA')
    print("Worksheet obtenida")
    worksheet = sh.worksheet("Encontrados")
    encontrados = worksheet.get_all_values()
    worksheet2 = sh.worksheet("Desaparecidos")
    desaparecidos = worksheet.get_all_values()

set_globvar()
getsheet()


# %% Flask app
app = Flask(__name__)
CORS(app)

# funcion para buscar por nombre


def buscar(nombre):
    listaEncontrados = []
    for i in range(len(encontrados)):
        ratio = fuzz.partial_ratio(param,encontrados[i][0])
        if (ratio>75):
            listaEncontrados.append(encontrados[i][0])
        i+=1
    listaDesaparecidos = []
    for i2 in range(len(desaparecidos)):
        ratio = fuzz.partial_ratio(param,desaparecidos[i][0])
        if (ratio>75):
            listaDesaparecidos.append(desaparecidos[i][0])
        i2+=1
    if (not listaEncontrados) and (not listaDesaparecidos):
        htmlString = "<h3>Lo sentimos, no encontramos ninguna coincidencia.</h3> <h4>Puedes intentar en las siguientes opciones</h4>"
    else:         
        htmlString = "<h3>Encontramos las siguientes coincidencias:</h3>"
        if (listaEncontrados):
            htmlString += "<h4>En la lista de encontrados:</h4><ul>"
            for x in range(len(listaEncontrados)):
                htmlString += '<li>%s</li>' % (listaEncontrados[x])
            htmlString += '</ul>'
        if (listaDesaparecidos):
            htmlString += '<h4>En la lista de desaparecidos</h4><ul>'
            for y in range(len(listaDesaparecidos)):
                htmlString += '<li>%s</li>' % (listaDesaparecidos[x])
            htmlString += '</ul>'
        htmlString +=  '<br><h4>En caso de no encontrar a la persona que estabas buscando, puedes intentar en las siguientes opciones.<br>Si encontraste a la persona puedes ver más detalles en <a href="https://docs.google.com/spreadsheets/d/1a-rZqtPUvHn-73sZEb7Epn4R9ouTiMfjPOysB-4hLYA">este enlace.</a></h4>'
    return htmlString

# LLamada get con url /persona, acepta solo el nombre como parametro


@app.route('/PERSONA', methods=['GET'])
def getparameters():
    nombre = request.args.get("nombre")
    x = buscar(nombre)
    return x


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
