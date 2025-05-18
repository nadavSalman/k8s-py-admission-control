from flask import Flask, request, jsonify, Response
import sys
import logging
from pprint import pformat
import base64
import json

from admission_webhook.mutating_webhook.resource_requests_limiter import resource_requests_limiter_bp
from admission_webhook.logging_config.logging_config import configure_logging


app = Flask(__name__)

# Configure logging to stdout
# Configure logging
logger = configure_logging()


# Register blueprints with a prefix
app.register_blueprint(resource_requests_limiter_bp, url_prefix='/mutating')

@app.route('/endpoints', methods=['GET'])
def list_endpoints():
    app.logger.info('Received request at /endpoints endpoint')
    endpoints = [rule.rule for rule in app.url_map.iter_rules()]
    app.logger.debug('Available endpoints: %s', pformat(endpoints))
    return jsonify(endpoints)

if __name__ == '__main__':
    app.run()
    app.logger.info('Starting admission webhook server')