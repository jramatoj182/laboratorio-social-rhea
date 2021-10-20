import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= 'socialrhea.db'
    conn= sqlite3.connect(dbname)
    return conn

def getUser(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Usuario WHERE Usuario = ?'
      cursor = conn.execute(sql, (user,))
      resultados = (cursor.fetchone())
      cursor.close()
      conn.close()
      if not resultados:
        return False
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getFotos(Posts):
    conn= conectar()
    token = Posts[2]['token']
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Foto WHERE token = ?'
      cursor = conn.execute(sql, (token,))
      resultados = (cursor.fetchall())
      results = [ dict(row) for row in resultados ]
      conn.close()
      print(token)
      print(resultados)
      if not results:
        return False
      else:
        print("Las fotos son:")
        print(results)
        return results
    except Error as e:
      print(f"error in getFotos() : {str(e)}"  )

def getUserAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_admin WHERE User = '"+ user +"';")
      resultados = dict(cursor.fetchone())
      if not resultados:
        print ('Login failed')
        return False
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
    finally:
        if conn:
            cursor.close()
            conn.close()

def getUserSuperAdmin(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_super_admin WHERE User = '"+ user +"';")
      resultados = dict(cursor.fetchone())
      if not resultados:
        print ('Login failed')
        return False
      else:
        return resultados
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
    finally:
        if conn:
            cursor.close()
            conn.close()

def getUsersByName(user):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_Users WHERE nombre like '%"+ user +"%';")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getUsers():
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM Usuario WHERE rol=2;")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getMensaje(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM tbl_mensajes where (remitente = ? OR remitente = ?) AND (receptor = ? OR receptor = ?);'
      cursor= conn.execute(sql, (emisor, receptor, receptor, emisor))
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      print(results)
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )


def getRelacion(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Amistad where (id_envia = ? AND id_recibe = ?) AND (id_recibe = ? AND id_envia = ?);'
      cursor= conn.execute(sql, (emisor, receptor, receptor, emisor))
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      if (results):
        return True
      else:
        return False
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def deleteRelacion(emisor, receptor):
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      sql = 'DELETE FROM Amistad where (id_envia = ? AND id_recibe = ?)'
      conn.execute(sql, (emisor, receptor,))
      conn.commit()
      conn.close()
      return True
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )
      return False

def getSuperUsers():
    conn= conectar()
    try:
      conn.row_factory = sqlite3.Row
      cursor= conn.execute("SELECT * FROM tbl_admin;")
      resultado = (cursor.fetchall())
      results = [ dict(row) for row in resultado ]
      conn.close()
      return results
    except Error as e:
      print(f"error in getUser() : {str(e)}"  )

def getPosts(idUsuario):
    try:
      print("Esta Buscando el usuario: "+str(idUsuario))
      conn= conectar()
      conn.row_factory = sqlite3.Row
      sql = 'SELECT * FROM Post WHERE ID_Usuario = ?;'
      cursor = conn.execute(sql, (idUsuario,))
      resultados= [ dict(row) for row in cursor ]
      print(resultados)
      conn.close()
      return resultados
    except Error as e:
      print(f"error in getPost() : {str(e)}"  )

def getPostByUser(user):
    conn= conectar()
    cursor= conn.execute("SELECT * FROM imagenes WHERE user = '"+ user +"' ORDER BY codigo DESC;")
    resultados= list(cursor.fetchall())
    conn.close()
    return resultados

def getPostById(idPost):
    conn= conectar()
    sql = 'SELECT * FROM imagenes WHERE codigo = ?;'
    cursor= conn.execute(sql, (idPost,))
    resultados= list(cursor.fetchone())
    conn.close()
    return resultados

def addPost(arregloImagenes , status, Titulo, idUser, visibilidad, postToken):
  
    try :
        conn=conectar()
        conn.execute("INSERT INTO Post (ID_Usuario , Titulo, Visibilidad, Descripcion, token) values(?,?,?,?,?);", (idUser, Titulo, visibilidad, status, postToken))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def addFoto(imagen, token):
    try:
      conn=conectar()
      conn.execute("INSERT INTO Foto (Ruta, token) values(?,?);", (imagen, token))
      conn.commit()
      conn.close()
      return True
    except Error as error:
      return False

def addMensaje(remitente, receptor, contenido):
    try :
        conn=conectar()
        conn.execute("insert into tbl_mensajes (remitente, receptor, contenido) values(?,?,?);", (remitente, receptor, contenido))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    
def addUser(usuario, password, nombres, apellidos, genero, email, pais, Foto, telefono , nacimiento, Estado_Civil, privacidad):
    rol = 2
    estado = 1
    try :
        conn=conectar()
        conn.execute("INSERT INTO Usuario (Usuario, Contrasena, Rol, Estado, Nombres, Apellidos, Genero, Email, Ubicacion, Foto, Telefono, Fecha_Nacimiento, Estado_Civil, Privacidad ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (usuario, password, rol, estado, nombres, apellidos, genero, email, pais, Foto, telefono , nacimiento, Estado_Civil, privacidad))
        conn.commit()
        conn.close()
        print('Registro Exitoso')
        return True
    except Error as error:
        print("error en Add User:", error)
        return False
      
def addAdmin(user, name, password, profPic, highPic, country):
    try :
        conn=conectar()
        conn.execute("insert into tbl_admin (user, name, passwrd, profPic, highPic, country) values(?,?,?,?,?,?);", (user, name, password, profPic, highPic, country))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
      
      
def addAmigo(envia, recibe):
    try :
        conn=conectar()
        conn.execute("INSERT into amistad (id_envia, id_recibe) values(?,?);", (envia, recibe))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
      
def updateUser(user, nombres, password, filename, pais):
    try :
        print('entro')
        conn=conectar()
        conn.execute("UPDATE tbl_Users SET name=?, passwrd = ?, profPic = ?, country = ? WHERE user = ?;", (nombres, password, filename, pais, user))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False
    
def deleteUser(user):
    try :
        conn=conectar()
        sql = 'DELETE FROM tbl_Users WHERE User = ?'
        conn.execute(sql, (user,))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

def deleteAdmin(user):
    try :
        conn=conectar()
        sql = 'DELETE FROM tbl_admin WHERE User = ?'
        conn.execute(sql, (user,))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
    

def deletePost(idPost):
    try :
        conn=conectar()
        sql = 'DELETE FROM imagenes WHERE codigo = ?'
        conn.execute(sql, (idPost,))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False
