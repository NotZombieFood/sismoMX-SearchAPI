import gspread
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from oauth2client.service_account import ServiceAccountCredentials

import json
import os

param="Adriana Sánchez Perez"
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('sismoAPI-cfab23253d15.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1a-rZqtPUvHn-73sZEb7Epn4R9ouTiMfjPOysB-4hLYA')
print("Worksheet obtenida")
worksheet = sh.worksheet("Encontrados")
encontrados = worksheet.get_all_values()
worksheet2 = sh.worksheet("Desaparecidos")
desaparecidos = worksheet2.get_all_values()
listaEncontrados = []
for i in range(len(encontrados)):
    ratio = fuzz.partial_ratio(param,encontrados[i][0])
    if (ratio>77):
        listaEncontrados.append(encontrados[i][0])
    i+=1
listaDesaparecidos = []
for i2 in range(len(desaparecidos)):
    ratio = fuzz.partial_ratio(param,desaparecidos[i2][0])
    if (ratio>77):
        listaDesaparecidos.append(desaparecidos[i2][0])
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
print (htmlString)
