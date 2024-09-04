# TODO make dynamic, for example read from ARGS and import
# TODO include https://github.com/csdms/bmi-example-julia as test dependency 
using Heat

import RemoteBMI 

port = parse(Int, get(ENV, "BMI_SERVER_PORT", "50051"))
secret = get(ENV, "BMI_SERVER_SECRET", "")
RemoteBMI.run(Heat.Model, "0.0.0.0", port, secret)
