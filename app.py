from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import mysql.connector
from datetime import datetime, timedelta
import bcrypt
from itsdangerous import URLSafeTimedSerializer
import random
import string
import uuid
from flask import flash


app = Flask(__name__)
app.secret_key = "prueba"

# Configuración de la conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="work"
)


##### CREACIÓN DE LAS TABLAS AL INICIAR APP.PY ##########


# Creación de la tabla de usuarios al iniciar la aplicación
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

# Creación de la tabla de tareas al iniciar la aplicación

cursor.execute("""
               
    CREATE TABLE IF NOT EXISTS tareas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        work_name VARCHAR(255) NOT NULL,
        registration_date DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
db.commit()


    ##### HASTA AQUÍ LA CREACIÓN DE LAS TABLAS AL INICIAR APP.PY ##########

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Definición de la clase User para Flask-Login
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
        # Obtener los datos del usuario desde la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0])
        return None

@login_manager.user_loader
def load_user(user_id):
    # Cargar el usuario a partir de su ID almacenado en la sesión
    return User.get(user_id)


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    else:
        return redirect(url_for("login"))
    
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Realizar consulta a la base de datos para obtener el hash de la contraseña del usuario
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            # Verificar el hash de la contraseña almacenada con la contraseña proporcionada
            if bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
                # Contraseña válida, iniciar sesión y redirigir al perfil
                user_obj = User(user[0])
                login_user(user_obj)
                return redirect(url_for("inicio"))

        # Si el usuario no existe o las credenciales son incorrectas, mostrar mensaje de error
        error_message = "Datos incorrectos, hazlo nuevamente o registrate si no tienes cuenta."
        return render_template("login.html", error_message=error_message)

    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Verificar si el usuario ya está registrado en la base de datos
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # El usuario ya está registrado, mostrar mensaje de alerta
            flash("El usuario ya está registrado, inicia sección.", "warning")
            return render_template("register.html")

        # Generar el hash y salting de la contraseña
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Obtener la fecha y hora actual
        current_date = datetime.now()

        # Insertar los datos del nuevo usuario y el hash de la contraseña en la base de datos
        cursor.execute("INSERT INTO users (email, password, registration_date) VALUES (%s, %s, %s)", (email, password_hash, current_date))
        db.commit()

        # Mostrar mensaje de éxito
        flash("Usuario registrado exitosamente, inicia sección.", "success")
        return render_template("register.html")

    return render_template("register.html")


# Esto aquí es para que el usuario no haga trampa en el login e inicio
@app.after_request
def add_cache_control(response):
    # Agregar encabezados de respuesta para evitar el almacenamiento en caché
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/inicio")
@login_required
def inicio():
    # Verificar si hay un usuario autenticado en la sesión
    user_id = current_user.id

    # Consultar los datos del usuario desde la base de datos
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if user:
        # Si el usuario existe, mostrar la página de perfil con los datos del usuario
        return render_template("index.html", user=user)

    # Si no hay un usuario autenticado en la sesión, redirigir al inicio de sesión
    return redirect(url_for("login"))



# Este es el resto de las rutas y sus funciones ...

@app.route("/logout")
@login_required
def logout():
    # Cerrar sesión y redirigir al inicio de sesión
    logout_user()
    response = make_response(redirect(url_for("login")))
    response.delete_cookie("")  # Cookie a eliminar
    return response



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)