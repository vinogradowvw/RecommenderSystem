from confluent_kafka import Consumer
from confluent_kafka import KafkaException, KafkaError
import yaml
import inspect
import json
from recsysMicroservice.Dependencies import get_kafka_producer, get_post_service, get_user_service


class KafkaConsumer():

    def __init__(self):
        with open("./recsysMicroservice/config.yml", 'r') as file:
            self.__kafka_conf = yaml.safe_load(file)['Kafka']
        print(self.__kafka_conf)
        self.__consumer = Consumer(self.__kafka_conf['consumer'])
        self.__producer = get_kafka_producer()
        self.user_service = get_user_service()
        self.post_service = get_post_service()
        self.__consume()

    def __consume(self):
        try:
            self.__consumer.subscribe(topics=[self.__kafka_conf["consumer.topic"]])
            print('Strarting consuming from topic {}'.format(self.__kafka_conf["consumer.topic"]))

            while True:
                msg = self.__consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                        #     (msg.topic(), msg.partition(), msg.offset()))
                        continue
                    elif msg.error():
                        print(msg.error())
                        raise KafkaException(msg.error())
                else:
                    value = json.loads(msg.value().decode('utf-8'))
                    print("Consumed message with value:")
                    print(value)
                    service_name, method_name = value['type'].split(".")
                    service = getattr(self, service_name)
                    method = getattr(service, method_name)
                    parameters = inspect.signature(method).parameters

                    args = {}
                    for param_name, param in parameters.items():
                        if param_name != "self":
                            args[param_name] = param.annotation(**value[param_name])

                    if (method_name.split("_")[0] == "get"):
                        self.__producer.produce(method(**args), correlation_id=dict(msg.headers()).get('Correlation-ID'))
                    else:
                        method(**args)

                    self.__consumer.commit(asynchronous=True)
        finally:
            self.__consumer.close()
