from proton import Message, Delivery
from proton.handlers import MessagingHandler
from proton.reactor import Container
import sys
import simpleMessage_pb2



# Connection parameters
host = 'localhost'  # Artemis broker host
port = 5672  # Default port for AMQP
username = 'admin'  # Username for authentication
password = 'admin'  # Password for authentication

if(len(sys.argv) != 2):
    print("Provide Queue name as argument")
    sys.exit()

queue_name = sys.argv[1]  # Name of the queue to consume messages from


class Consumer(MessagingHandler):
    def __init__(self, url):
        super(Consumer, self).__init__()
        self.url = url

    def on_start(self, event):
        conn = event.container.connect(url=self.url, user=username, password=password)
        event.container.create_receiver(conn, source=queue_name)

    def on_message(self, event):
        message = event.message
        print("Received message:")
        print("Subject:", message.subject)
        print("Body Before parsing:", message.body.decode('utf-16'))
        messageBody = simpleMessage_pb2.Hello()
        messageBody.ParseFromString(message.body)
        print("Body after parsing...")
        print("BodyHeader:", messageBody.header)
        print("BodyMessage:", messageBody.testMessage)

        # Manually send a disposition to acknowledge the message
        event.delivery.update(Delivery.ACCEPTED)

    def on_accepted(self, event):
        event.receiver.flow(1)

    def on_rejected(self, event):
        event.receiver.flow(1)

    def on_released(self, event):
        event.receiver.flow(1)

    def on_settled(self, event):
        event.receiver.flow(1)


# Create a consumer instance and run the reactor
consumer = Consumer(f'amqp://{host}:{port}')
Container(consumer).run()
