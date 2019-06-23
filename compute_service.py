import yagmail
from nameko.rpc import rpc, RpcProxy

class Compute(object):
    name = "compute"
    mail = RpcProxy('mail')
    customer = RpcProxy("customer")

    @rpc
    def compute(self, operation, value, myid):
        operations = {'dolar': lambda x: int(x)*5.8,
                      'euro': lambda x: int(x)*6.8}
        try:
            result = operations[operation](value)
        except Exception as e:
            self.mail.send.call_async(myid, "An error occurred", str(e))
            raise
        else:
            a,b = self.customer.find(myid)
            if a != 0:
                self.mail.send.call_async( b, "Your operation is complete!","The result is: %s" % result)
            return result

