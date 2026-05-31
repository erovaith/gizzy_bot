from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "🚀 GIZZY BOT SYSTEM: ACTIVE 7/24"

@app.route('/status')
def status():
    return {"status": "running", "uptime": "100%", "version": "2.5.0"}

def run_server():
    # Sunucuyu dış dünyaya açıyoruz (Port 8080)
    app.run(host='0.0.0.0', port=8080)

def start_uptime_server():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()