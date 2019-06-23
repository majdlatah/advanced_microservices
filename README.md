# Advanced microservices

In this project we used docker containers, RabbitMQ (Message Broker) and Nameko (Remote Procedure Call (RPC) inter-service-communication) frameworks. Flask is also used to implement the API gateway.

As shown below the COMPUTING service first checks whether the customer exists in our MySQL database or not using Customer Services to get the customer ID and Email, then it will amount given by the user to (dolar, euro). Finally, it will use the MAIL service to send the result of to the user’s email address. The communication is done based on RPC communication. Nameko services are containers.

<p align="center">
  <img src="https://github.com/majdlatah/advanced_microservices/blob/master/ar.png">
</p>

Our defined REST API are shown below:

<p align="center">
  <img src="https://github.com/majdlatah/advanced_microservices/blob/master/api.png">
</p>

Computer API: curl -X POST "http://127.0.0.1:5000/compute" -H "Content-Type: application/json" -d "{ \"changeto\": \"dolar\", \"customerid\": 1, \"value\": 40}"

Customer API: http://127.0.0.1:5000/customer/1

Mail API: curl -X POST "127.0.0.1:5000/email" -H "Content-Type: application/json" -d "{ \"email\": \"youremail@outlook.com\", \"msg\": \"My message\", \"subject\": \"My topic\"}"
