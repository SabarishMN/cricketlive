import yfinance as yf
import time
import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests
import time


def kafka_producer():
    producer = KafkaProducer(bootstrap_servers=['34.227.190.251:9136'],  # change ip and port number here
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    # run for 10 iterations
    # sleep for 1 sec for every iteration
    # Change topic name
    # Create a new topic cli kafka
    # change S3 folder name
    # change port

    t_end = time.time() + 1 * 1  # Amount of time data is sent for in seconds
    # df_stream = pd.DataFrame(columns=["Name", "Price", "Timestamp"])
    while time.time() < t_end:
        response = requests.get(
            "https://api.cricapi.com/v1/currentMatches?apikey=b424&offset=0")
        response_obj = response.json()
        data = response_obj['data']
        data_array=[]
        i=0
        for match in data:
            data_array[i] = {
                'id': match['id'],
                'name': match['name'],
                'venue': match['venue'],
                'score': match['score'],
            }
            i = i + 1
        print(data_array)
        # print(df_stream)
        producer.send('CricketData', value=data)  # Add topic name here
        # time.sleep(2)
    print("done producing")


kafka_producer()
