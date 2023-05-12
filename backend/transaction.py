#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Transaction(db.Model):
    __tablename__ = 'transaction'

    transaction_id = db.Column(db.Integer, primary_key=True)
    washer_id = db.Column(db.String(32), nullable=False)
    packaging_type = db.Column(db.String(15), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def json(self):
        dto = {
            'transaction_id': self.transaction_id,
            'washer_id': self.washer_id,
            'packaging_type': self.packaging_type,
            'quantity': self.quantity,
            'created': self.created
        }

        return dto


@app.route("/transaction")
def get_all():
    transactionlist = Transaction.query.all()
    if len(transactionlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no washing vendor transactions."
        }
    ), 404


@app.route("/transaction/<string:transaction_id>")
def find_by_transaction_id(transaction_id):
    transaction = Transaction.query.filter_by(
        transaction_id=transaction_id).first()
    if transaction:
        return jsonify(
            {
                "code": 200,
                "data": transaction.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "transaction_id": transaction_id
            },
            "message": "Transaction not found."
        }
    ), 404


@app.route("/transaction", methods=['POST'])
def create_transaction():
    washer_id = request.json.get('washer_id', None)
    packaging_type = request.json.get('packaging_type', None)
    quantity = request.json.get('quantity', None)

    transaction = Transaction(
        washer_id=washer_id, packaging_type=packaging_type, quantity=quantity)

    try:
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the transaction. " + str(e)
            }
        ), 500

    # convert a JSON object to a string and print
    print(json.dumps(transaction.json(), default=str))
    print()

    return jsonify(
        {
            "code": 201,
            "data": transaction.json()
        }
    ), 201


@app.route("/transaction/washer/<string:washer_id>")
def find_by_washer_id(washer_id):
    transactionlist = Transaction.query.filter(
        Transaction.washer_id == washer_id).all()

    if transactionlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "washer_id": washer_id
            },
            "message": "Transaction not found."
        }
    ), 404


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) +
          ": manage transactions ...")
    app.run(host='0.0.0.0', port=5005, debug=True)
