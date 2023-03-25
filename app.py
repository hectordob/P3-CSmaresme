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
        rol = request.form['rol']
        password = request.form['password']
        funcionesbbdd.insert_user(nombre, apellido1, apellido2, nacimiento, email, telefono, usuario, password, rol)
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


if __name__ == '__main__':
    app.run(debug=True)
