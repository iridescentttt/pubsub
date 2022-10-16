# PubSub with python and grpc

Pre-install:


```bash
pip install grpcio 
pip install grpcio-tools
```

usage example: 

run server

```bash
python3 pubsub_server.py
```

publish request

```bash
python3 pubsub_client.py publish channel1 "hello world" 1
```

subscribe request

```bash
python3 pubsub_client.py subscribe channel1 1
```