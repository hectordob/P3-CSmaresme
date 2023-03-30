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


def database_interaction(sql=None, values=None, get_result=False):
    conn = sqlite3.connect('maresme.sqlite')
    if sql is not None:
        if values is None:
            cursor = conn.execute(sql)
        else:
            cursor = conn.execute(sql, values)
        if get_result is True:
            colnames = [row[0] for row in cursor.description]
            elements = []
            for i, element in enumerate(cursor):
                elements.append({})
                for j, colname in enumerate(colnames):
                    elements[i][colname] = element[j]
            conn.commit()
            conn.close()
            return elements
        conn.commit()
        conn.close()


def show_user(idusuario=None, rol=None):
    if idusuario:
        if rol == 'admin':
            sql = 'SELECT * FROM usuarios WHERE idusuario=?'
            return database_interaction(sql=sql, values=[idusuario], get_result=True)
        sql = 'SELECT nombre, apellido1, apellido2, fecha_nac, email, telefono, fecha_alta, usuario, password FROM usuarios WHERE idusuario=?'
        return database_interaction(sql=sql, values=[idusuario], get_result=True)
    else:
        if rol == 'admin':
            sql = 'SELECT * FROM usuarios'
            return database_interaction(sql=sql, get_result=True)
        sql = 'SELECT nombre, apellido1, apellido2, fecha_nac, email, telefono, fecha_alta, usuario, password FROM usuarios'
        return database_interaction(sql=sql, get_result=True)


def update_user(nombre, apellido1, apellido2, fecha_nac, email, telefono, usuario, password, id):
    values = [nombre, apellido1, apellido2, fecha_nac, email, telefono, usuario, generate_password_hash(password), id]
    sql = 'UPDATE usuarios SET nombre=?, apellido1=?, apellido2=?, fecha_nac=?, email=?, telefono=?, usuario=?, password=? WHERE idusuario=?'
    database_interaction(sql=sql, values=values)


def delete_user(idusuairo):
    values = [idusuairo]
    sql = 'DELETE FROM usuarios WHERE idusuario=?'
    database_interaction(sql=sql, values=values)


def create_articulo(idprestador, titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1):
    values = [idprestador, titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1]
    sql = 'INSERT INTO articulos(idprestador, titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    database_interaction(sql, values)


def show_articulos(idarticulo=None, rol=None):
    if idarticulo:
        if rol == 'admin':
            sql = 'SELECT * FROM articulos WHERE idarticulo=?'
            return database_interaction(sql=sql, values=[idarticulo], get_result=True)
        sql = 'SELECT titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1 FROM articulos WHERE idarticulo=?'
        return database_interaction(sql=sql, values=[idarticulo], get_result=True)
    else:
        if rol == 'admin':
            sql = 'SELECT * FROM articulos'
            return database_interaction(sql=sql, get_result=True)
        sql = 'SELECT titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1 FROM articulos'
        return database_interaction(sql=sql, get_result=True)


def update_articulo(titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1, idarticulo):
    values = [titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1, idarticulo]
    sql = 'UPDATE articulos SET titulo=?, autor=?, editorial=?, year=?, categoria=?, edad_min=?, descripcion=?, imagen1=? WHERE idarticulo=?'
    database_interaction(sql=sql, values=values)


def delete_articulo(idarticulo):
    sql = 'DELETE FROM articulos WHERE idarticulo=?'
    values = [idarticulo]
    database_interaction(sql, values)


def own_articulos(idprestador):
    sql = 'SELECT * FROM articulos WHERE idprestador=?'
    return database_interaction(sql=sql, values=[idprestador], get_result=True)


def show_articulos_user(idprestador=None, rol=None):
    if ideprestador:
        if rol == 'admin':
            sql = 'SELECT * FROM articulos WHERE idprestador=?'
            return database_interaction(sql=sql, values=[idprestador], get_result=True)
        sql = 'SELECT titulo, autor, editorial, year, categoria, edad_min, descripcion, imagen1 FROM articulos WHERE idprestador=?'
        return database_interaction(sql=sql, values=[idarticulo], get_result=True)


# ====================================================================================================
# 2 - PRESTAMOS
# ====================================================================================================
def create_prestamo(idusuario, idarticulo):
    fecha_ini = date.today()
    values = [idusuario, idarticulo, fecha_ini]
    sql = 'INSERT INTO prestamos(idusuario, idarticulo, fecha_ini) VALUES (?, ?, ?)'
    database_interaction(sql, values)


def show_prestamos(idprestamo=None, rol=None):
    if idprestamo:
        if rol == 'admin':
            sql = 'SELECT * FROM prestamos WHERE idprestamo=?'
            return database_interaction(sql=sql, values=[idprestamo], get_result=True)
        sql = 'SELECT fecha_ini, fecha_fin, devuelto, observaciones FROM prestamos WHERE idprestamo=?'
        return database_interaction(sql=sql, values=[idprestamo], get_result=True)
    else:
        if rol == 'admin':
            sql = 'SELECT * FROM prestamos'
            return database_interaction(sql=sql, get_result=True)
        sql = 'SELECT fecha_ini, fecha_fin, devuelto, observaciones FROM prestamos WHERE idprestamo=?'
        return database_interaction(sql=sql, get_result=True)


def update_prestamo(idusuario, idarticulo, fecha_ini, devuelto, observaciones, idprestamo):
    if devuelto == 1:
        fecha_fin = date.today()
        sql = 'UPDATE prestamos SET idusuario=?, idarticulo=?, fecha_ini=?, fecha_fin=?, devuelto=?, observaciones=? WHERE idprestamo=?'
        database_interaction(sql,
                             values=[idusuario, idarticulo, fecha_ini, fecha_fin, devuelto, observaciones, idprestamo])
    else:
        sql = 'UPDATE prestamos SET idusuario=?, idarticulo=?, fecha_ini=?, devuelto=?, observaciones=? WHERE idprestamo=?'
        database_interaction(sql, values=[idusuario, idarticulo, fecha_ini, devuelto, observaciones, idprestamo])


def delete_prestamo(idprestamo):
    sql = 'DELETE FROM prestamos WHERE idprestamo=?'
    values = [idprestamo]
    database_interaction(sql, values)


def own_prestamos(idprestante):
    sql = 'SELECT * FROM prestamos WHERE idprestante=?'
    return database_interaction(sql=sql, values=[idprestante], get_result=True)
