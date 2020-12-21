# celery_zabbix_monitor
Monitor your Celery tasks sending failure tasks to Zabbix Server

Requirements
- py-zabbix
- Celery
- Decouple

Important!
You have to put the argument -E on all your workers, to able to celery send events.
If you use celery as Service on Linux, put in CELERY_OPTS

1 - Clone the repo

2 - link celery_monitor.service do system services

3 - Configure the .service file for you env Python and app.py locations

4 - Create a .env file for configs: 

    BROKER_URL = 'redis//localhost:6379' (path for Broker)
    HOST = 'parlatore' (name of Host machine on Zabbix - Not Host Server**)
    PATH_AGENT_ZABBIX = '/etc/zabbix/zabbix_agent2.conf' (Path to file location of agent2)
    LOG_PATH = '/home/ubuntu/celery_zabbix_monitor/monitor.log' (Path to file location of monitor.log)

