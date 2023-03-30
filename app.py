from flask import *
import funcionesbbdd
from functools import wraps

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'ssadvwqvgfqgrytasddfgjcbmklñpoeqz'


@app.route('/logout/')
def logout():
    if request.method == 'GET':
        session.pop('logged')
        if 'admin' in session:
            session.pop('admin')
        return redirect(url_for('home'))


def login_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        if 'logged' not in session:
            flash('Es necesario iniciar sesión')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return check_token

def admin_required(f):
    @wraps(f)
    def check_rol(id=None, *args, **kwargs):
        if session['rol'] != 'admin':

            flash('Se requieren permisos especiales')
            return redirect(url_for('home'))
        else:
            if id is None:
                return f(*args, **kwargs)
            else:
                return f(id, *args, **kwargs)
    return check_rol



@app.route('/home')
def get_admin():
    if 'admin' in session:
        return render_template('admin.html')
    if 'logged' in session:
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/register', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        nacimiento = request.form['nacimiento']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        password = request.form['password']
        funcionesbbdd.insert_user(nombre, apellido1, apellido2, nacimiento, email, telefono, usuario, password)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usuario = request.form['usuario']
        password = request.form['password']
        check = funcionesbbdd.check(usuario, password)

        if check == 'admin':
            session['logged'] = 'hdffddsdaihlcutdcilñcretckjdfhvcb'
            session['admin'] = 'yes'
            return redirect(url_for('admin'))

        elif check == True:
            session['logged'] = 'hdffddsdaihlcutdcilñcretckjdfhvcb'
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))


@app.route('/articulos/')
@login_required
def mostrar_articulos():
    datos = funcionesbbdd.show_articulos(rol='admin')
    mis_articulos = funcionesbbdd.funcionesbbdd.own_articulos(idprestador=session['idusuario'])
    idsarticulos = [articulo['idarticulo'] for articulo in mis_articulos]
    return render_template('mostrar_articulos.html',
                           datos=datos,
                           idsarticulos=idsarticulos,
                           idusuario=session['idusuario'],
                           rol=session['rol'])


@app.route('/articulos/<idarticulo>/')
@login_required
def mostrar_articulo(idarticulo):
    datos = funcionesbbdd.show_articulos(idarticulo=idarticulo, rol='admin')
    mis_articulos = funcionesbbdd.funcionesbbdd.own_articulos(idprestador=session['idusuario'])
    idsarticulos = [articulo['idarticulo'] for articulo in mis_articulos]
    return render_template('mostrar_articulos.html',
                           datos=datos,
                           idsarticulos=idsarticulos,
                           idusuario=session['idusuario'],
                           rol=session['rol'])


@app.route('/articulos/mis_articulos/')
@login_required
def mis_articulos():
    if session['rol'] == 'user':
        datos = funcionesbbdd.funcionesbbdd.own_articulos(session['idusuario'])
        return render_template('mostrar_articulos.html', datos)
    return redirect(url_for('mostrar_articulos'))


@app.route('/articulos/crear/', methods=['GET', 'POST'])
@login_required
def crear_articulo():
    if request.method == 'GET':
        return render_template('add_article.html')
    else:
        idprestador = session['idusuario']
        titulo = request.form['titulo']
        autor = request.form['autor']
        editorial = request.form['editorial']
        year = request.form['year']
        categoria = request.form['categoria']
        edad_min = request.form['edad_min']
        descripcion = request.form['descripcion']

        imagen1 = request.files['imagen1']
        filename = secure_filename(imagen1.filename)
        imagen1.save(f'./static/images/{filename}')  # DESDE PERSPECTIVA DE APP
        imagen1 = f'/static/images/{filename}'  # DESDEPERSPECTIVA DE HTML
        # imagen1.save(path.join(app.config['UPLOAD_FOLDER'], filename))
        # imagen1 = path.join(app.config['UPLOAD_FOLDER'], filename)

        funcionesbbdd.create_articulo(idprestador, titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1)

        idarticulo = funcionesbbdd.show_articulos(rol='admin')[-1]['idarticulo']
        return redirect(url_for('mostrar_articulo', idarticulo=idarticulo))
        # return redirect(url_for('articulos'))


@app.route('/articulos/<idarticulo>/borrar/')
@login_required
def borrar_articulo(idarticulo):
    print('permiso aceptado')
    funcionesbbdd.delete_articulo(idarticulo=idarticulo)
    return redirect(url_for('articulos'))


@app.route('/articulos/<idarticulo>/actualizar/', methods=['GET', 'POST'])
@login_required
def actualizar_articulo(idarticulo):
    if request.method == 'GET':
        datos = funcionesbbdd.show_articulos(rol=session['rol'])
        return render_template('actualizar_articulo.html', datos=datos)
    else:
        idprestador = session['idusuario']
        titulo = request.form['titulo']
        autor = request.form['autor']
        editorial = request.form['editorial']
        year = request.form['year']
        categoria = request.form['categoria']
        edad_min = request.form['edad_minima']
        descripcion = request.form['descripcion']
        imagen1 = request.files['imagen1']
        print('antes', imagen1)
        imagen1.save(secure_filename(imagen1.filename))
        imagen1 = imagen1.filename
        print('despues', imagen1)
        funcionesbbdd.create_articulo(idprestador, titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1)
        return redirect(url_for('mostrar_articulo', idarticulo=idarticulo))
        # return redirect(url_for('articulos'))


# ====================================================================================================
# 9 - PRESTAMOS
# ====================================================================================================
@app.route('/prestamos/')
@login_required
@admin_required
def mostrar_prestamos():
    funcionesbbdd.show_prestamos(rol=session['rol'])
    return render_template('mostrar_prestamos.html')


@app.route('/prestamos/<idprestamo>/')
@login_required
def mostrar_prestamo(idprestamo):
    datos = funcionesbbdd.show_prestamos(idprestamo=idprestamo, rol=session['rol'])
    return render_template('mostrar_prestamos.html', datos=datos)


@app.route('/prestamos/mis_prestamos/')
@login_required
def mis_prestamos():
    if session['rol'] == 'user':
        datos = own_prestamos(session['idusuario'])
        return render_template('mostrar_prestamos.html', datos=datos)
    return redirect(url_for('mostrar_prestamos'))


""" CREAR: UN PRESTAMO NO SE CREA CON UN FORMULARIO, SE EJECUTA SI SE DA A UN BOTON """


@app.route('/prestamos/crear/')
@login_required
def crear_prestamo():
    idusuario = session['idusuario']
    idarticulo = request.args['idarticulo']
    funcionesbbdd.create_prestamo(idusuario, idarticulo)

    idprestamo = funcionesbbdd.show_prestamos(rol=session['rol'])[-1]['idprestamo']
    return redirect(url_for('prestamo', idprestamo=idprestamo))




if __name__ == '__main__':
    app.run(debug=True)
