from nameko.rpc import rpc, RpcProxy
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="pmauser",
  passwd="password",
  database="resturant"
)

mycursor = mydb.cursor()

class Customer(object):
    name = "customer"

    @rpc
    def find(self, cno):
        mycursor.execute("SELECT c_email FROM customer where c_no=%s", (cno,))
        row_headers=[xf[0] for xf in mycursor.description] 
        myresult = mycursor.fetchone()
        json_data=[]
        email = myresult[0]
        #for x in myresult:
        #    json_data.append(dict(zip(row_headers,x)))
        
        if myresult != None:
            return 1,email.encode("latin-1")
        else:
            return 0,3
