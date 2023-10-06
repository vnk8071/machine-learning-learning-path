import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from flaskr.router import question_router, category_router
from flaskr.doc import doc_router


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

    app.register_blueprint(blueprint=question_router)
    app.register_blueprint(blueprint=category_router)
    app.register_blueprint(blueprint=doc_router)
    return app
