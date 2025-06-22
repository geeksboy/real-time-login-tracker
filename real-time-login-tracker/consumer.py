from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'user-activity',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

client = MongoClient("mongodb://localhost:27017/")
db = client.userlogs
collection = db.logs

for message in consumer:
    log = message.value
    collection.insert_one(log)
    print("Stored in MongoDB:", log)
