# Dependencies
- ActiveMQ Artemis broker
- Protobuf
- Robot Framework
- Apache QPID Proton


# Start ActiveMQ Artemis broker
`docker run --rm -e AMQ_USER=admin -e AMQ_PASSWORD=admin -e AMQ_EXTRA_ARGS="--relax-jolokia" -p 61616:61616 -p 8161:8161 -p 5672:5672 --name artemis quay.io/artemiscloud/activemq-artemis-broker`
