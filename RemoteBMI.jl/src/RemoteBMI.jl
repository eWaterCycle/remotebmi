"""RemoteBmi module.

For server use

```julia-repl
julia> import RemoteBMI.Server: run_bmi_server
julia> using Heat
julia> run_bmi_server(Heat.Model, "localhost", 8000)
[ Info: Listening on: 0.0.0.0:50051, thread id: 1
```

For client use

```julia-repl
julia> import RemoteBMI.Client: BMIClient
julia> import BasicModelInterface as BMI
julia> model = BMIClient("http://localhost:8000")
julia> model = BMI.initialize(model, "config_file")
julia> BMI.get_component_name(model)
"The 2D Heat Equation"
```

"""
module RemoteBMI

include("./Server.jl")
export Server

include("./Client.jl")
export Client

end
