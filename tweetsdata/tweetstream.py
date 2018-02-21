
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


import TwitterAPI
from TwitterAPI.TwitterError import *
from reader import init_api
from flask import Flask, jsonify, g
from background import make_celery
from random import random
import json

app = Flask(__name__)

with app.app_context():
    g = {'a':12}
    api = init_api()
    app.config.update(
        CELERY_BROKER_URL='amqp://localhost',
        CELERY_RESULT_BACKEND='amqp://localhost'
    )
    celery = make_celery(app)


    # @celery.task()
    # def stream():
    #     while True:
    #         try:
    #             iterator = api.request('statuses/filter', {
    #                 'locations':'-3.223999,55.932888,-3.170612,55.958842'
    #             }).get_iterator()
    #             for item in iterator:
    #                 if 'text' in item:
    #                     with open('realtimetweets.json', 'w') as fp:
    #                         print(getattr(item, 'text'))
    #                         json.dump(getattr(item, 'text'), fp)

    #                 elif 'disconnect' in item:
    #                     event = item['disconnect']
    #                     if event['code'] in [2,5,6,7]:
    #                         # something needs to be fixed before re-connecting
    #                         raise Exception(event['reason'])
    #                     else:
    #                         # temporary interruption, re-try request
    #                         break
    #         except TwitterRequestError as e:
    #             if e.status_code < 500:
    #                 # something needs to be fixed before re-connecting
    #                 raise
    #             else:
    #                 # temporary interruption, re-try request
    #                 pass
    #         except TwitterConnectionError:
    #             # temporary interruption, re-try request
    #             pass

    @celery.task()
    def setg():
        setattr(g, 'a', random())


    # @app.route('/echo')
    # def send():
    #     try:
    #         with open('realtimetweets.json', 'r+') as fp:
    #             tws = json.load(fp)
    #             fp.close()
    #             return tws
    #     except:
    #         return('Not available')

    @app.route('/')
    def hello():
        return 'Hello World!'
    
    @app.route('/echo')
    def get_g():
        print(g['a'])
        return(str(g['a']))

