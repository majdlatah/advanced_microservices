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
    #email = request.json.get('email')
    #subject = "API Notification"
    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        rpc.mail.send(email, subject, msg)
        # asynchronously spawning the compute task
        #print result.result()
        #rpc.mail.send.call_async(email, subject, result)
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
    #email = request.json.get('email')
    msg = "Please wait the calculation, you'll receive an email with results"
    #subject = "API Notification"
    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        #rpc.mail.send.call_async(email, subject, msg)
        # asynchronously spawning the compute task
        result = rpc.compute.compute.call_async(changeto, value,customerid)
        #print result.result()
        #rpc.mail.send.call_async(email, subject, result)
        return msg, 200




#@app.route('/customer', methods=['GET'])
@app.route('/customer/<customerid>', methods = ['GET'])
def find(customerid):  
    #subject = "API Notification"
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
        # asynchronously spawning and email notification
        result = rpc.customer.find(customerid)
        if (result == 1):
            return "We Found the Customer",200
        else:
            return "Customer Not Found",404

        #asynchronously spawning the compute task
           #result = rpc.compute.compute.call_async("sum", value, other, email)
        #print result.result()
        #rpc.mail.send.call_async(email, subject, result)



app.run(
        host="0.0.0.0",
        port=5000
        )


