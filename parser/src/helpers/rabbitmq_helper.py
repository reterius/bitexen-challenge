import json
import pika


def data_parser(data):
    data = str(data, "UTF-8")
    data = json.loads(data)
    return data


class RabbitmqHelper:
    def __init__(self, host_uri: str, host_port: int = None, username: str = None, password: str = None,
                 is_dsn_conn=False, queue_name: str = None):
        self.host_uri = host_uri
        self.host_port = host_port
        self.username = username
        self.password = password
        self.is_dsn_conn = is_dsn_conn
        self.queue_name = queue_name

    def __create_parameters(self):
        if self.is_dsn_conn:
            return pika.URLParameters(self.host_uri)

        credentials = pika.PlainCredentials(self.username, self.password)
        return pika.ConnectionParameters(host=self.host_uri, port=self.host_port, credentials=credentials)

    def publish(self, queue_name: str, data: dict, priority: int):
        try:
            data_json = json.dumps(data)

            connection = pika.BlockingConnection(self.__create_parameters())
            channel = connection.channel()

            self.queue_declare(channel)

            args = {}
            args["x-max-priority"] = 100
            channel.queue_declare(
                queue=queue_name,
                durable=True,
                exclusive=False,
                auto_delete=False,
                arguments=args
            )

            channel.basic_publish(
                properties=pika.BasicProperties(priority=priority),
                exchange="",
                routing_key=queue_name,
                body=data_json,
                # properties = pika.BasicProperties(
                #     delivery_mode=2,  # make message persistent
                # )
            )
        except Exception as ex:
            raise Exception("RabbitMQ Publisher Exception", ex)

    def queue_declare(self, channel):
        args = {}
        args["x-max-priority"] = 100
        return channel.queue_declare(
            queue=self.queue_name,
            durable=True,
            exclusive=False,
            auto_delete=False,
            passive=False,
            arguments=args
        )

    def subscribe(self, queue_name: str, callback):
        try:
            connection = pika.BlockingConnection(self.__create_parameters())
            channel = connection.channel()

            channel.queue_declare(
                queue=queue_name,
                durable=False,
            )

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(callback, queue=queue_name, no_ack=True)

            channel.start_consuming()
        except Exception as ex:
            raise Exception("RabbitMQ Subscriber Exception", ex)
