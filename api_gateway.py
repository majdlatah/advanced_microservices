from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


@app.route('/email', methods=['POST'])
def email():
    """
    Micro Service Based Mail API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: data
          properties:
            email:
              type: string
            subject:
              type: string
            msg:
              type: string
    responses:
      200:
        description: Email message has been submitted
    """
    email = request.json.get('email')
    subject = request.json.get('subject')
    msg = request.json.get('msg')

    with ClusterRpcProxy(CONFIG) as rpc:
        rpc.mail.send(email, subject, msg)
        return msg, 200

@app.route('/compute', methods=['POST'])
def compute():
    """
    Micro Service Based Compute API, which also uses Mail and Customer Micro services via RPC communication
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: data
          properties:
            changeto:
              type: string
              enum:
                - dolar
                - euro
            value:
              type: integer
            customerid:
              type: integer
    responses:
      200:
        description: Please wait the calculation, you'll receive an email with results
    """
    changeto = request.json.get('changeto')
    value = request.json.get('value')
    customerid = request.json.get('customerid')
    msg = "Please wait the calculation, you'll receive an email with results"
    with ClusterRpcProxy(CONFIG) as rpc:
        result = rpc.compute.compute.call_async(changeto, value,customerid)
        return msg, 200


@app.route('/customer/<customerid>', methods = ['GET'])
def find(customerid):
    """
    Micro Service Based Customer API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: customerid
        description: Please enter your customer id
        in: customerid
        required: true
    responses:
      200:
        description: We Found the Customer
      404:
        description: Customer Not Found
    """
    with ClusterRpcProxy(CONFIG) as rpc:
        res,b = rpc.customer.find(customerid)
        if (res == 1):
            return "We Found the Customer",200
        else:
            return "Customer Not Found",404


app.run(host="0.0.0.0",port=5000)
