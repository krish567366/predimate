# Updated consumer.py
from kafka import KafkaConsumer
import json

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = "my-kafka-kafka-bootstrap.default.svc.cluster.local:9092"
KAFKA_TOPIC = "predimate-data"

mqtt_to_kafka = {
    "predimate/vibration": KAFKA_TOPIC,
    "predimate/temperature": KAFKA_TOPIC,
    "predimate/current": KAFKA_TOPIC,
    "predimate/pressure": KAFKA_TOPIC,
    "predimate/flow": KAFKA_TOPIC,
    "predimate/gas": KAFKA_TOPIC,
    "predimate/emissions": KAFKA_TOPIC,
    "predimate/cpu": KAFKA_TOPIC,
    "predimate/memory": KAFKA_TOPIC,
    "predimate/disk_io": KAFKA_TOPIC,
    "predimate/network_latency": KAFKA_TOPIC,
    "predimate/network_packet_loss": KAFKA_TOPIC,
}

def consume_from_mqtt():
    import paho.mqtt.client as mqtt

    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT broker")
        client.subscribe(list(mqtt_to_kafka.keys()))

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            kafka_producer.send(mqtt_to_kafka[msg.topic], json.dumps(data).encode('utf-8'))
            print(f"Published to Kafka: {data}")
        except Exception as e:
            print(f"Error processing MQTT message: {e}")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()

def create_kafka_producer():
    from kafka import KafkaProducer
    return KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

if __name__ == "__main__":
    kafka_producer = create_kafka_producer()
    consume_from_mqtt()