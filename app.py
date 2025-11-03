from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from database import Database

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el front-end

db = Database()
db.conectar()

conn = db.connection # Conexión para uso directo en rutas con templates

# ---------------------------
# 🔹 RUTAS DE LA API REST
# ---------------------------
@app.route('/objetos', methods=['GET'])
def obtener_objetos():
    objetos = db.listar_objetos()
    return jsonify(objetos)

@app.route('/objetos', methods=['POST'])
def agregar_objeto():
    data = request.get_json()

    nombre_objeto = data.get('nombre_objeto')
    descripcion = data.get('descripcion')
    fecha_perdida = data.get('fecha_perdida')
    estado = data.get('estado')
    id_lugar = data.get('id_lugar')
    id_usuario = data.get('id_usuario')

    # Validar que los campos obligatorios estén presentes
    if not all([nombre_objeto, id_lugar, id_usuario]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Llamar al método crear_objeto de la base de datos
    db.crear_objeto(nombre_objeto, descripcion, fecha_perdida, estado, id_lugar, id_usuario)

    return jsonify({"mensaje": "🆕 Objeto agregado correctamente."}), 201


@app.route('/objetos/<int:id>', methods=['DELETE'])
def eliminar_objeto(id):
    resultado = db.eliminar_objeto(id)
    return jsonify(resultado)

# ---------------------------
# 🔹 RUTAS CON TEMPLATES HTML
# ---------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ver_objetos')
def ver_objetos():
    objetos = db.listar_objetos()
    return render_template('objetos.html', objetos=objetos)

@app.route("/agregar_objeto_html", methods=["GET", "POST"])
def agregar_objeto_html():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        id_lugar = request.form["id_lugar"]
        id_usuario = request.form["id_usuario"]
        fecha_perdida = request.form["fecha_perdida"]
        estado = request.form["estado"]

        cursor = conn.cursor()
        sql = """
        INSERT INTO objetos (nombre, descripcion, fecha_perdida, estado, id_lugar, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, fecha_perdida, estado, id_lugar, id_usuario))
        conn.commit()
        cursor.close()

        return redirect(url_for("ver_objetos"))
    
    return render_template("crear_objeto.html")

@app.route("/actualizar_objeto/<int:id>", methods=["GET", "POST"])
def actualizar_objeto_html(id):
    cursor = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        id_lugar = request.form["id_lugar"]
        id_usuario = request.form["id_usuario"]
        fecha_perdida = request.form["fecha_perdida"]
        estado = request.form["estado"]

        sql = """
        UPDATE objetos 
        SET nombre=%s, descripcion=%s, fecha_perdida=%s, estado=%s, id_lugar=%s, id_usuario=%s
        WHERE id=%s
        """
        cursor.execute(sql, (nombre, descripcion, fecha_perdida, estado, id_lugar, id_usuario, id))
        conn.commit()
        cursor.close()
        return redirect(url_for("ver_objetos"))

    # Si es GET → mostramos el formulario con los datos actuales
    cursor.execute("SELECT * FROM objetos WHERE id = %s", (id,))
    objeto = cursor.fetchone()
    cursor.close()

    return render_template("actualizar_objeto.html", objeto=objeto)

@app.route("/eliminar_objeto/<int:id>", methods=["GET", "POST"])
def eliminar_objeto_html(id):
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute("DELETE FROM objetos WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        return redirect(url_for("ver_objetos"))

    # Si es GET → mostramos la confirmación
    cursor.execute("SELECT * FROM objetos WHERE id = %s", (id,))
    objeto = cursor.fetchone()
    cursor.close()

    return render_template("eliminar_objeto.html", objeto=objeto)

# ---------------------------
# 🔹 EJECUCIÓN DEL SERVIDOR
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
