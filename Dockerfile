# Use the base Kafka Connect image
FROM confluentinc/cp-kafka-connect:latest

# Install the required plugin (HTTP connector in this case)
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-http:latest
