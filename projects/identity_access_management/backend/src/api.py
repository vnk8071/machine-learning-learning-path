import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from .logger import Logger


app = Flask(__name__)
setup_db(app=app)
CORS(app=app)
logger = Logger.get_logger(__name__)


with app.app_context():
    db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def get_drinks():
    """Get all drinks.

    Returns:
        dict: A dictionary with success status and drinks list.
    """
    logger.info('Request route /drinks: Get all drinks')
    drinks_row_list = [drink.short() for drink in Drink.query.all()]
    logger.info(f'Response: {drinks_row_list}')
    return jsonify({
        'success': True,
        'drinks': drinks_row_list
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(payload):
    """Get all drinks detail.

    Args:
        payload (dict): Payload from Auth0.

    Returns:
        dict: A dictionary with success status and drinks list.
    """
    logger.info('Request route /drinks-detail: Get all drinks detail')
    drinks_row_list = [drink.long() for drink in Drink.query.all()]
    logger.info(f'Response: {drinks_row_list}')
    return jsonify({
        'success': True,
        'drinks': drinks_row_list
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def post_drink(payload):
    """Create a new drink.

    Args:
        payload (dict): Payload from Auth0.

    Returns:
        dict: A dictionary with success status and drink.
    """
    logger.info('Request route /drinks: Create a new drink')
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    if not title and not recipe:
        logger.info('Response: 403')
        abort(code=403)
    drink = Drink(title=title, recipe=json.dumps(recipe))
    drink.insert()
    logger.info(f'Response: {drink.long()}')
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def patch_drink(payload, id):
    """Update a drink.

    Args:
        payload (dict): Payload from Auth0.
        id (int): Drink ID.

    Returns:
        dict: A dictionary with success status and drink.

    Raises:
        AuthError 404: If the drink is not found.
        AuthError 400: If title or recipe is not provided.
    """
    logger.info(f'Request route /drinks/{id}: Update a drink')
    drink_row = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink_row:
        logger.info('Response: 404')
        abort(code=404)
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)
    logger.info(f'Request body: {body}')
    if not title and not recipe:
        logger.info('Response: 400')
        abort(code=400)
    drink_row.title = title
    drink_row.recipe = json.dumps(recipe)
    drink_row.update()
    logger.info(f'Response: {drink_row.long()}')
    return jsonify({
        'success': True,
        'drinks': [drink_row.long()]
    }), 200


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(payload, id):
    """Delete a drink.

    Args:
        payload (dict): Payload from Auth0.
        id (int): Drink ID.

    Returns:
        dict: A dictionary with success status and deleted drink ID.
    """
    logger.info(f'Request route /drinks/{id}: Delete a drink')
    drink_row = Drink.query.filter(Drink.id == id).one_or_none()
    if not drink_row:
        logger.info('Response: 404')
        abort(code=404)
    drink_row.delete()
    logger.info(f'Response: {id}')
    return jsonify({
        'success': True,
        'delete': id
    }), 200


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400
