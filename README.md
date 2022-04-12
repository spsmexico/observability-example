### Demo

Este repositorio contiene un pequeño servicio python usando el framework Flask. Tiene 4 versiones ditintas y 1 servicio consumidor.

1 - Sin instrumentación (APM)

2 - Con instrumentación básica (APM)

3 - Instrumentación avanzada (APM)

4 - Instrumentación avanzada (APM) y logs en formato ECS (logger).

### Requerimientos
Tener docker instaldo y levantar una instancia de redis:

```
docker run -p 6379:6379 -d redis
```


Es recomendable un entorno virtual pero es posible saltarse este paso:
```
virtualenv -p python3 .venv
source .venv/bin/activate
```

Instalar dependencias:
```
pip install -r requirements.txt
```

Asegurate de tener los siguientes datos de tu instancia de Elastic:
```
APM:
server_url
token

Filebeat: 
cloud.id: deploymentname:secret123
cloud.auth: elastic:secret123
ó
output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "changeme"
```

Tener instalado Filebeat. Puedes descargar filebeat de aquí: https://www.elastic.co/downloads/beats/filebeat

APM-Server, Elasticsearch y Kibana se deben estar ejecutando. Puedes encontrar más información [aquí](https://www.elastic.co/elastic-stack/) u obtener una prueba gratuita de [Elastic Cloud](https://www.elastic.co/es/cloud/)

### Ejecutar Filebeat

```
mv filebeat.yml C:\Users\RicardoOrtega\Documents\filebeat-8.1.1-windows-x86_64
cd C:\Users\RicardoOrtega\Documents\filebeat-8.1.1-windows-x86_64
filebeat.exe -e 
```

### Iniciar servicios

```
python 01-app-uninstrumented.py
python 02-app-instrumented.py
python 03-app-instrumented-compression.py
python 04-app-ecs-logging.py
python 05-app-consumer.py
```

### Hacer peticiones a servicios
```
01-app-uninstrumented
curl localhost:5001/endpoint1

02-app-instrumented
curl localhost:5002/endpoint1

03-app-instrumented-compression
curl localhost:5003/endpoint1

04-app-ecs-logging
curl localhost:5004/endpoint1

05-app-consumer
curl localhost:5005/consume
```

### Ejecutar el script de carga
El script de carga hace peticiones a las 4 versiones del servicio en un bucle infinito. 

```
sh loadgen.sh
```


### Capturas de Kibana

![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-overview-2022-01-20-10_43_46](https://user-images.githubusercontent.com/11661400/150313736-05bf3ddf-1b82-40e8-94d0-948f04a75ecb.png)
![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-transactions-view-2022-01-20-10_44_23](https://user-images.githubusercontent.com/11661400/150313846-bff9ae02-4d6c-4ef9-844e-ff1aa265a727.png)
