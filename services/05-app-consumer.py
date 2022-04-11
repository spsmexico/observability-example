from flask import Flask

# instrument flask with Elastic APM
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
import random
import time
from requests import request
import structlog

import ecs_logging
import logging
import requests

# disable the default flask logger
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Log to a file
handler = logging.FileHandler(filename='service5.log')
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

from elasticapm.handlers.structlog import structlog_processor
structlog.configure(
    processors=[structlog_processor,ecs_logging.StructlogFormatter()],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory()
)



app = Flask(__name__)

server_url = 'https://a4a3c652f5a84484837858075ff47ee6.apm.us-central1.gcp.cloud.es.io:443'
service_name = '05-app-consumer'
environment = 'production'

# this is just an example token - please replace with your token that you get from Elastic Cloud or your APM Server
token = 'if0SfRh1EhBu7UiBru'
apm = ElasticAPM(app, server_url=server_url, service_name=service_name, environment=environment,
                 secret_token=token, span_compression_enabled=True)
client = elasticapm.get_client()

# redis, slow and fast requests
@app.route("/consume")
def endpoint1():
    logger.info("Received request", extra={"http.request.method": "get"})

    logger.info('connecting to Redis 20 times')
    for x in range(5):
        response = requests.get("http://localhost:5004/endpoint1")
        logger.info(response.text)

    # slow down the request 10% of the time
    if random.randint(0,9) < 1:
        with elasticapm.capture_span('this is a slow span'):
            elasticapm.label(label1='slowed down deliberately')
            time.sleep(0.02)
            logger.info('slow request')
    else:
        with elasticapm.capture_span('this is a fast span'):
            logger.info('fast request')

    # we'll try to do something here that might fail
    try:
        # we fail for 10% of all requests
        if random.randint(0, 9) < 1:
            time.sleep(0.1)
            raise RuntimeError('Failed to do something')
    except Exception as e:
        logger.error(e)
        client.capture_exception()
        elasticapm.set_transaction_outcome(outcome='failure')

    return "Consulta"

app.run(host='0.0.0.0', port=5005)
