import sys
import os
from os import environ
from flask_cors import CORS
from flask import Flask, request, jsonify
from invokes import invoke_http

import amqp_setup
import pika
import json
import copy

app = Flask(__name__)
CORS(app)

inventory_URL = environ.get('inventory_URL') or "http://localhost:5001/inventory"
order_URL = environ.get('order_URL') or "http://localhost:5003/orders"


@app.route("/order", methods=['POST'])
def order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPlaceOrder(order)
            # return jsonify(result), result["code"]
            return jsonify(result)

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processPlaceOrder(order):
    # 2. Try to update inventory
    # Invoke the Inventory microservice
    print('\n-----Invoking Inventory microservice-----')
    inventory_results = []
    for item in order["cart_item"]:
        type = item["packaging_type"]
        quantity = item["quantity"]
        body = {"quantity": quantity}
        inventory_result = invoke_http(
            inventory_URL + "/loan/" + type, method='PUT', json=body)
        # Check the order result; if a failure, send it to the error microservice.
        code = inventory_result["code"]
        if code not in range(200, 300):

            print("Update inventory failed")

            # 3. Return error
            return {
                "code": 500,
                "data": {"inventory_result": inventory_result},
                "message": "Process of placing order failed at updating Inventory."
            }
        inventory_results.append(inventory_result)
    print(inventory_results)

    # 3. Record a new order
    # Invoke the Orders microservice
    print('\n-----Invoking Orders microservice-----')
    orders_result = invoke_http(order_URL, method='POST', json=order)

    # Check the order result; if a failure, send it to the error microservice.
    code = orders_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": orders_result},
            "message": "Order creation failure sent for error handling."
        }
    print(orders_result)

    # 4. Send notification
    print('\n\n-----Publishing the (Order info) message with routing_key=notification-----')
    message = copy.deepcopy(orders_result)
    message["notification_type"] = "order"
    message = json.dumps(message)

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notification",
                                     body=message)

    print("\nOrder published to RabbitMQ Exchange.\n")

    # 5. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "inventory_results": inventory_results,
            "orders_result": orders_result
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
