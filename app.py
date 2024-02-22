from flask import Flask, render_template, request, redirect, url_for, session, make_response, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import mysql.connector
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.secret_key = "prueba"

# Configuración de la conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="work"
)

# CREACIÓN DE LAS TABLAS AL INICIAR APP.PY
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        registration_date DATETIME NOT NULL
    )
""")
db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        work_name VARCHAR(255) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'pendiente',
        registration_date DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
db.commit()

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Clase User para Flask-Login
class User:
    def __init__(self, user_id):
        self.id = user_id
        self.is_active = True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    @staticmethod
    def get(user_id):
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Ruta de inicio
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    else:
        return redirect(url_for("login"))

# Ruta de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
            user_obj = User(user[0])
            login_user(user_obj)
            return redirect(url_for("inicio"))

        error_message = "Datos incorrectos, hazlo nuevamente o registrate si no tienes cuenta."
        return render_template("login.html", error_message=error_message)

    return render_template("login.html")

# Ruta de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("El usuario ya está registrado, inicia sesión.", "warning")
            return render_template("register.html")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        current_date = datetime.now()
        cursor.execute("INSERT INTO users (email, password, registration_date) VALUES (%s, %s, %s)", (email, password_hash, current_date))
        db.commit()
        flash("Usuario registrado exitosamente, inicia sesión.", "success")
        return render_template("register.html")

    return render_template("register.html")

# Configuración para evitar almacenamiento en caché
@app.after_request
def add_cache_control(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Ruta de inicio de la sesión
@app.route("/inicio")
@login_required
def inicio():
    user_id = current_user.id
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if user:
        query = "SELECT * FROM tareas WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        tasks = cursor.fetchall()
        return render_template("index.html", user=user, tasks=tasks)

    return redirect(url_for("login"))

# Ruta para agregar una tarea
@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        user_id = current_user.id
        registration_date = datetime.now()

        cursor = db.cursor()
        query = "INSERT INTO tareas (user_id, work_name, registration_date) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, task, registration_date))
        db.commit()
        cursor.close()

        flash('Tarea agregada correctamente', 'success')
        return redirect(url_for('inicio'))

# Ruta para eliminar una tarea
@app.route('/delete_task/<int:task_id>', methods=['GET'])
@login_required
def delete_task(task_id):
    cursor = db.cursor()
    query = "DELETE FROM tareas WHERE id = %s AND user_id = %s"
    cursor.execute(query, (task_id, current_user.id))
    db.commit()
    cursor.close()

    flash('Tarea eliminada correctamente', 'success')
    return redirect(url_for('inicio'))

# Ruta para editar una tarea
@app.route('/edit_task/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    if request.method == 'POST':
        new_task = request.form['task']
        new_status = request.form['status']  # Obtener el nuevo estado desde el formulario

        cursor = db.cursor()
        query = "UPDATE tareas SET work_name = %s, status = %s WHERE id = %s AND user_id = %s"
        cursor.execute(query, (new_task, new_status, task_id, current_user.id))
        db.commit()
        cursor.close()

        flash('Tarea actualizada correctamente', 'success')
        return redirect(url_for('inicio'))



# Ruta de cierre de sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for("login")))
    response.delete_cookie("")  
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
