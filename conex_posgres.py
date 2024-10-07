import psycopg2

def crear_conexion():
    try:
        connection = psycopg2.connect(
            host="localhost",  # o la IP del servidor donde está PostgreSQL
            database="SistemaFinanciero",  # nombre de tu base de datos
            user="postgres",  # tu usuario de PostgreSQL
            password="123456",  # la contraseña de tu usuario
            port="5432"  # el puerto, usualmente es 5432
        )
        print("hola")
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

