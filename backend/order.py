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


class Orders(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    hawker_id = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'order_id': self.order_id,
            'hawker_id': self.hawker_id,
            'status': self.status,
            'created': self.created,
            'modified': self.modified
        }

        dto['order_item'] = []
        for oi in self.order_item:
            dto['order_item'].append(oi.json())

        return dto


class Order_Item(db.Model):
    __tablename__ = 'order_item'

    item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.ForeignKey(
        'orders.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    packaging_type = db.Column(db.String(15), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    orders = db.relationship(
        'Orders', primaryjoin='Order_Item.order_id == Orders.order_id', backref='order_item')

    def json(self):
        return {'item_id': self.item_id, 'packaging_type': self.packaging_type, 'quantity': self.quantity, 'order_id': self.order_id}


@app.route("/orders")
def get_all():
    orderlist = Orders.query.all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404


@app.route("/orders/<string:order_id>")
def find_by_order_id(order_id):
    order = Orders.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404


@app.route("/orders", methods=['POST'])
def create_order():
    hawker_id = request.json.get('hawker_id', None)
    order = Orders(hawker_id=hawker_id, status='NEW')

    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            packaging_type=item['packaging_type'], quantity=item['quantity']))

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    # convert a JSON object to a string and print
    print(json.dumps(order.json(), default=str))
    print()

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201


@app.route("/orders/<string:order_id>", methods=['PUT'])
def update_order(order_id):
    try:
        order = Orders.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "order_id": order_id
                    },
                    "message": "Order not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['status']:
            order.status = data['status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": order.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while updating the order. " + str(e)
            }
        ), 500


@app.route("/orders/hawker/<string:hawker_id>")
def find_by_hawker_id(hawker_id):
    orderlist = Orders.query.filter(Orders.hawker_id == hawker_id).all()
    if orderlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "hawker_id": hawker_id
            },
            "message": "Order not found."
        }
    ), 404


@app.route("/orders/hawker/new/<string:hawker_id>")
def find_by_hawker_id_new_orders(hawker_id):
    orderlist = Orders.query.filter((Orders.hawker_id == hawker_id) & (Orders.status == "NEW")).all()
    if orderlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "hawker_id": hawker_id
            },
            "message": "Order not found."
        }
    ), 404


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5003, debug=True)
