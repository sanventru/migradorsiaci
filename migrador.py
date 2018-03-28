import os
import sys
import pyodbc
import requests
import datetime
import simplejson as json
import winreg


hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\ODBC\ODBC.INI\spagfic")
registrov = str(winreg.QueryValueEx(hKey, "CommLinks")).split('=')[1].split('}')[0]


server_rest = 'http://' + registrov + ':8000'
#server_rest = 'http://186.4.251.26:8000'
#server_rest = 'http://localhost:8000'

database = 'interface'
username = 'SAC'
password = 'SAC'

#database = 'interface' 
#username = 'sa' 
#password = 'quinde07'

desde = ''
hasta = ''
tipo = ''

parametros = sys.argv # Fecha_inicio Fecha_fin Tipo
desde = parametros[1].replace('_', ' ')
hasta = parametros[2].replace('_', ' ')
tipo = parametros[3]
estacion = parametros[4]

#desde = '2018-01-01'
#hasta = '2019-01-01'
#tipo = 1
#estacion = 'san'



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
r = requests.post(server_rest + '/insertpost', json=j)
if r.status_code == requests.codes.ok:
    print('si')
else:
    print('no')
cur.close()
conn.close()
