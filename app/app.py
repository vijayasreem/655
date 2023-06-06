from flask import Flask, request, redirect
from flask_restful import Resource, Api
import stripe

app = Flask(__name__)
api = Api(app)

class PaymentGateway(Resource):
    def post(self):
        # Get payment method from request
        payment_method = request.form.get('payment_method')
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
            payment_method=payment_method
        )
        # Redirect user to payment page
        return redirect(payment_intent.payment_method.redirect.url)

# Handle successful and failed payments
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    try:
        # Get payment intent from request
        payment_intent = stripe.PaymentIntent.retrieve(
            request.form.get('payment_intent')
        )
        # Check if payment is successful
        if payment_intent.status == 'succeeded':
            return 'Payment successful!'
        else:
            return 'Payment failed!'
    except Exception as e:
        # Log and handle payment errors
        print('Error: ', e)
        return 'An error occurred while processing your payment.'

# Add PaymentGateway resource
api.add_resource(PaymentGateway, '/payment-gateway')

if __name__ == '__main__':
    app.run()