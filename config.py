import logging

import pika


RMQ_HOST = "0.0.0.0"
RMQ_PORT = "5672"

RMQ_USER = "admin"
RMQ_PASSWORD = "admin"

MQ_EXCHANGE = ""
MQ_ROUTING_KEY = "news"


conntection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(
        username=RMQ_USER,
        password=RMQ_PASSWORD,
    ),
)


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=conntection_params,
    )


def configure_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
    )
