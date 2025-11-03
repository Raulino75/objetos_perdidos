import mysql.connector

class Database:
    def __init__(self):
        # Ajusta estos valores según tu configuración
        self.host = "localhost"
        self.user = "root"
        self.password = "1234"
        self.database = "objetosperdidos"
        self.connection = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("✅ Conexión exitosa a la base de datos.")
        except mysql.connector.Error as err:
            print(f"❌ Error al conectar: {err}")

    def cerrar_conexion(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 Conexión cerrada.")

    # --- CRUD actualizado ---
    def crear_objeto(self, nombre_objeto, descripcion, fecha_perdida, estado, id_lugar, id_usuario):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO objetos (nombre_objeto, descripcion, fecha_perdida, estado, id_lugar, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nombre_objeto, descripcion, fecha_perdida, estado, id_lugar, id_usuario))
        self.connection.commit()
        cursor.close()
        print("🆕 Objeto agregado correctamente.")


    def listar_objetos(self):
        cursor = self.connection.cursor(dictionary=True)
        query = """
            SELECT 
                o.id_objeto,
                o.nombre_objeto,
                o.descripcion,
                o.fecha_perdida,
                o.estado,
                l.nombre_lugar AS lugar,
                u.nombre AS usuario
            FROM objetos o
            LEFT JOIN lugares l ON o.id_lugar = l.id_lugar
            LEFT JOIN usuarios u ON o.id_usuario = u.id_usuario
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados


    def actualizar_objeto(self, id_objeto, nuevo_nombre, nueva_descripcion, nueva_fecha, nuevo_estado, nuevo_id_lugar, nuevo_id_usuario):
        cursor = self.connection.cursor()
        query = """
            UPDATE objetos 
            SET nombre_objeto = %s, descripcion = %s, fecha_perdida = %s, estado = %s, id_lugar = %s, id_usuario = %s
            WHERE id_objeto = %s
        """
        cursor.execute(query, (nuevo_nombre, nueva_descripcion, nueva_fecha, nuevo_estado, nuevo_id_lugar, nuevo_id_usuario, id_objeto))
        self.connection.commit()
        cursor.close()
        print("✏️ Objeto actualizado correctamente.")


    def eliminar_objeto(self, id_objeto):
        cursor = self.connection.cursor()
        query = "DELETE FROM objetos WHERE id_objeto = %s"
        cursor.execute(query, (id_objeto,))
        self.connection.commit()
        cursor.close()
        print("🗑️ Objeto eliminado correctamente.")
