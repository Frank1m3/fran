from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # 👈 Esto carga automáticamente las variables desde tu archivo .env

app = Flask(__name__)
PORT = int(os.getenv("PORT", 3000))

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Conexión a PostgreSQL exitosa")
except Exception as e:
    print("❌ Error al conectar a PostgreSQL:", e)
    conn = None

@app.route("/")
def home():
    return "Servidor Flask funcionando correctamente"

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
