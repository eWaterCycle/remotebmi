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
export BMI_PORT=50555
julia --project=$PWD heat_bmi_server.jl
```

Prepare a config file

```shell
wget https://github.com/csdms/bmi-example-julia/raw/main/example/heat.toml
```

Interact with it using the Python client.

```python
from remotebmi.client.client import RemoteBmiClient
from remotebmi.reserve import reserve_values

client = RemoteBmiClient('http://localhost:50555')
# TODO use placeholder for path
# client.initialize('<absolute path>/heat.toml')
client.initialize('/home/stefanv/git/eWaterCycle/remotebmi/python/heat.toml')
client.get_component_name()
'The 2D Heat Equation'
client.update()
client.get_current_time()
0.25
client.get_time_units()
's'
client.get_var_location('plate_surface__temperature')
'node'
client.get_var_type('plate_surface__temperature')
numpy.float64
client.get_var_grid('plate_surface__temperature')
0
client.get_grid_type(0)
'uniform_rectilinear'
dest = reserve_values(client, 'plate_surface__temperature')
r = client.get_value('plate_surface__temperature', dest)
r
client.finalize()
```
