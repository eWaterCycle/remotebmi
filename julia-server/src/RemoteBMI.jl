module RemoteBmi

using HTTP

include("./serverimpl.jl")
using .ServerImpl

include("./APIServer.jl")
using .APIServer

function run_server(model, host="0.0.0.0")
    port = parse(Int, ENV["BMI_PORT"], default=50051)
    global MyModel = model
    try
        router = HTTP.Router()
        router = APIServer.register(router, ServerImpl;)
        server[] = HTTP.serve!(router, host, port; verbose=true;)
        wait(server[])
    catch ex
        @error("Server error", exception=(ex, catch_backtrace()))
    end
end

end