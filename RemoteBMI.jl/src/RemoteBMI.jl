module RemoteBMI

using HTTP

include("./APIServer.jl")
using .APIServer

include("./serverimpl.jl")
using .ServerImpl


function run(model, host, port)
    global MyModel = model
    try
        router = HTTP.Router()
        router = APIServer.register(router, ServerImpl;)
        server = HTTP.serve!(router, host, port; verbose=true)
        wait(server)
    catch ex
        @error("Server error", exception=(ex, catch_backtrace()))
    end
end

end