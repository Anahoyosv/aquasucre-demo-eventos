from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

#BUS DE EVENTOS
#___________________________________

def publicar_evento(nombre_evento, data):
    print (f"\n Evento publicado: {nombre_evento}")

    if nombre_evento == "Factura_vencida":
        notificar_cliente(data)
        registrar_evento(data)
        log_evento(data)

#REACCIOES DE LOS CONSUMIDORES
def notificar_cliente(data):
    print(f"Notificando cliente {data['cliente_id']} - factura vencida ({data['dias_mora']} dias)")


def registrar_evento(data):
    print(f"Registrando en la base de datos del sistema: cliente {data['cliente_id']} con mora")


def log_evento(data):
    print(f" LOG: Evento procesado correctamente")


#RUTA BASE 
#___________________

@app.route("/")
def home():
    return "API AquaSucre funcionando..."


#ENDPOINT PRINCIPAL 
#_____________________

@app.route("/facturas", methodos=["POST"])

def crear_factura():
    data = request.get_json()

    cliente_id = data.get("cliente_id")
    valor = data.get("valor")
    fecha_vencimiento = data.get("fecha_vencimiento")

    #Validacion basica de formato Json
    if not cliente_id or not valor or not fecha_vencimiento:
        return jsonify({"error": "Datos incompletos"}), 400
    
    try:
        fecha_venc = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
    except ValueError:
      return jsonify({"error": "Formato de fecha inválido, utiliza YYY-mm-DD"}), 400  
    
    hoy = datetime.now()

    print(f"\n Factura recibida para cliente {cliente_id}")

    #LÓGICA DE NEGOCIO
    #_____________________________

    if hoy > fecha_venc:
        dias_mora = (hoy - fecha_venc).days

        #Configuramos evento una vez se valide que la factura vencio
        evento = {
            "cliente_id": cliente_id,
            "valor": valor,
            "dias_mora": dias_mora,
            "timestamp": datetime.now().isoformat()
        }

        publicar_evento("factura_vencida", evento)

        return jsonify({
            "mensaje": "Factura vencida detectada", 
            "evento": "factura_vencida", 
            "dias_mora": dias_mora
        })
    
    else: 
        return jsonify({
            "mensaje": "Factura registrada SIN mora"
        })
    
#EJECUCIÓN PARA RENDER
#____________________________-

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 




