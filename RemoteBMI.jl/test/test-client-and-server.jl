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

  @testset "Model control functions" begin
    @test BMI.get_current_time(model) == 0
    @test BMI.update(model) === nothing
    @test BMI.get_current_time(model) == 1

    @test BMI.finalize(model) === nothing
    @test BMI.get_current_time(model) == -1

    @test BMI.update_until(model, 3.0) === nothing
    @test BMI.get_current_time(model) == 3.0
  end

  @testset "Model information functions" begin
    @test BMI.get_component_name(model) == "FakeModel"
    @test size(BMI.get_input_var_names(model)) == 0
    @test BMI.get_input_item_count(model) == 0
    @test BMI.get_output_var_names(model) == ["var1", "var2"]
    @test BMI.get_output_item_count(model) == 2
  end

  @testset "Variable information functions" begin
    @test BMI.get_var_grid(model, "var1") == 1
    @test BMI.get_var_type(model, "var1") == "Float64"
    @test BMI.get_var_units(model, "var1") == "unit1"
    @test BMI.get_var_itemsize(model, "var1") == 8
    @test BMI.get_var_nbytes(model, "var1") == 32
    @test BMI.get_var_location(model, "var1") == "node"
  end

  @testset "Time functions" begin
    @test BMI.get_current_time(model) == 3
    @test BMI.get_start_time(model) == 0
    @test BMI.get_end_time(model) == 168
    @test BMI.get_time_step(model) == 1
    @test BMI.get_time_units(model) == "h"
  end

  @testset "Variable getter and setter functions" begin
    @test BMI.get_value(model, "var1", zeros(4)) == [1.0, 2.0, 3.0, 4.0]
    function test_get_value_filled()
      x = zeros(4)
      BMI.get_value(model, "var1", x)
      return x
    end
    @test test_get_value_filled() == [1.0, 2.0, 3.0, 4.0]
    # TODO does index start at 0 or 1?
    @test BMI.get_value_at_indices(model, "var1", zeros(2), [2, 4]) == [2.0, 4.0]
    function test_get_value_at_indices_filled()
      x = zeros(2)
      BMI.get_value_at_indices(model, "var1", x, [2, 4])
      return x
    end
    @test test_get_value_at_indices_filled() == [2.0, 4.0]

    @test BMI.set_value(model, "var1", [1.2, 2.2, 3.2, 4.2]) === nothing
    # Check that set_value filled the array correctly
    @test BMI.get_value(model, "var1", zeros(4)) == [1.2, 2.2, 3.2, 4.2]

    @test BMI.set_value_at_indices(model, "var1", [2, 4], [1.3, 2.3]) === nothing
    # Check that set_value_at_indices filled the array correctly
    @test BMI.get_value(model, "var1", zeros(4)) == [1.2, 1.3, 3.2, 2.3]
  end

  @testset "Model grid functions" begin
    @test BMI.get_grid_type(model, 1) == "uniform_rectilinear"
    @test BMI.get_grid_size(model, 1) == 4
    @test BMI.get_grid_rank(model, 1) == 3
    @test BMI.get_grid_shape(model, 1) == [2, 3, 4]
    @test BMI.get_grid_spacing(model, 1, zeros(3)) == [0.1, 0.1, 0.3]
    @test BMI.get_grid_origin(model, 1, zeros(3)) == [0.1, 1.1, 2.1]
    @test BMI.get_grid_x(model, 1, zeros(4)) == [0.1, 0.2, 0.3, 0.4]
    # Test that given array is filled after get_grid_x call
    function test_grid_x_filled()
      x = zeros(4)
      BMI.get_grid_x(model, 1, x)
      return x
    end
    @test test_grid_x_filled() == [0.1, 0.2, 0.3, 0.4]
    @test BMI.get_grid_y(model, 1, zeros(3)) == [1.1, 1.2, 1.3]
    @test BMI.get_grid_z(model, 1, zeros(2)) == [2.1, 2.2]
    @test BMI.get_grid_node_count(model, 1) == 6
    @test BMI.get_grid_edge_count(model, 1) == 8
    @test BMI.get_grid_face_count(model, 1) == 3
    @test BMI.get_grid_edge_nodes(model, 1, zeros(16)) ==
          [0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3]
    @test BMI.get_grid_face_edges(model, 1, zeros(12)) == [0, 1, 1, 2, 2, 0, 1, 3, 3, 2, 2, 4]
    @test BMI.get_grid_face_nodes(model, 1, zeros(9)) == [0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3]
    @test BMI.get_grid_nodes_per_face(model, 1, zeros(3)) == [4, 4, 3]
  end

  # TODO Stop server, now gets killed when Julia exits
end
