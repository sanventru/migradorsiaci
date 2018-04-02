from flask import Flask, request
from flask_twisted import Twisted
import sqlanydb

app = Flask(__name__)
app.secret_key = 'siaci 2018 rep0rt3r14.!'
# twisted = Twisted(app)

host = 'localhost'
eng = 'siaci_db'
pwd = '197304'
uid = 'dba'


@app.route('/')
def home():
    return('Migrador Siaci')


@app.route('/insertget/<registros>', methods=['GET'])
def datos(registros):
    return(registros)


@app.route('/insertpost', methods=['POST'])
def datospost():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Mensaje: " + str(request.data)

    elif request.headers['Content-Type'] == 'application/json':
        conn = sqlanydb.connect(uid=uid, pwd=pwd, eng=eng,
                                host=host, preFetchRows='15000')
        curs = conn.cursor()
        rows = request.json
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
        conn.commit()
        conn.close()
        return "JSON Mensaje"

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Dato binario!"
    else:
        return "415 Tipo no soportado ;)"


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'memcached'
    app.run(host='0.0.0.0', port=8000, debug=True)
    # app.run(debug=True, host='0.0.0.0', port=5000)
