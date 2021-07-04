from celery import Celery, platforms

import os

from src.helpers.general_helper import load_config

import json

app_config = load_config(os.environ.get("APP_CONFIG"))

os.environ['app_config_json'] = json.dumps(app_config)

worker = Celery('celery_worker')
platforms.C_FORCE_ROOT = True
celeryconfig = {}
celeryconfig['BROKER_URL'] = app_config['celery']['broker_url']

celeryconfig['CELERY_ACKS_LATE'] = True
celeryconfig['CELERYD_PREFETCH_MULTIPLIER'] = 1
celeryconfig['CELERY_RESULT_BACKEND'] = 'rpc://'

celeryconfig['CELERY_QUEUE_HA_POLICY'] = 'all'
celeryconfig['QUEUE_HA_POLICY'] = 'all'

celeryconfig['BROKER_HEARTBEAT'] = 0
celeryconfig['BROKER_POOL_LIMIT'] = None
celeryconfig['BROKER_TRANSPORT_OPTIONS'] = {'confirm_publish': True}
celeryconfig['CELERY_TASK_TRACK_STARTED'] = True
celeryconfig['CELERY_ACCEPT_CONTENT'] = ['pickle', 'json']

worker.config_from_object(celeryconfig)

celeryconfig['CELERY_INCLUDE'] = ['tasks']

worker.conf.broker_pool_limit = app_config['celery']['broker_pool_limit']
worker.conf.broker_connection_max_retries = app_config['celery']['broker_connection_max_retries']
worker.conf.worker_disable_rate_limits = app_config['celery']['worker_disable_rate_limits']

worker.conf.task_inherit_parent_priority = True

worker.conf.task_queue_max_priority = 100

worker.conf.beat_schedule = app_config['celery']['worker_beat_schedule']
