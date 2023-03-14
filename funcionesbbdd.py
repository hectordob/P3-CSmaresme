import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

def nuevousuario(nombre,apellido1,apellido2,fecha_nac,email,telefono,usuario,password):
    conn = sqlite3.connect('maresme.sqlite')
    sql = '''
        INSERT INTO usuarios(nombre,apellido1,apellido2,fecha_nac,email,telefono,usuario,password) VALUES(?,?,?,?,?,?,?,?)
        '''
    VALUES = [nombre,apellido1,apellido2,fecha_nac,email,telefono,usuario,generate_password_hash(password)]
    conn.execute(sql,VALUES)
    conn.commit()
    conn.close()