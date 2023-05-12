from flask import Flask, jsonify, redirect
import os
from flask_cors import CORS
import stripe


app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "default_key")
stripe.api_key = "<STRIPE API KEY>"


@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    try:
        # Create new Checkout Session for the order
        # Other optional params include:

        # For full details see https:#stripe.com/docs/api/checkout/sessions/create
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/washer-make-payment",
            mode='payment',
            line_items=[{
                "price": "price_1MsTwuHfoHRbQNfbrH3UAdrJ",
                "quantity": 1
            }]
        )
        print("it worked")
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print("it failed")
        return jsonify(error=str(e)), 403


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for Stripe Wrapper...")
    app.run(host="0.0.0.0", port=5002, debug=True)
