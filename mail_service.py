import yagmail
from nameko.rpc import rpc, RpcProxy


class Mail(object):
    name = "mail"

    @rpc
    def send(self, to, subject, contents):
        yag = yagmail.SMTP('majdlatah@gmail.com', 'password')
        yag.send(to=to.encode('utf-8'),
                 subject=subject.encode('utf-8'),
                 contents=[contents.encode('utf-8')])

