from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

PORT = int(os.getenv("PORT", 3000))
DATABASE_URL = os.getenv("DATABASE_URL")

# Conexión a PostgreSQL
try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Conexión a PostgreSQL exitosa")
except Exception as e:
    print("❌ Error al conectar a PostgreSQL:", e)
    conn = None

@app.route("/")
def home():
    return render_template("index.html")  # Sirve tu HTML

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # ⚠️ Este ejemplo solo imprime. NO es seguro almacenar contraseñas así.
    print(f"📥 Usuario: {username}, Contraseña: {password}")
    return "", 200

@app.route("/test-db")
def test_db():
    if conn is None:
        return jsonify({"error": "No hay conexión a la base de datos"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        return jsonify({"PostgreSQL version": version})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
