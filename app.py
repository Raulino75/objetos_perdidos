from flask import Flask, abort, jsonify, request, render_template, redirect, url_for
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

    nombre_objeto = data.get('nombre')
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

@app.route('/index')
def index():
    return redirect(url_for('home'))


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
        INSERT INTO objetos (nombre_objeto, descripcion, fecha_perdida, estado, id_lugar, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, fecha_perdida, estado, id_lugar, id_usuario))
        conn.commit()
        cursor.close()

        return redirect(url_for("ver_objetos"))
    
    return render_template("crear_objeto.html")

# Mostrar todos los objetos con opción de actualizar
@app.route("/actualizar_objeto", methods=["GET"])
def actualizar_objeto_html():
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id_objeto, nombre_objeto, descripcion FROM objetos")
    objetos = cur.fetchall()
    cur.close()

    print("DEBUG → objetos:", objetos)  # 👈 añade esta línea

    return render_template("actualizar_objeto.html", objetos=objetos)



@app.route("/editar_objeto/<int:id>", methods=["GET", "POST"])
def editar_objeto(id):
    cur = conn.cursor(dictionary=True)

    if request.method == "POST":
        # Obtén todos los campos dinámicamente
        campos = request.form.to_dict()

        # Genera la parte del SQL automáticamente
        set_clause = ", ".join([f"{campo} = %s" for campo in campos.keys()])
        valores = list(campos.values()) + [id]

        cur.execute(f"UPDATE objetos SET {set_clause} WHERE id_objeto = %s", valores)
        conn.commit()
        cur.close()

        return redirect(url_for("actualizar_objeto_html"))

    cur.execute("SELECT * FROM objetos WHERE id_objeto = %s", (id,))
    objeto = cur.fetchone()
    cur.close()
    return render_template("editar_objeto.html", objeto=objeto)



@app.route("/eliminar_objeto", methods=["GET", "POST"])
@app.route("/eliminar_objeto/<int:id>", methods=["GET", "POST"])
def eliminar_objeto_html(id=None):
    cursor = conn.cursor()

    if request.method == "POST" and id is not None:
        cursor.execute("DELETE FROM objetos WHERE id_objeto = %s", (id,))
        conn.commit()
        cursor.close()
        return redirect(url_for("eliminar_objeto_html"))  # volver a la misma página

    cursor.execute("SELECT id_objeto, nombre_objeto, descripcion FROM objetos")
    objetos = cursor.fetchall()
    cursor.close()

    return render_template("eliminar_objeto.html", objetos=objetos)

# ---------------------------
# 🔹 RUTAS DE USUARIOS
# ---------------------------

@app.route('/usuarios')
def ver_usuarios():
    usuarios = db.listar_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        db.crear_usuario(nombre, correo, telefono)
        return redirect(url_for('ver_usuarios'))
    
    return render_template('agregar_usuario.html')




# ---------------------------
# 🔹 EJECUCIÓN DEL SERVIDOR
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
