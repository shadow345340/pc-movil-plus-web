from flask import Flask, render_template, request
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enviar_correo', methods=['POST'])
def enviar():
    datos = request.form
    msg = EmailMessage()
    msg.set_content(f"NUEVO TRABAJO:\n\nNombre: {datos['nombre']}\nContacto: {datos['contacto']}\nEquipo: {datos['equipo']}\nFalla: {datos['falla']}")
    
    msg['Subject'] = f"🛠️ Nuevo Equipo: {datos['equipo']}"
    msg['From'] = os.getenv("GMAIL_USER")
    msg['To'] = os.getenv("GMAIL_USER")

    try:
        # Usamos SSL y puerto 465 (el más seguro para evitar bloqueos)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
            smtp.send_message(msg)
        return "<h1>✅ Enviado. ¡Dile a tu abuelo que revise su correo!</h1>"
    except Exception as e:
        return f"<h1>❌ Error: {e}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
