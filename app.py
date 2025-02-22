from flask import Flask, render_template, request, jsonify
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyodbc
import pywhatkit

app = Flask(__name__)

# Configurar el motor de voz
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Configurar Wikipedia en español
wikipedia.set_lang("es")

# Conexión a la base de datos SQL Server
server = 'basesitaxd123.database.windows.net'
bd = 'DatabaseSenati'
user = 'carmenwita123'
passw = 'Holaxd123456'
conexion = None
cursor = None

try:
    conexion = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={bd};UID={user};PWD={passw}')
    cursor = conexion.cursor()
    print("✅ Conectado a la base de datos")
except Exception as e:
    print("❌ Error al conectar a SQL Server:", e)

# Función para que el asistente hable
def Decir(audio):
    engine.say(audio)
    engine.runAndWait()

@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error cargando la plantilla: {e}"

@app.route('/obtener_alumnos', methods=['GET'])
def obtener_alumnos():
    if cursor:
        try:
            cursor.execute("SELECT codalumno, nombres FROM tasistencia;")
            rows = cursor.fetchall()
            alumnos = [{"codalumno": row[0], "nombres": row[1]} for row in rows]
            return jsonify(alumnos=alumnos)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "No hay conexión a la base de datos."})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Usa el puerto asignado por Render
    app.run(host="0.0.0.0", port=port, debug=True)
