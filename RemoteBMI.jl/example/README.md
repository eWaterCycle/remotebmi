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
import os

client = RemoteBmiClient('http://localhost:50555')
client.initialize(os.getcwd() + '/heat.toml')
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
client.get_grid_shape(0)
dest = reserve_values(client, 'plate_surface__temperature')
r = client.get_value('plate_surface__temperature', dest)
r
client.finalize()
```

Interact using the Julia client.

```julia
# julia --project=$PWD/..
import RemoteBMI.Client: setup
import BasicModelInterface as BMI
model = setup("http://localhost:50555")
m = BMI.initialize(model, joinpath(pwd(), "heat.toml"))
BMI.get_component_name(m)
# "The 2D Heat Equation"
BMI.get_grid_type(m, 0)
# "uniform_rectilinear"
BMI.get_grid_shape(m, 0)
# {}
BMI.get_grid_rank(m, 0)
# 2
BMI.get_grid_x(m, 0, [0.0, 0.0])
```

# Run Wflow.jl

```shell
julia --project=.
]
add Wflow
# Install RemoteBMI
dev ..
<backspace>

# Download a parameter set
# From https://deltares.github.io/Wflow.jl/stable/user_guide/sample_data/#wflow_sbm_data
# with *nc moved to data/input
toml_url = "https://raw.githubusercontent.com/Deltares/Wflow.jl/master/test/sbm_config.toml"
staticmaps = "https://github.com/visr/wflow-artifacts/releases/download/v0.2.9/staticmaps-moselle.nc"
forcing = "https://github.com/visr/wflow-artifacts/releases/download/v0.2.6/forcing-moselle.nc"
instates = "https://github.com/visr/wflow-artifacts/releases/download/v0.2.6/instates-moselle.nc"
# create a "data" directory in the current directory
datadir = joinpath(@__DIR__, "data")
mkpath(datadir)
inputDir = joinpath(datadir, "input")
mkpath(inputDir)
toml_path = joinpath(@__DIR__, "sbm_config.toml")
# download resources to current and data dirs
download(staticmaps, joinpath(inputDir, "staticmaps-moselle.nc"))
download(forcing, joinpath(datadir, "forcing-moselle.nc"))
download(instates, joinpath(inputDir, "instates-moselle.nc"))
download(toml_url, toml_path)

# Run server
using Wflow
import RemoteBMI
port = parse(Int, get(ENV, "BMI_PORT", "50051"))
RemoteBMI.run(Wflow.Model, "0.0.0.0", port)
```

Interact with it using the Python client.

```python
from remotebmi.client.client import RemoteBmiClient
from remotebmi.reserve import reserve_values, reserve_grid_nodes, reserve_grid_edge_nodes, reserve_grid_nodes_per_face, reserve_grid_face_
import numpy as np
import os

client = RemoteBmiClient('http://localhost:50051')
# Change to location of sbm_config.toml
os.chdir('../RemoteBMI.jl/example')
%time client.initialize(os.getcwd() + '/sbm_config.toml')
CPU times: user 3.08 ms, sys: 8 μs, total: 3.09 ms
Wall time: 18.7 s
%time client.update()
CPU times: user 1.45 ms, sys: 78 μs, total: 1.53 ms
Wall time: 7.78 s
%time client.update()
CPU times: user 596 μs, sys: 980 μs, total: 1.58 ms
Wall time: 227 ms
client.get_component_name()
'sbm'
client.get_current_time()
172800.0
client.get_time_units()
's'
client.get_output_var_names()
['vertical.nlayers',
 'vertical.n_unsatlayers',
 ...
 'lateral.river.q',
 ...
 'lateral.river.reservoir.evaporation',
 'lateral.river.reservoir.actevap']
client.get_var_location('lateral.river.q')
'node'
client.get_var_type('lateral.river.q')
numpy.float64
client.get_var_grid('lateral.river.q')
3
client.get_grid_type(3)
'unstructured'
client.get_grid_rank(3)
2
client.get_grid_size(3)
5809
client.get_grid_shape(3, np.empty(2))
# Method does not exist, which is ok for this grid type
x = client.get_grid_x(3, reserve_grid_nodes(client, 3))
len(x)
5809
y = client.get_grid_y(3, reserve_grid_nodes(client, 3))
len(y)
5809
value = client.get_value('lateral.river.q', reserve_values(client, 'lateral.river.q'))
len(value)
5809
client.get_grid_node_count(3)
5809
client.get_grid_edge_count(3)
5808
client.get_grid_face_count(3)
# Method does not exist, which is ok for this var location
edge_nodes = client.get_grid_edge_nodes(3, reserve_grid_edge_nodes(client, 3))
len(edge_nodes)
11616
client.finalize()
```
