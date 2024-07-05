# TODO make dynamic, for example read from ARGS and import
# TODO include https://github.com/csdms/bmi-example-julia as test dependency 
import Heat.Model

import RemoteBMI 

BMIServer.run_server(Heat.Model)
