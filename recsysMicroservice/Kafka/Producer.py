from confluent_kafka import Producer
import yaml

class KafkaProducer():

    def __init__(self):
        
        with open("./recsysMicroservice/config.yml", 'r') as file:
            self.__kafka_conf = yaml.safe_load(file)['Kafka']

        self.__producer = Producer(self.__kafka_conf['producer'])

    def produce(self, data, correlation_id):
        self.__producer.produce(
            topic=self.__kafka_conf["producer_topic"],
            value={"data": data},
            headers=[('Correlation-ID', correlation_id)]
        )

