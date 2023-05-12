from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

from invokes import invoke_http

import amqp_setup
import json
import copy

app = Flask(__name__)
CORS(app)

stripe_URL = environ.get('stripe_URL') or "http://localhost:5002/create_checkout_session"
order_URL = environ.get('order_URL') or "http://localhost:5003/orders"
payment_URL = environ.get('payment_URL') or "http://localhost:5004/payment"


@app.route("/hawker_payment", methods=['POST'])
def hawker_payment():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            payment = request.get_json()
            print("\nReceived an payment in JSON:", payment)

            # do the actual work
            # 1. Send payment info
            result = processPlacePayment(payment)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "hawker_payment.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processPlacePayment(payment):
    # 2. Get all orders not paid yet
    # Invoke the orders microservice
    print('\n-----Invoking orders microservice-----')
    orders1_result = invoke_http(order_URL + "/hawker/new/" + payment["hawker_id"], method='GET', json=payment)

    code = orders1_result["code"]
    if code not in range(200, 300):

        print("Update inventory failed")

        # 3. Return error
        return {
            "code": 404,
            "data": {"orders1_result": orders1_result},
            "message": "Inventory not found."
        }

    print('orders1_result:', orders1_result)

    # 3. Update each of the others to be paid
    # Invoke the orders microservice
    print('\n-----Invoking orders microservice-----')
    ordersList = orders1_result["data"]["orders"]
    orders2_result = []
    body = {
        "status": "PAID"
    }
    for order in ordersList:
        order_id = order["order_id"]
        orders_sub_result = invoke_http(order_URL + "/" + str(order_id), method='PUT', json=body)
        orders2_result.append(orders_sub_result)
    print('orders2_result', orders2_result)

    # 4. Send Payment info for payment log
    print('\n\n-----Publishing the (Payment info) message with routing_key=transaction-----')
    for order in ordersList:
        order_id = order["order_id"]
        message = json.dumps({
            "hawker_id": payment["hawker_id"],
            "order_id": order_id,
            "payment_amount": 10
        })
        print(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="payment",
                                         body=message)

    # 4. Send payment info for notification
    print('\n\n-----Publishing the (Pyment info) message with routing_key=notification-----')
    orders_message = []
    for order in ordersList:
        print(order)
        order_id = str(order["order_id"])
        orders_message.append(order_id)
    orders_message = ", ".join(orders_message)
    message = json.dumps({
        "hawker_id": payment["hawker_id"],
        "orders": orders_message,
        "notification_type": "payment"
    })
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification",
                                     body=message)

    print("\nUpdate Transaction published to RabbitMQ Exchange.\n")

    # 5. Return created payment
    return {
        "code": 201,
        "data": {
            "orders1_result": orders1_result,
            "orders2_result": orders2_result
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an payment...")
    app.run(host="0.0.0.0", port=5101, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
