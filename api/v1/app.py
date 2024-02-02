#!/usr/bin/python3
"""
A script that runs Flask with REST Api for AIRBNB clone
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors by returning a JSON-formatted response."""
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    """
    Run Flask app with environment variable or default value
    """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
