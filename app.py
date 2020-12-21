import celery.bin.base
import logging
from celery import Celery
import os
import threading
import _thread as thread
import sys
from pyzabbix import ZabbixMetric, ZabbixSender
from decouple import config

logging.basicConfig(filename=config('LOG_PATH'), level=logging.INFO)
logger = logging.getLogger(__name__)


def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)

        task = state.tasks.get(event['uuid'])

        info = str(task.info()['exception'])
        name = str(task.name)
        value = f'Task: {name} | Error: {info}'
        logger.info(f"Task captured: {value}")
        packet = [
            ZabbixMetric(config('HOST'), 'celery[task]',value)
        ]
        result = ZabbixSender(use_config=config('PATH_AGENT_ZABBIX')).send(packet)
        logger.info(f"Result sending to zabbix: {result}")

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    logger.info("Service started")
    app = Celery(broker=config('BROKER_URL'))
    try:
        my_monitor(app)
    except Exception as ex:
        logger.info("Error!")
        logger.info(ex)