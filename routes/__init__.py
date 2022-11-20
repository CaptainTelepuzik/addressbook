from flask import request
from classes.EndpointFactory import EndpointFactory

from app import app


@app.route('/service', methods=['POST'])
def main_route():
    request_data = request.get_json() or {}
    return EndpointFactory(request_data).process()