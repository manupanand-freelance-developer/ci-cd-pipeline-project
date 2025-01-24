"""
Module: error_handlers
"""
from flask import jsonify
from service import app
from . import status

# General Error Handler
def handle_error(error, status_code, error_message):
    """Handles all error types"""
    app.logger.warning(f"{error_message}: {str(error)}")
    return jsonify(
        status=status_code, error=error_message, message=str(error)
    ), status_code

# Error Handlers for Specific HTTP Status Codes
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """Handles bad requests (400)"""
    return handle_error(error, status.HTTP_400_BAD_REQUEST, "Bad Request")

@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles not found errors (404)"""
    return handle_error(error, status.HTTP_404_NOT_FOUND, "Not Found")

@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """Handles method not allowed errors (405)"""
    return handle_error(error, status.HTTP_405_METHOD_NOT_ALLOWED, "Method Not Allowed")

@app.errorhandler(status.HTTP_409_CONFLICT)
def resource_conflict(error):
    """Handles conflict errors (409)"""
    return handle_error(error, status.HTTP_409_CONFLICT, "Conflict")

@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """Handles unsupported media type errors (415)"""
    return handle_error(error, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported Media Type")

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Handles internal server errors (500)"""
    app.logger.error(f"Internal Server Error: {str(error)}")
    return handle_error(error, status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error")
