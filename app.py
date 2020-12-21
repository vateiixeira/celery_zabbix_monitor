import celery.bin.base
import logging
from functools import wraps
from celery import Celery
from django.conf import settings
import os
import time
import threading
import _thread as thread
import sys
from pyzabbix import ZabbixMetric, ZabbixSender
from decouple import config


def my_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

    
        info = str(task.info()['exception'])
        name = str(task.name)
        value = f'Task: {name} | Error: {info}'
        packet = [
            ZabbixMetric('parlatore', 'celery[task]',value)
        ]
        ZabbixSender(use_config='/etc/zabbix/zabbix_agent2.conf').send(packet)

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                '*': state.event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    app = Celery(broker=config('BROKER_URL'))
    my_monitor(app)