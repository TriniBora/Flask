from flask import Flask
from flask import render_template, url_for, request, redirect, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'emple_dep'

conexion = MySQL(app)


@app.before_request
def before_request():
    print('Antes de la petición...')


@app.after_request
def after_request(response):
    print('Después de la petición...')
    return response


@app.route('/')
def index():
    # return '<h1>Dame un mate!!</h1>' #puede retornar algo estático
    cursos = ['PHP', 'Pyhon', 'Java', 'Kotlin', 'Dart', 'JavaScripts']

    data = {
        'titulo': 'Index',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_cursos': len(cursos),
    }

    return render_template('index.html', data=data)


@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }

    return render_template('contacto.html', data=data)


def query_string():  # obtener un/os parametro/s a traves de una url
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return 'OK'


@app.route('/departamentos')
def listar_departamentos():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id_depto, nombre_depto FROM departamentos ORDER BY nombre_depto ASC"
        cursor.execute(sql)
        departamentos=cursor.fetchall()
        #print(departamentos)#muestro lo que traigo de la bd por consola
        data['departamentos'] = departamentos
        #data['mensaje']='Éxito!' #mensaje para comprobar si andaba la conexion
    except Exception as ex:
        data['mensaje']='Error...'
    #return jsonify(data) #muestro lo que traigo de la bd en el html como json
    return render_template('departamentos.html', data=data)


def pagina_no_encontrada(error):
    # return render_template('404.html'), 404 #le asociamos el codigo de error #retorno una vista especial
    # redireccionamos a otra vista, en este caso el indice
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)  # habilito el modo debug y elijo el puerto
