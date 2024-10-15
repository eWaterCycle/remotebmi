using Test
using Sockets
import RemoteBMI

include("fake.jl")


function find_unused_port()
    port, server = listenany(8000)
    close(server)
    return port
end

# TODO move client to RemoteBMI.jl/src/Client.jl and export as RemoteBMI.Client
module Client
    using HTTP
    using JSON
    import RemoteBMI

    function initialize(base_url::String, config_file::String)
        HTTP.post(
            base_url * "/initialize",
            ["Content-Type" => "application/json"],
            json(RemoteBMI.InitializeRequest(config_file))
        )
    end

    function get_component_name(base_url::String)
        response = HTTP.get(base_url * "/get_component_name")
        return JSON.parse(String(response.body))["name"]
    end
end

@testset "RemoteBMI Tests" begin
  # Start server and initialize model
  port = find_unused_port()
  server_thread = Threads.@spawn RemoteBMI.run(FakeModel.Model, "0.0.0.0", port)
  url = "http://localhost:$port"
  # TODO sleep to wait for server to start?
  Client.initialize(url, "config_file")

  @test Client.get_component_name(url) == "FakeModel"

  # TODO Stop server, now gets killed when Julia exits
end