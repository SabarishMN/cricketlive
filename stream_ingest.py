import time
from kafka import KafkaConsumer
from json import loads
import json
from s3fs import S3FileSystem


def kafka_consumer():
    s3 = S3FileSystem()
    DIR = "s3://ece5984-s3-sabarishm/Cricketdata"            # Add S3 bucket location
    t_end = time.time() + 60 * 5  # Amount of time data is sent for
    while time.time() < t_end:
        consumer = KafkaConsumer(
            'CricketData',  # add Topic name here
            bootstrap_servers=['34.227.190.251:9134'],  # add your IP and port number here
            value_deserializer=lambda x: loads(x.decode('utf-8')))

        for count, i in enumerate(consumer):
            with s3.open("{}/cricket_data.json".format(DIR),
                         'w') as file:
                json.dump(i.value, file)
    print("done consuming")
