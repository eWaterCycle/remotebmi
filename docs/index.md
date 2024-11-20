# remotebmi

With remotebmi you can communicate to models using the [Basic Model Interface](bmi.md) using a 
RESTful API.
The REST API specification uses the [OpenAPI](openapi.md) format.

Documentation for the implementations in specific languages are available separately:

- [Python](https://www.ewatercycle.org/remotebmi/python)
- [Julia](https://www.ewatercycle.org/remotebmi/julia)
- [R](R/index.md)

## Quick start

### Python consumer

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

### Python provider

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

### Julia provider

Given you have a model class called `MyModel` and a BMI called `BMI` inside the `MyPackage` package.

```julia
using MyPackage
import RemoteBMI.Server: run_bmi_server

port = parse(Int, get(ENV, "BMI_PORT", "50051"))
run_bmi_server(MyPackage.Model, "0.0.0.0", port)
```

### Julia consumer

```julia
import RemoteBMI.Client: BMIClient
import BasicModelInterface as BMI
model = BMIClient("http://localhost:50555")
BMI.get_component_name(m)
```

### R provider

Given you have a model called `ModelBmi` that has a BMI inside a `MyModel` R library.

```r
library(remotebmi)
library(MyModel)

port = as.integer(Sys.getenv("BMI_PORT", 50051))
serve(MyModel::ModelBmi$new(), port=port, host="localhost")
``` 
