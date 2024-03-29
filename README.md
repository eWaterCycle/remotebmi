# Remote BMI

The [Basic Model Interface (BMI)](https://bmi.readthedocs.io/en/stable/) is a standard interface for models. 
The interface is available in different languages and a [language agnosting version in SIDL](https://github.com/csdms/bmi/blob/stable/bmi.sidl).

To have a consumer of the model and the provider of the model seperated you can use grpc4bmi, but this only on languages that have a grpc implementation.
This repo replaced the gRPC protocol with an REST API.
The [REST API specification](openapi.yaml) is in the [OpenAPI](https://swagger.io/specification/) format.

## Usage

### Python consumer

A client can connect to a running server with the following code.

```python
from remotebmi.client import BmiClient

model = RemoteBmiClient('http://localhost:50051')
# Now you can use the BMI methods on model
# for example
model.initialize('config.file')
model.update()
model.get_value('var_name')
```

A client can also start a [Apptainer](https://apptainer.org) container containing the model and the server.

```python
from remotebmi.client import BmiClientApptainer

model = BmiClientApptainer('my_model.sif', work_dir='/tmp')
```

The client picks a random port and expects the container to run the BMI web server on that port.
The port is passed to the container using the `BMI_PORT` environment variable.

A client can also start a [Docker](https://docs.docker.com/engine/) container containing the model and the server.

```python
from remotebmi.client import BmiClientDocker

model = BmiClientDocker('ewatercycle/wflowjl:0.7.3', work_dir='/tmp')
```

The BMI web server inside the Docker container should be running on port 50051.
If the port is different, you can pass the port as the `image_port` argument to the `BmiClientDocker` constructor.

### Python provider

Given you have a model instance called `my_model` that has a BMI.

```python
import os
from remotebmi.server import RemoteBmiServer

port = int(os.environ.get('BMI_PORT', 50051))
app = RemoteBmiServer(my_model, port=port, host='localhost')
app.run()
```

### Julia provider

Given you have a model instance called `my_model` and a BMI called `BMI` inside the `MyModel` package.

```julia
using MyModel
using RemoteBMI

port = parse(Int, get(ENV, "BMI_PORT", 50051))
server = RemoteBmiServer(MyModel.my_model, MyModel.BMI, port=port, host="localhost")
run(server)
```

### R provider

Given you have a model called `ModelBmi` that has a BMI inside a `MyModel` R library.

```r
library(remotebmi)
library(MyModel)

port = as.integer(Sys.getenv("BMI_PORT", 50051))
server <- RemoteBmiServer$new(MyModel$ModelBmi, port=port, host="localhost")
server$run()
``` 

### Other languages

Any language that can run a HTTP server and parse/load JSON can be used as a provider.

The server should implement the [openapi.yaml specification](openapi.yaml).
