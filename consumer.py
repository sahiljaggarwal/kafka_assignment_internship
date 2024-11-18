from kafka import KafkaConsumer, KafkaProducer
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KafkaConsumer")

# Kafka Topics
ORDERS_TOPIC = "orders"
ENRICHED_ORDERS_TOPIC = "enriched_orders"
INVALID_ORDERS_TOPIC = "invalid_orders"

# Kafka configurations
KAFKA_BROKER = "localhost:9092"

# Create Kafka Consumer
consumer = KafkaConsumer(
    ORDERS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="order-processing-group"
)

# Create Kafka Producers for valid and invalid data
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def process_order(order):
    """
    Process order to calculate total value.
    Perform validation and determine destination topic.
    """
    try:
        order_id = order.get("order_id")
        quantity = order.get("quantity")
        price = order.get("price")
        
        # Validation: Ensure quantity and price are positive numbers
        if quantity <= 0 or price <= 0:
            logger.warning(f"Invalid order: {order}")
            producer.send(INVALID_ORDERS_TOPIC, order)
            return
        
        # Enrich the order data
        total_value = quantity * price
        enriched_order = {
            **order,
            "total_value": total_value
        }
        
        logger.info(f"Enriched order: {enriched_order}")
        producer.send(ENRICHED_ORDERS_TOPIC, enriched_order)

    except Exception as e:
        logger.error(f"Error processing order: {order}, Error: {e}")

def consume_orders():
    """
    Consume messages from the 'orders' topic and process them.
    """
    for message in consumer:
        order = message.value
        logger.info(f"Received order: {order}")
        process_order(order)

if __name__ == "__main__":
    logger.info("Starting Kafka Consumer...")
    consume_orders()
