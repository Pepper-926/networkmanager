from flask import Flask, render_template, request, redirect, url_for, session
import secrets  # Genera claves
from APIDB import ApiDBGabriel

app = Flask(__name__)
app.secret_key = f'{secrets.token_hex(32)}'  # Genera una clave cada vez que se inicia el servidor.
#Es necesaria para trabajar con sesiones
db_conn = ApiDBGabriel()

#Gabriel
@app.route('/inicio', methods=['GET', 'POST'])
def index():
    return redirect(url_for('logs'))



@app.route('/', methods=['GET','POST'])
def logs():
    opciones = db_conn.obtener_opciones_logs()
    if session.get('logs'):
            return render_template('logs.html', opciones = opciones, logs = session.get('logs'))
    return render_template('logs.html', opciones = opciones)

#Esta ruta es solo para procesar los datos que se envian desde el form de logs, no renderiza ningun html
@app.route('/filtrar_logs', methods=['GET'])
def filtrar_logs():
    hostname = request.args.get('hostname')  # Será None si no se selecciona nada
    codigo_sys = request.args.get('codigo_sys')  #Devuelve '' si esta vacio
    n_secuencia = request.args.get('numero_secuencia')  #Devuelve '' si esta vacio
    fecha_hora_inicio = request.args.get('fecha_hora_inicio')  #Devuelve '' si esta vacio
    fecha_hora_fin = request.args.get('fecha_hora_fin')  #Devuelve '' si esta vacio
    subsistema = request.args.get('subsistema')  # Será None si no se selecciona nada
    nivel = request.args.get('nivel')  # Será None si no se selecciona nada
    tipo_evento = request.args.get('tipo_evento')  # Será None si no se selecciona nada

    #Construimos el diccionario que contendra todos los filtros necesarios
    filtros = {
        'hostname':hostname,
        'codigo_sys':codigo_sys,
        'n_secuencia':n_secuencia,
        'fecha_inicio':fecha_hora_inicio,
        'fecha_fin':fecha_hora_fin,
        'subsistema':subsistema,
        'nivel':nivel,
        'tipo_evento':tipo_evento
    }

    session['logs'] = db_conn.filtrar_logs(filtros)

    return redirect(url_for('logs'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)