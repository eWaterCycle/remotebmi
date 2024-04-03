module BMIServer

using HTTP

# TODO make dynamic, for example read from ARGS and import
# TODO include https://github.com/csdms/bmi-example-julia as test dependency 
import Heat.Model

include("./serverimpl.jl")
using .ServerImpl

include("./APIServer.jl")
using .APIServer

function run_server(port=50051)
    try
        router = HTTP.Router()
        router = APIServer.register(router, ServerImpl;)
        server[] = HTTP.serve!(router, port)
        wait(server[])
    catch ex
        @error("Server error", exception=(ex, catch_backtrace()))
    end
end

end

BMIServer.run_server()