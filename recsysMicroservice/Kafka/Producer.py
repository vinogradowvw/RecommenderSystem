from confluent_kafka import Producer
import yaml
import json

class KafkaProducer():

    def __init__(self):
        
        with open("./recsysMicroservice/config.yml", 'r') as file:
            self.__kafka_conf = yaml.safe_load(file)['Kafka']

        self.__producer = Producer(self.__kafka_conf['producer'])

    def produce(self, data, correlation_id):
        print('Proucing data to kafka')
        print(data)
        self.__producer.produce(
            topic=self.__kafka_conf["producer.topic"],
            value=json.dumps({"data": data}),
            headers=[('Correlation-ID', correlation_id)]
        )

