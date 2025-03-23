import logging
import time

from typing import TYPE_CHECKING

from config import (
    get_connection,
    configure_logging,
    MQ_EXCHANGE,
    MQ_ROUTING_KEY
)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

log = logging.getLogger(__name__)


def process_new_messages(
    channel: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("channel: %s", channel)
    log.info("method: %s", method)
    log.info("properties: %s", properties)
    log.warning("[ ] Start proccesing message %r", body)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    log.warning("[X] Finished proccesing message %r", body)
    


def consume_messages(channel: "BlockingChannel") -> None:
    channel.basic_consume(
        queue=MQ_ROUTING_KEY,
        on_message_callback=process_new_messages,
        # auto_ack=True, # лучще не использовать
    )
    log.warning("Wating for messages")
    channel.start_consuming()


def main():
    configure_logging(level=logging.WARNING)
    with get_connection() as connection:
        log.info("Created connection: %s", connection)

        with connection.channel() as channel:
            log.info("Created channel: %s", channel)
            consume_messages(channel=channel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
