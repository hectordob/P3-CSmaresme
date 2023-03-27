import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def insert_user(nombre, apellido1, apellido2, nacimiento, email, telefono, usuario, password):
    conn = sqlite3.connect('maresme.sqlite')
    sql = '''insert into usuarios(nombre,apellido1,apellido2,fecha_nac,email,telefono,usuario, password) values (?,?,?,?,?,?,?,?)'''
    values = [nombre, apellido1, apellido2, nacimiento, email, telefono, usuario, generate_password_hash(password)]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def check(usuario, password):
    conn = sqlite3.connect('maresme.sqlite')
    sql = '''select usuario,password,rol from usuarios'''
    cursor = conn.execute(sql)
    users = []
    for row in cursor:
        users.append(
            {
                'usuario': row[0],
                'password': row[1],
                'rol': row[2]
            }
        )
    conn.close()
    for i in range(len(users)):
        check_pass = check_password_hash(users[i]['password'], password)
        if usuario == users[i]['usuario'] and check_pass == True and users[i]['rol'] == 'admin':
            return 'admin'
        if usuario == users[i]['usuario'] and check_pass == True:
            return True
        else:
            final = False
    return final
