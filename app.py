from flask import *
import funcionesbbdd

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/contacto')
def contacto():
    return render_template('Contacto.html')


@app.route('/register', methods=['GET', 'POST'])
def crearusuario():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        fecha_nac = request.form['fecha_nac']
        email = request.form['email']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        password = request.form['password']
        funcionesbbdd.nuevousuario(nombre, apellido1, apellido2, fecha_nac, email, telefono, usuario, password)
    # return redirect('/register')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug='True')
