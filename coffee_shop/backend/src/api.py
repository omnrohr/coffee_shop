"""
This file is to handle the route, users and registration with AUTH.
written partially by Obda Al Ahdab
project number 3 in NANO degree for Udacity.
"""
# --------------------------------------------------------------------------------------#
# Import dependencies.
# --------------------------------------------------------------------------------------#

import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# --------------------------------------------------------------------------------------#
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this funciton will add one
# --------------------------------------------------------------------------------------#

# db_drop_and_create_all()


# --------------------------------------------------------------------------------------#
# Implement endpoint GET /drinks.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200


# --------------------------------------------------------------------------------------#
# Implement endpoint GET /drinks-detail.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


# --------------------------------------------------------------------------------------#
# Implement endpoint POST /drinks.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    req = request.get_json()

    try:
        req_recipe = req['recipe']
        if isinstance(req_recipe, dict):
            req_recipe = [req_recipe]

        drink = Drink()
        drink.title = req['title']
        drink.recipe = json.dumps(req_recipe)
        drink.insert()

    except BaseException:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]})


# --------------------------------------------------------------------------------------#
# Implement endpoint PATCH /drinks/<id>.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    req = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        req_title = req.get('title')
        req_recipe = req.get('recipe')
        if req_title:
            drink.title = req_title

        if req_recipe:
            drink.recipe = json.dumps(req['recipe'])

        drink.update()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'drinks': [drink.long()]}), 200


# --------------------------------------------------------------------------------------#
# Implement endpoint DELETE /drinks/<id>.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'delete': id}), 200


# --------------------------------------------------------------------------------------#
# Implement error handling.
#   Error (422) Un processable
# --------------------------------------------------------------------------------------#


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

# --------------------------------------------------------------------------------------#
# Implement error handling.
#   Error (404) Resuource not found
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


# --------------------------------------------------------------------------------------#
# Implement error handling.
#   Error (401) Unauthorized.
#   NOTE it is TODO item.
# --------------------------------------------------------------------------------------#


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized."
    }), 401

# --------------------------------------------------------------------------------------#
#           The END of CODE.
# --------------------------------------------------------------------------------------#
