# Run bmi-example-julia as server

```shell
# Install bmi-example-julia
julia
] 
activate .
add https://github.com/csdms/bmi-example-julia#b5d963e6bf864f5d42769e6cc0814dd7bffc9264
# Install RemoteBMI
dev ..
CTRL-D
# Run server
export BMI_SERVER_PORT=50555
julia --project=$PWD heat_bmi_server.jl
```

Prepare a config file

```shell
wget https://github.com/csdms/bmi-example-julia/raw/main/example/heat.toml
```

Interact with it using the Python client.

```python
from remotebmi.client.client import RemoteBmiClient
from remotebmi.client.reserve import reserve_values

client = RemoteBmiClient('http://localhost:50555')
# TODO use placeholder for path
# client.initialize('<absolute path>/heat.toml')
client.initialize('/home/stefanv/git/eWaterCycle/remotebmi/python/heat.toml')
# TODO Julia server throws error here
client.get_component_name()
client.update()
client.get_current_time()
dest = reserve_values(client, 'plate_surface__temperature')
r = client.get_value('plate_surface__temperature', dest)
r
client.finalize()
```
