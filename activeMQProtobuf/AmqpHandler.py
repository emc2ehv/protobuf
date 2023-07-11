from __future__ import print_function
import optparse
from proton import Message, Url
from proton.handlers import MessagingHandler
from proton.reactor import Container


class Server(MessagingHandler):
    def __init__(self, url, address):
        super(Server, self).__init__()
        self.url = url
        self.address = address

    def on_start(self, event):
        print("Listening on", self.url)
        self.container = event.container
        self.conn = event.container.connect(self.url)
        self.receiver = event.container.create_receiver(self.conn, self.address)
        self.server = self.container.create_sender(self.conn, None)

    def on_message(self, event):
        print("Received", event.message)
        self.server.send(Message(address=event.message.reply_to, body=event.message.body.upper(),
                                 correlation_id=event.message.correlation_id))


parser = optparse.OptionParser(usage="usage: %prog [options]")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address from which messages are received (default %default)")
opts, args = parser.parse_args()

url = Url(opts.address)

try:
    Container(Server(url, url.path)).run()
except KeyboardInterrupt:
    pass