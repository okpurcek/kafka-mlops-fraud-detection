import time
import json
import random
from kafka import KafkaProducer
from datetime import datetime

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

TOPIC_NAME = 'transactions'
CITIES = ["Istanbul", "New York", "London", "Berlin", "Tokyo", "Paris"]

print(f"💳 Transaction Stream Started on topic: {TOPIC_NAME}")
print("Press Ctrl+C to stop.")

while True:
    # Simulate Fraud (5% probability)
    is_fraud = random.random() < 0.05
    
    if is_fraud:
        # Anomaly: High amount or Suspicious Location
        amount = random.randint(5000, 20000)
        city = "UNKNOWN_IP_ADDR"
    else:
        # Normal Behavior
        amount = random.randint(10, 500)
        city = random.choice(CITIES)

    # Create Message
    transaction = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "amount": amount,
        "city": city,
        "is_fraud": is_fraud,
        "account_id": f"ACC-{random.randint(1000,9999)}"
    }

    # Send to Kafka
    producer.send(TOPIC_NAME, value=transaction)
    
    # Log to terminal
    status = "🚨 FRAUD" if is_fraud else "✅ OK"
    print(f"[{status}] Sent: ${amount} from {city}")

    # Random delay for realistic stream effect
    time.sleep(random.uniform(0.1, 1.0))