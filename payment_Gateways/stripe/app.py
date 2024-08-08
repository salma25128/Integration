
import json
import stripe
import os
from flask import Flask, render_template, request,jsonify

app = Flask(__name__)

# define your secret keys as environment variables

# export STRIPE_SECRET_KEY='put your secret api key here'
# export STRIPE_PUBLISHABLE_KEY='put your publishable api key here'

stripe_keys = {
    "secret_key":os.environ["STRIPE_SECRET_KEY"],
    "publishable_key":os.environ["STRIPE_PUBLISHABLE_KEY"],
}

stripe.api_key = stripe_keys["secret_key"]

@app.route('/')
def checkout():
        return render_template('checkout.html',key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 1000

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    return render_template('charge.html', amount=amount)


if __name__ == '__main__':
     app.run()

endpoint_secret = 'Put your endpoint here'

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
      payment_intent = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
