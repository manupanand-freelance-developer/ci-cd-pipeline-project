"""
Controller for routes
"""
from flask import jsonify, url_for, abort, request
from service import app
from service.common import status
import re
import threading
import logging

COUNTER = {}
counter_lock = threading.Lock()

# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), status.HTTP_404_NOT_FOUND

@app.errorhandler(409)
def conflict_error(error):
    return jsonify({"error": "Conflict error: Counter already exists"}), status.HTTP_409_CONFLICT

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), status.HTTP_500_INTERNAL_SERVER_ERROR

# Helper functions
def counter_exists(name):
    """Helper to check if a counter exists"""
    if name not in COUNTER:
        return abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    return True

def validate_name(name):
    """Validates counter name (alphanumeric and between 3-20 characters)"""
    if not re.match(r'^[a-zA-Z0-9]{3,20}$', name):
        abort(status.HTTP_400_BAD_REQUEST, f"Invalid counter name: {name}")

############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# Index page
############################################################
@app.route("/")
def index():
    """Returns information about the service"""
    app.logger.info("Request for Base URL, User-Agent: %s", request.headers.get('User-Agent'))
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters"""
    app.logger.info("Request to list all counters...")

    counters = [dict(name=count[0], counter=count[1]) for count in COUNTER.items()]

    return jsonify(counters)


############################################################
# Create counters
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a new counter"""
    app.logger.info("Request to Create counter: %s...", name)
    validate_name(name)

    with counter_lock:
        if COUNTER.get(name) is not None:
            return abort(status.HTTP_409_CONFLICT, f"Counter {name} already exists")

        COUNTER[name] = 0

    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a single counter"""
    app.logger.info("Request to Read counter: %s...", name)
    counter_exists(name)

    counter = COUNTER[name]
    return jsonify(name=name, counter=counter)


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Updates a counter"""
    app.logger.info("Request to Update counter: %s...", name)
    counter_exists(name)

    with counter_lock:
        COUNTER[name] += 1

    counter = COUNTER[name]
    return jsonify(name=name, counter=counter)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Deletes a counter"""
    app.logger.info("Request to Delete counter: %s...", name)

    with counter_lock:
        if name in COUNTER:
            COUNTER.pop(name)

    return "", status.HTTP_204_NO_CONTENT


############################################################
# Utility for testing
############################################################
def reset_counters():
    """Removes all counters while testing"""
    global COUNTER  # pylint: disable=global-statement
    if app.testing:
        COUNTER = {}
