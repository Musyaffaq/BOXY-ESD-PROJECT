import json
import os

import amqp_setup

from twilio.rest import Client

# Twilio details
account_sid = '<TWILIO ACCOUNT SID>'
auth_token = '<TWILIO AUTH TOKEN>'
client = Client(account_sid, auth_token)

sendFromNumber = '<SEND FROM NUMBER>'
sendToNumber = '<SEND TO NUMBER>'


def receiveNotification():
    amqp_setup.check_setup()

    queue_name = 'notify'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    body = json.loads(body)
    notification_type = body["notification_type"]
    print(body)

    if notification_type == "order":
        print("\nReceived Order by " + __file__)
        processOrder(body)
        print()  # print a new line feed
    elif notification_type == "payment":
        print("\nReceived Payment by " + __file__)
        processPayment(body)
        print()  # print a new line feed
    elif notification_type == "update":
        print("\nReceived Update by " + __file__)
        processUpdate(body)
        print()  # print a new line feed


def processOrder(order):
    info = order['data']
    hawker_id = info['hawker_id']
    order_id = info['order_id']

    OrderMsg = "Dear " + str(hawker_id) + ", \n" + "We have received your order! Order id :" + \
        str(order_id) + " has been recorded successfully! Thank you!"

    message = client.messages.create(
        from_=sendFromNumber,
        body=OrderMsg,
        to=sendToNumber)

    print("Record an Order:")
    print(order)
    print(message.sid)


def processPayment(payment):
    hawker_id = payment['hawker_id']
    orders = payment['orders']

    paymentMsg = "Dear " + str(hawker_id) + ", \n" + "Your payment for order id(s) " + orders + " has been successful! Thank you!"

    message = client.messages.create(
        from_=sendFromNumber,
        body=paymentMsg,
        to=sendToNumber)

    print("Record a Payment:")
    print(payment)
    print(message.sid)


def processUpdate(update):
    washer_id = update['washer_id']
    packaging_type = update['packaging_type']
    quantity = update['quantity']

    paymentMsg = "Dear " + str(washer_id) + ", \n" + "Your washing update of " + str(quantity) + " " + packaging_type + " has been successful! Thank you!"

    message = client.messages.create(
        from_=sendFromNumber,
        body=paymentMsg,
        to=sendToNumber)

    print("Record an Update:")
    print(update)
    print(message.sid)


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        "notification", amqp_setup.exchangename))
    receiveNotification()
