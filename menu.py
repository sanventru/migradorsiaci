import os
import pyodbc
import requests
import datetime
import simplejson as json

server = 'tcp:localhost'
database = 'msp'
username = 'sa'
password = 'quinde07'
desde = ''
hasta = ''
tipo = ''


def menu():
    os.system('cls')  # NOTA para windows tienes que cambiar clear por cls
    print("Selecciona una opción")
    print("\t1 - Ingresar parámetros y procesar")
    print("\t2 - Ejecutar")
    # print ("\t3 - tercera opción")
    print("\t9 - salir")


while True:
    menu()
    opcionMenu = input("inserta un numero valor >> ")
    if opcionMenu == "1":
        print("")
        while True:
            desde = input('Desde (yyyy-mm-dd): ')
            try:
                desde1 = datetime.datetime.strptime(desde, '%Y-%m-%d')
                break
            except ValueError:
                print('Dato erróneo!')
                continue
        while True:
            hasta = input('Hasta (yyyy-mm-dd): ')
            try:
                hasta1 = datetime.datetime.strptime(hasta, '%Y-%m-%d')
                break
            except ValueError:
                print('Dato erróneo!')
                continue
        while True:
            tipo = input('Tipo : ')
            try:
                tipo = int(tipo)
                break
            except ValueError:
                print('Dato erróneo!')
                continue
    elif opcionMenu == "2":
        conn = pyodbc.connect('DSN=pruebaproc;UID=SA;PWD=quinde07')
        cur = conn.cursor()
        params = ("error", desde, hasta, tipo)
        cur.execute("{CALL sp_IntegraContabilidad (?,?,?,?)}", params)
        data_json = []
        header = [i[0] for i in cur.description]
        data = cur.fetchall()
        for i in data:
            data_json.append(dict(zip(header, i)))
        j = data_json
        j = json.loads(json.dumps(j, use_decimal=True))
        r = requests.post('http://localhost:8000/insertpost', json=j)
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
