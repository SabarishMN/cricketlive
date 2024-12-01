import yfinance as yf
import time
import pandas as pd
from kafka import KafkaProducer
from json import dumps
import requests
import time


def kafka_producer():
    producer = KafkaProducer(bootstrap_servers=['34.227.190.251:9134'],  # change ip and port number here
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
            "https://api.cricapi.com/v1/currentMatches?apikey=&offset=0")
        response1 = requests.get(
            "https://api.cricapi.com/v1/match_info?apikey=&offset=0&id=820cfd88-3b56-4a6e-9dd8-1203051140da")
        response_obj = response.json()
        data = response_obj['data']
        data_array=[]
        for match in data:
            data_array.append({
                'id': match['id'],
                'name': match['name'],
                'venue': match['venue'],
                'score': match['score'],
            })
        print(data_array)
        # print(df_stream)
        for i in range(0,10):
            time.sleep(1)
            print(i)
            producer.send('CricketData', value=data_array)  # Add topic name here
        time.sleep(2)
    print("done producing")


kafka_producer()
