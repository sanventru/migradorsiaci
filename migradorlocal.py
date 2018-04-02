import os
import sys
import pyodbc
import requests
import datetime
import simplejson as json
import winreg
import sqlanydb


#hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\ODBC\ODBC.INI\spagfic")
#registrov = str(winreg.QueryValueEx(hKey, "CommLinks")).split('=')[1].split('}')[0]


server_rest = 'http://localhost:8000'
#server_rest = 'http://186.4.251.26:8000'
#server_rest = 'http://localhost:8000'

server = 'tcp:localhost'
database = 'interface'
username = 'SAC'
password = 'SAC'

#database = 'pruebaproc' 
#username = 'sa' 
#password = 'quinde07'

desde = ''
hasta = ''
tipo = ''


desde = input('Desde (yyyy-mm-dd): ')
hasta = input('Hasta (yyyy-mm-dd): ')
tipo = input('Tipo : ')
estacion = input('Agencia :')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


conn = pyodbc.connect('DSN=' + database + ';UID=' + username + ';PWD=' + password)
cur = conn.cursor()
params = ("error", desde, hasta, tipo)
cur.execute("{CALL sp_IntegraContabilidad (?,?,?,?)}", params)
data_json = []
header = [i[0] for i in cur.description]
data = cur.fetchall()
for i in data:
    d = dict(zip(header, i))
    d.update({'estacion':estacion})
    data_json.append(d)
j = data_json
j = json.loads(json.dumps(j, use_decimal=True, default = myconverter))
#r = requests.post(server_rest + '/insertpost', json=j)
#if r.status_code == requests.codes.ok:
#    print('si')
#else:
#    print('no')
cur.close()
conn.close()


host = '127.0.0.1'
eng = 'siaci_db'
pwd = '197304'
uid = 'dba'

conn2 = sqlanydb.connect(uid=uid, pwd=pwd, eng=eng, host=host, preFetchRows='15000')
curs = conn2.cursor()
rows = j
for r in rows:
	param = list(r.values())
	#param = param[1:]
	param = str(tuple(param)).replace('None','null')
	columnas = list(r.keys())
	#columnas = columnas[1:]
	columnas = str(tuple(columnas))
	columnas = columnas.replace("'", '')
	sql = "insert into ventas_solintece_tmp " + columnas + " values" + param
	curs.execute(sql)
curs.close()
conn2.commit()
conn2.close()
