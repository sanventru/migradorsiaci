# -*- coding: utf-8 -*-
import os
import pyodbc
import requests
import datetime
import simplejson as json

server_rest = 'http://192.168.0.153:8000'
#server_rest = 'http://186.4.251.26:8000'
#server_rest = 'http://localhost:8000'

server = 'tcp:localhost'
#database = 'interface'
#username = 'SAC'
#password = 'SAC'

database = 'pruebaproc' 
username = 'sa' 
password = 'quinde07'

desde = ''
hasta = ''
tipo = ''


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def menu():
    #os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 - Ingresar parámetros y procesar")
    print("\t2 - Ejecutar")
    # print ("\t3 - tercera opción")
    print("\t9 - salir")


while True:
    menu()
    opcionMenu = input("inserta un número valor >> ")
    if opcionMenu == "1":
        print("")
        desde = input('Desde (yyyy-mm-dd): ')
        hasta = input('Hasta (yyyy-mm-dd): ')
        tipo = input('Tipo : ')
	# while True:
            # desde = input('Desde (yyyy-mm-dd): ')
            # try:
                # desde1 = datetime.datetime.strptime(desde, '%Y-%m-%d')
                # break
            # except ValueError:
                # print('Dato errÃ³neo!')
                # continue
        # while True:
            # hasta = input('Hasta (yyyy-mm-dd): ')
            # try:
                # hasta1 = datetime.datetime.strptime(hasta, '%Y-%m-%d')
                # break
            # except ValueError:
                # print('Dato errÃ³neo!')
                # continue
        # while True:
            # tipo = input('Tipo : ')
            # try:
                # tipo = int(tipo)
                # break
            # except ValueError:
                # print('Dato errÃ³neo!')
                # continue
    elif opcionMenu == "2":
        conn = pyodbc.connect('DSN=' + database + ';UID=' + username + ';PWD=' + password)
        cur = conn.cursor()
        params = ("error", desde, hasta, tipo)
        cur.execute("{CALL sp_IntegraContabilidad (?,?,?,?)}", params)
        data_json = []
        header = [i[0] for i in cur.description]
        data = cur.fetchall()
        for i in data:
            data_json.append(dict(zip(header, i)))
        j = data_json
        f = open('a.txt','w')
        f.write(str(j))
        f.close()		
        j = json.loads(json.dumps(j, use_decimal=True, default = myconverter))
        r = requests.post(server_rest + '/insertpost', json=j)
        print(str(r.text))
        cur.close()
        conn.close()
    elif opcionMenu == "3":
        print("")
        input("Has pulsado la opción 3...\npulsa una tecla para continuar")
    elif opcionMenu == "9":
        break
    else:
        print("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
