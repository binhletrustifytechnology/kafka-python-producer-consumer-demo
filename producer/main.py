import socket
from fastapi import FastAPI
from confluent_kafka import Producer

app = FastAPI()
conf = {
    'bootstrap.servers': "kafka-broker:9092", # for kubernetes
    # 'bootstrap.servers': "host.docker.internal:29092",
    # 'bootstrap.servers': "localhost:29092",
    # 'bootstrap.servers': "localhost:9092",
    # 'bootstrap.servers': "kafka:9092",
    # 'client.id': socket.gethostname()
}
producer = Producer(conf)

@app.post("/produce")
async def produce(key: str):
    producer.produce('my-topic', key="key", value=key)
    # producer.flush()
    return {"status": "success"}
