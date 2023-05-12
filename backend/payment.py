from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    hawker_id = db.Column(db.String(10), nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    payment_amount = db.Column(db.Float(precision=2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'payment_id': self.payment_id,
            'hawker_id': self.hawker_id,
            'order_id': self.order_id,
            'payment_amount': self.payment_amount,
            'payment_date': self.payment_date
        }
        return dto


@app.route("/payment")
def get_all():
    paymentlist = Payment.query.all()
    if len(paymentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payments": [payment.json() for payment in paymentlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments."
        }
    ), 404


@app.route("/payment/<string:payment_id>")
def find_by_payment_id(payment_id):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No payment found for that ID found."
        }
    ), 404


@app.route("/payment", methods=['POST'])
def create_payment():
    hawker_id = request.json.get('hawker_id')
    payment_amount = request.json.get('payment_amount')
    order_id = request.json.get('order_id')
    payment = Payment(hawker_id=hawker_id, order_id=order_id,
                      payment_amount=payment_amount)

    try:
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the payment." + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": payment.json()
        }
    ), 201


@app.route("/payment/hawker/<string:hawker_id>")
def find_by_hawker_id(hawker_id):
    paymentlist = Payment.query.filter(Payment.hawker_id == hawker_id).all()
    if paymentlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payments": [payment.json() for payment in paymentlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No payment found for that ID found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
