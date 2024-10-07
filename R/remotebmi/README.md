
# remotebmi

<!-- badges: start -->
<!-- badges: end -->

The goal of remotebmi is to allow a model with BMI interface written in R to be called from a Python client via a http json webservice.

## Installation

You can install the development version of remotebmi from [GitHub](https://github.com/) with:

``` r
# install.packages("pak")
pak::pak("github::eWaterCycle/remotebmi/R/remotebmi")
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
from remotebmi.reserve import reserve_values
import numpy as np

client = RemoteBmiClient('http://localhost:50051')
!wget https://github.com/eWaterCycle/grpc4bmi-examples/raw/refs/heads/master/walrus/walrus.yml
!wget https://github.com/ClaudiaBrauer/WALRUS/raw/refs/heads/master/demo/data/PEQ_Hupsel.dat
# Make data path in walrus.yml absolute
client.initialize( os.getcwd() + '/walrus.yml')
client.get_component_name()
'WALRUS'

client.update()
client.get_current_time()
367417
client.get_time_units()
'hours since 1970-01-01 00:00:00.0 00:00'
client.get_output_var_names()
['ETact', 'Q', 'fGS', 'fQS', 'dV', 'dVeq', 'dG', 'hQ', 'hS', 'w']
# TODO add to AbstractBmi and WalrusBmi
# client.get_var_location('Q')
client.get_var_type('Q')
numpy.float64
client.get_var_grid('Q')
0
client.get_grid_type(0)
'rectilinear'
client.get_value('Q', dest=np.array([.1]))
array([0.0044])
client.get_var_nbytes('Q')
'mm/h'
dest = reserve_values(client, 'Q')
r = client.get_value('Q', dest)
r
client.finalize()

```