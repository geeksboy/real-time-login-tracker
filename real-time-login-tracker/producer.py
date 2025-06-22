import time, json, random
from kafka import KafkaProducer

# 👇 Replace 'localhost' with 'kafka' ONLY if you're running this from a Docker container
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # ✅ Change to 'kafka:9092' if inside Docker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

events = ["page_click", "scroll", "login", "logout"]
pages = ["/home", "/product", "/about", "/contact"]

while True:
    log = {
        "user_id": f"user_{random.randint(100, 999)}",
        "event": random.choice(events),
        "page": random.choice(pages),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    # 👇 Topic name — keep same in producer and consumer
    producer.send('user-activity', value=log)
    print("Sent:", log)
    time.sleep(1)
