import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink, Ingredient, Property
from auth.auth import requires_auth
from logger import Logger

logger = Logger.get_logger(__name__)


def create_app(test=False):
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')

    # Set up database
    if not test:
        setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.route('/', methods=['GET']
              )(lambda: jsonify({'message': 'Hello end-user!'}))

    @app.after_request
    def after_request(response):
        """Use the after_request decorator to set Access-Control-Allow"""
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/drinks', methods=['GET'])
    @requires_auth(permission='get:drinks')
    def get_drinks(payload=None):
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
    def get_drinks_detail(payload=None):
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

    @app.route('/drinks/<int:id>', methods=['GET'])
    @requires_auth(permission='get:drinks-detail')
    def get_drink(payload, id):
        """Get a drink.

        Args:
            payload (dict): Payload from Auth0.
            id (int): Drink ID.

        Returns:
            dict: A dictionary with success status and drink.

        Raises:
            AuthError 404: If the drink is not found.
        """
        logger.info(f'Request route /drinks/{id}: Get a drink')
        drink_row = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink_row:
            logger.info('Response: 404')
            abort(code=404)
        logger.info(f'Response: {drink_row.long()}')
        return jsonify({
            'success': True,
            'drinks': [drink_row.long()]
        }), 200

    @app.route('/drinks', methods=['POST'])
    @requires_auth(permission='post:drinks')
    def post_drink(payload=None):
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

    @app.route('/ingredients', methods=['GET'])
    @requires_auth(permission='get:ingredients')
    def get_ingredients(payload=None):
        """Get all ingredients.

        Returns:
            dict: A dictionary with success status and ingredients list.
        """
        logger.info('Request route /ingredients: Get all ingredients')
        ingredients_row_list = [ingredient.format()
                                for ingredient in Ingredient.query.all()]
        logger.info(f'Response: {ingredients_row_list}')
        return jsonify({
            'success': True,
            'ingredients': ingredients_row_list
        }), 200

    @app.route('/ingredients', methods=['POST'])
    @requires_auth(permission='post:ingredients')
    def post_ingredient(payload=None):
        """Create a new ingredient.

        Args:
            payload (dict): Payload from Auth0.

        Returns:
            dict: A dictionary with success status and ingredient.
        """
        logger.info('Request route /ingredients: Create a new ingredient')
        body = request.get_json()
        name = body.get('name', None)
        density = body.get('density', None)
        if not name:
            logger.info('Response: 403')
            abort(code=403)
        ingredient = Ingredient(name=name, density=density)
        ingredient.insert()
        logger.info(f'Response: {ingredient}')
        return jsonify({
            'success': True,
            'ingredients': ingredient.format()
        }), 200

    @app.route('/ingredients/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:ingredients')
    def patch_ingredient(payload, id):
        """Update an ingredient.

        Args:
            payload (dict): Payload from Auth0.
            id (int): Ingredient ID.

        Returns:
            dict: A dictionary with success status and ingredient.

        Raises:
            AuthError 404: If the ingredient is not found.
            AuthError 400: If name is not provided.
        """
        logger.info(f'Request route /ingredients/{id}: Update an ingredient')
        ingredient_row = Ingredient.query.filter(
            Ingredient.id == id).one_or_none()
        if not ingredient_row:
            logger.info('Response: 404')
            abort(code=404)
        body = request.get_json()
        name = body.get('name', None)
        logger.info(f'Request body: {body}')
        if not name:
            logger.info('Response: 400')
            abort(code=400)
        ingredient_row.name = name
        ingredient_row.update()
        logger.info(f'Response: {ingredient_row}')
        return jsonify({
            'success': True,
            'ingredients': ingredient_row.format()
        }), 200

    @app.route('/ingredients/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:ingredients')
    def delete_ingredient(payload, id):
        """Delete an ingredient.

        Args:
            payload (dict): Payload from Auth0.
            id (int): Ingredient ID.

        Returns:
            dict: A dictionary with success status and deleted ingredient ID.
        """
        logger.info(f'Request route /ingredients/{id}: Delete an ingredient')
        ingredient_row = Ingredient.query.filter(
            Ingredient.id == id).one_or_none()
        if not ingredient_row:
            logger.info('Response: 404')
            abort(code=404)
        ingredient_row.delete()
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

    return app


app = create_app()
with app.app_context():
    db_drop_and_create_all()


if __name__ == '__main__':
    app.run(debug=True)
