#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Inventory(db.Model):
    __tablename__ = 'inventory'

    type = db.Column(db.String(15), primary_key=True)
    stripe_id = db.Column(db.String(30), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    loaned = db.Column(db.Integer, nullable=False)

    def json(self):
        dto = {
            'type': self.type,
            'stripe_id': self.stripe_id,
            'available': self.available,
            'loaned': self.loaned
        }

        return dto


@app.route("/inventory")
def get_all():
    inventorylist = Inventory.query.all()
    if len(inventorylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [inventory.json() for inventory in inventorylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no inventory."
        }
    ), 404


@app.route("/inventory/<string:type>")
def find_by_type(type):
    inventory = Inventory.query.filter_by(type=type).first()
    if inventory:
        return jsonify(
            {
                "code": 200,
                "data": inventory.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "type": type
            },
            "message": "Inventory not found."
        }
    ), 404


@app.route("/inventory/return/<string:type>", methods=['PUT'])
def update_inventory(type):
    try:
        inventory = Inventory.query.filter_by(type=type).first()
        if not inventory:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "inventory": inventory
                    },
                    "message": "inventory not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['quantity']:
            quantity_return = data['quantity']

            if quantity_return > int(inventory.loaned):
                return jsonify(
                    {
                        "code": 406,
                        "quantity": quantity_return,
                        "data": inventory.json(),
                        "message": "Quantity to be returned is more than the loaned quantity."
                    }
                ), 406

            available = int(inventory.available) + int(quantity_return)
            loaned = int(inventory.loaned) - int(quantity_return)
            inventory.available = available
            inventory.loaned = loaned
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": inventory.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "type": type
                },
                "message": "An error occurred while updating the inventory. " + str(e)
            }
        ), 500


@app.route("/inventory/loan/<string:type>", methods=['PUT'])
def loan_inventory(type):
    try:
        inventory = Inventory.query.filter_by(type=type).first()
        if not inventory:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "inventory": inventory
                    },
                    "message": "inventory not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['quantity']:
            quantity_loan = data['quantity']

            if quantity_loan > int(inventory.available):
                return jsonify(
                    {
                        "code": 406,
                        "quantity": quantity_loan,
                        "data": inventory.json(),
                        "message": "Quantity to be returned is more than the loaned quantity."
                    }
                ), 406

            available = int(inventory.available) - int(quantity_loan)
            loaned = int(inventory.loaned) + int(quantity_loan)
            inventory.available = available
            inventory.loaned = loaned
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": inventory.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "type": type
                },
                "message": "An error occurred while updating the inventory. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": inventory ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
