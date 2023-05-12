import json
import os
from os import environ
from invokes import invoke_http

import amqp_setup

payment_URL = environ.get('payment_URL') or "http://localhost:5004/payment"


def receivePayment():
    amqp_setup.check_setup()

    queue_name = 'payment'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    body = json.loads(body)

    print("\nReceived Order by " + __file__)
    processTransaction(body)
    print()  # print a new line feed


def processTransaction(payment):
    # washer_id = info['washer_id']
    # packaging_type = info['packaging_type']
    # quantity = int(info['quantity'])

    print("Record a Payment:")
    # Invoke the transaction microservice
    print('\n\n-----Invoking payment microservice-----')
    payment_transaction = invoke_http(payment_URL, method="POST", json=payment)
    print("payment_transaction:", payment_transaction)


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        "payment", amqp_setup.exchangename))
    receivePayment()
