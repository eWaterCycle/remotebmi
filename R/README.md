
# remotebmi

<!-- badges: start -->
<!-- badges: end -->

The goal of remotebmi is to allow a model with BMI interface written in R to be called from a Python client via a http json webservice.

## Installation

You can install the development version of remotebmi from [GitHub](https://github.com/) with:

``` r
# install.packages("pak")
pak::pak("github::eWaterCycle/remotebmi/R")
```

## Example

This is a basic example which shows you how to solve a common problem:

``` r
library(remotebmi)
## basic example code

pak::pak("github::ClaudiaBrauer/WALRUS")
pak::pak("github::eWaterCycle/bmi-r")
pak::pak('configr')
source('https://github.com/eWaterCycle/grpc4bmi-examples/raw/master/walrus/walrus-bmi.r')
model <- WalrusBmi$new()

remotebmi::serve(model)
Fire started at 127.0.0.1:50051
```

With Python client test the model

```python
import os
from remotebmi.client.client import RemoteBmiClient
from remotebmi.reserve import reserve_values, reserve_grid_padding, reserve_grid_shape
import numpy as np

client = RemoteBmiClient('http://localhost:50051')
!wget https://github.com/eWaterCycle/grpc4bmi-examples/raw/refs/heads/master/walrus/walrus.yml
!wget https://github.com/ClaudiaBrauer/WALRUS/raw/refs/heads/master/demo/data/PEQ_Hupsel.dat
# Make data path in walrus.yml absolute
client.initialize( os.getcwd() + '/walrus.yml')
client.update()
# model information functions
client.get_component_name()
'WALRUS'
client.get_output_var_names()
['ETact', 'Q', 'fGS', 'fQS', 'dV', 'dVeq', 'dG', 'hQ', 'hS', 'w']
client.get_output_item_count()
10
client.get_input_var_names()
# kaput, R server returns '' instead of '[]', while reqres::format_json()(list()) does return '[]'
client.get_input_item_count()
0
# Time functions
client.get_current_time()
367417
client.get_time_units()
'hours since 1970-01-01 00:00:00.0 00:00'
client.get_time_step()
1
client.get_end_time()
368904
client.get_start_time()
367416
# Variable information functions
client.get_var_grid('Q')
0
client.get_var_type('Q')
numpy.float64
client.get_var_units('Q')
'mm/h'
client.get_var_itemsize('Q')
8
client.get_var_nbytes('Q')
8
client.get_var_location('Q')
'node'
# Variable getter and setter functions
client.get_value('Q', dest=np.array([.1]))
array([0.0044])
client.get_value_at_indices('Q', dest=np.array([0.0]), inds=np.array([0]))
array([0.0044])  # walrus ignores inds and just always returns lumped value
# setter not implemented in walrus
# Model grid functions
client.get_grid_rank(0)
2
client.get_grid_type(0)
'uniform_rectilinear'
client.getgrid_size(0)
1
client.get_grid_shape(0, reserve_grid_shape(client, 0))
array([1, 1])
client.get_grid_origin(0, reserve_grid_padding(client, 0))
array([ 6.6544, 52.0613])
client.get_grid_spacing(0, reserve_grid_padding(client, 0))
array([0, 0])
# Other grid function not needed for walrus
# And finally
client.finalize()
```
