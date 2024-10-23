"""RemoteBmi module.

For server use

```julia-repl
julia> import RemoteBMI.Server: run
julia> using Heat
julia> run(Heat.Model, "localhost", 8000)
[ Info: Listening on: 0.0.0.0:50051, thread id: 1
```

For client use

```julia-repl
julia> import RemoteBMI.Client: setup
julia> import BasicModelInterface as BMI
julia> model = setup("http://localhost:8000")
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
