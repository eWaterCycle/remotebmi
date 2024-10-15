using Test
using Sockets
import RemoteBMI
import BasicModelInterface as BMI

include("fake.jl")

function find_unused_port()
    port, server = listenany(8000)
    close(server)
    return port
end

# TODO move client to RemoteBMI.jl/src/Client.jl and export as RemoteBMI.Client

@testset "RemoteBMI Tests" begin
  # Start server and initialize model
  port = find_unused_port()
  server_thread = Threads.@spawn RemoteBMI.run(FakeModel.Model, "0.0.0.0", port)
  # TODO sleep to wait for server to start?
  model = RemoteBMI.Client.setup("http://localhost:$port")
  model = BMI.initialize(model, "config_file")

  @test BMI.get_component_name(model) == "FakeModel"

  # TODO Stop server, now gets killed when Julia exits
end