import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='prueba'
        )
        if connection.is_connected():
            print('Conexión exitosa')
            return connection
        else:
            print('Conexión fallida')
            return None
    except mysql.connector.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def insertar_datos(nombre, apellido, cedula, imagen_blob, face_encoding):
    try:
        conexion = get_connection()
        if not conexion:
            return False
        
        cursor = conexion.cursor()
        
        query = """
            INSERT INTO alumnos (nombre, apellido, cedula_de_identidad, foto, face_encoding) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, apellido, cedula, imagen_blob, face_encoding)
        
        cursor.execute(query, valores)
        conexion.commit()
        print("Datos insertados correctamente")
        return True
        
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        return False
        
    finally:
        if 'conexion' in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()

# Bloque de prueba
if __name__ == "__main__":
    # Prueba de conexión
    conexion = get_connection()
    if conexion:
        conexion.close()