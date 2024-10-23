using Test
using Sockets
import RemoteBMI.Client: setup
import RemoteBMI.Server: run
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
  server_thread = Threads.@spawn run(FakeModel.Model, "0.0.0.0", port)
  # TODO sleep to wait for server to start?
  model = setup("http://localhost:$port")
  model = BMI.initialize(model, "config_file")

  @test BMI.get_component_name(model) == "FakeModel"
  @test BMI.get_grid_type(model, 1) == "uniform_rectilinear"
  @test BMI.get_grid_shape(model, 1) == [2, 3, 4]
  @test BMI.get_grid_x(model, 1, zeros(4)) == [0.1, 0.2, 0.3, 0.4]
  # Test that given array is filled after get_grid_x call
  function test_grid_x_filled()
    x = zeros(4)
    BMI.get_grid_x(model, 1, x)
    return x
  end
  @test test_grid_x_filled() == [0.1, 0.2, 0.3, 0.4]

  # TODO Stop server, now gets killed when Julia exits
end