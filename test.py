import gspread
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import json
import os
import time, threading


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
# 	for i2 in range(len(magiclist[i])):
# 		print(magiclist[i][i2])
# 		i2+=1
# 	i+=1
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


