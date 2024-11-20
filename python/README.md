# Remote BMI

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
[![Codecov test coverage](https://codecov.io/gh/eWaterCycle/remotebmi/graph/badge.svg)](https://app.codecov.io/gh/eWaterCycle/remotebmi)

The [Basic Model Interface (BMI)](https://bmi.readthedocs.io/en/stable/) is a standard interface for models. 
The interface is available in different languages and a [language agnosting version in SIDL](https://github.com/csdms/bmi/blob/stable/bmi.sidl).

To have a consumer of the model and the provider of the model seperated you can use [grpc4bmi](https://grpc4bmi.readthedocs.io/), but this only works on languages that have a grpc implementation.
This Python package replaced the gRPC protocol with an REST API.
The [REST API specification](https://github.com/eWaterCycle/remotebmi/blob/main/openapi.yaml) is in the [OpenAPI](https://swagger.io/specification/) format.

Remotebmi is available in other languages see [here](https://github.com/eWaterCycle/remotebmi?tab=readme-ov-file#structure).

## Difference from BMI

- Request body and response body are in JSON format
- On errors you get 4xx and 5xx responses with [Problem Details](https://tools.ietf.org/html/rfc7807) as response body
- Variable names must be URL safe
- Variable type must be in enum.
- get_value_ptr function is not available

## Consumer

Installation

```shell
pip install remotebmi
```

A client can connect to a running server with the following code.

```python
from remotebmi import RemoteBmiClient

model = RemoteBmiClient('http://localhost:50051')
# Now you can use the BMI methods on model
# for example
model.initialize('config.file')
model.update()
model.get_value('var_name')
```

A client can also start a [Apptainer](https://apptainer.org) container containing the model and the server.

```python
from remotebmi import BmiClientApptainer

model = BmiClientApptainer('my_model.sif', work_dir='/tmp')
```

The client picks a random port and expects the container to run the BMI web server on that port.
The port is passed to the container using the `BMI_PORT` environment variable.

A client can also start a [Docker](https://docs.docker.com/engine/) container containing the model and the server.

```python
from remotebmi import BmiClientDocker

model = BmiClientDocker('ewatercycle/wflowjl:0.7.3', work_dir='/tmp')
```

The BMI web server inside the Docker container should be running on port 50051.
If the port is different, you can pass the port as the `image_port` argument to the `BmiClientDocker` constructor.

## Provider

Given you have a model class called `MyModel` in a package `mypackage` then the web service can be started with the following command.

```shell
BMI_MODULE=mypackage BMI_CLASS=MyModel run-bmi-server 
```

For example [leakybucket](https://github.com/eWaterCycle/leakybucket-bmi):

```shell
pip install leakybucket
BMI_MODULE=leakybucket.leakybucket_bmi BMI_CLASS=LeakyBucketBmi run-bmi-server
```

and the client can connect to it with the following code.

```python
> from remotebmi import RemoteBmiClient
> client = RemoteBmiClient('http://localhost:50051')
> client.get_component_name()
leakybucket
```

## Documentation

In a Python environment, go to the docs directory, do `pip install -r requirements.txt`
and then `make html`.
