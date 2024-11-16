from flask import Flask, request, jsonify
from flask_cors import CORS
from endpoints import domain
from whiskey import SimpleMiddleware
from public_endpoints import domain as domik

app = Flask(__name__)
CORS(app)  # Дозволити CORS для всього додатку

# Uncomment for prod
app.wsgi_app = SimpleMiddleware(app.wsgi_app)

app.register_blueprint(domain, url_prefix="/api")
app.register_blueprint(domik, url_prefix="/public")

if __name__ == "__main__":
    app.run(debug=True)
