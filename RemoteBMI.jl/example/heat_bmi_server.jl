# TODO make dynamic, for example read from ARGS and import
# TODO include https://github.com/csdms/bmi-example-julia as test dependency 
using Heat

import RemoteBMI 

port = parse(Int, get(ENV, "BMI_PORT", 50051))
RemoteBMI.run(Heat.Model, "0.0.0.0", port)
