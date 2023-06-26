from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container


# Connection parameters
host = 'localhost'  # Artemis broker host
port = 5672  # Default port for AMQP
username = 'admin'  # Username for authentication
password = 'admin'  # Password for authentication
queue_name = 'my_queue'  # Name of the queue to send messages to


class Producer(MessagingHandler):
    def __init__(self, url):
        super(Producer, self).__init__()
        self.url = url

    def on_start(self, event):
        conn = event.container.connect(url=self.url, user=username, password=password)
        event.container.create_sender(conn, target=queue_name)

    def on_sendable(self, event):
        message = Message(subject='Hello', body="Hello, World!")
        event.sender.send(message)
        event.sender.close()
        #event.connection.close()


# Create a producer instance and run the reactor
producer = Producer(f'amqp://{host}:{port}')
Container(producer).run()
