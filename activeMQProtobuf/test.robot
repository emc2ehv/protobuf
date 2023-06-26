*** Settings ***
Library    Producer.py

*** Variables ***
${pm}    simpleMessage_pb2.Hello()
${pm.header}    'Test Type'
${pm.testMessage}    'Hello, World!'
${sm}    ${pm}.SerializeToString()
${producer}    Producer('amqp://localhost:5672', ${sm})
${container}    Container(${producer})


*** Test Cases ***
Print Run Container and test
    Log    ${container}.run()
