using Test
using Sockets
using HTTP
using JSON
import RemoteBMI
import RemoteBMI.Client: BMIClient
import RemoteBMI.Server: run_bmi_server
import BasicModelInterface as BMI

include("fake.jl")

function find_unused_port()
  port, server = listenany(8000)
  close(server)
  return port
end

# TODO move client to julia/src/Client.jl and export as RemoteBMI.Client

@testset "RemoteBMI Tests" begin
  # Start server and initialize model
  port = find_unused_port()
  server_thread = Threads.@spawn run_bmi_server(FakeModel.Model, "0.0.0.0", port)
  # TODO sleep to wait for server to start?
  model = BMIClient("http://localhost:$port")

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
    @test BMI.get_input_var_names(model) == ["invar1"]
    @test BMI.get_input_item_count(model) == 0
    @test BMI.get_output_var_names(model) == ["var1", "var2"]
    @test BMI.get_output_item_count(model) == 2
  end

  @testset "Variable information functions" begin
    @test BMI.get_var_grid(model, "var1") == 1

    # TODO handle errors using middleware on server
    # @test_throws ArgumentError("Variable not found") BMI.get_var_grid(model, "missing")

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
    @test BMI.get_value(model, "var1", zeros(Int, 4)) == [1.0, 2.0, 3.0, 4.0]
    function test_get_value_filled()
      x = zeros(4)
      BMI.get_value(model, "var1", x)
      return x
    end
    @test test_get_value_filled() == [1.0, 2.0, 3.0, 4.0]
    # TODO does index start at 0 or 1?
    @test BMI.get_value_at_indices(model, "var1", zeros(2), [2, 4]) == [2.0, 4.0]
    function test_get_value_at_indices_filled()
      x = zeros(Int, 2)
      BMI.get_value_at_indices(model, "var1", x, Int[2, 4])
      return x
    end
    @test test_get_value_at_indices_filled() == [2.0, 4.0]

    @test BMI.set_value(model, "var1", [1.2, 2.2, 3.2, 4.2]) === nothing
    # Check that set_value filled the array correctly
    @test BMI.get_value(model, "var1", zeros(4)) == [1.2, 2.2, 3.2, 4.2]

    @test BMI.set_value_at_indices(model, "var1", Int[2, 4], [5.3, 6.3]) === nothing
    # Check that set_value_at_indices filled the array correctly
    @test BMI.get_value(model, "var1", zeros(4)) == [1.2, 5.3, 3.2, 6.3]
  end

  @testset "Model grid functions" begin
    @test BMI.get_grid_type(model, 1) == "uniform_rectilinear"
    @test BMI.get_grid_size(model, 1) == 4
    @test BMI.get_grid_rank(model, 1) == 3
    @test BMI.get_grid_shape(model, 1) == Int[2, 3, 4]
    @test BMI.get_grid_spacing(model, 1, zeros(3)) == [0.1, 1.1, 2.1]
    @test BMI.get_grid_origin(model, 1, zeros(3)) == [0.1, 0.2, 0.3]
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
    @test BMI.get_grid_edge_nodes(model, 1, zeros(Int, 16)) ==
          Int[0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3]
    @test BMI.get_grid_face_edges(model, 1, zeros(Int, 11)) == Int[0, 1, 2, 3, 4, 5, 6, 1, 6, 7, 2]
    @test BMI.get_grid_face_nodes(model, 1, zeros(Int, 11)) == Int[0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3]
    @test BMI.get_grid_nodes_per_face(model, 1, zeros(Int, 3)) == Int[4, 4, 3]
  end

  @testset "IEEE non-finite values" begin
    raw_model = RemoteBMI.Server.m
    raw_get(path) = JSON.parse(String(HTTP.get(model.base_url * path).body))
    number_cases = ((NaN, "NaN"), (Inf, "Infinity"), (-Inf, "-Infinity"), (1.25, 1.25))
    time_cases = ((Inf, "Infinity"), (-Inf, "-Infinity"), (2.5, 2.5))

    @testset "get_value" begin
      for (value, encoded) in number_cases
        raw_model.values = [value, 2.0, value, 4.0]

        @test raw_get("/get_value/var1") == [encoded, 2.0, encoded, 4.0]
        dest = zeros(4)
        @test BMI.get_value(model, "var1", dest) === dest
        @test isequal(dest, raw_model.values)
        @test isequal(BMI.get_value(model, "var1", zeros(Float32, 4)), Float32.(raw_model.values))
      end

      @test raw_get("/get_value/intvar") == fill(2^53 + 1, 4)
      @test BMI.get_value(model, "intvar", zeros(Int64, 4)) == fill(2^53 + 1, 4)

      raw_model.values = [NaN]
      @test raw_get("/get_value/var1") == ["NaN"]
      @test isequal(BMI.get_value(model, "var1", zeros(1)), [NaN])
    end

    @testset "get_value_at_indices" begin
      for (value, encoded) in number_cases
        raw_model.values = [value, 2.0, value, 4.0]

        @test isequal(BMI.get_value_at_indices(model, "var1", zeros(2), [1, 2]), [value, 2.0])
        response = HTTP.post(model.base_url * "/get_value_at_indices/var1", ["Content-Type" => "application/json"], "[0]")
        @test JSON.parse(String(response.body)) == [encoded]
        @test isequal(BMI.get_value_at_indices(model, "var1", zeros(1), [1]), [value])
      end

      @test BMI.get_value_at_indices(model, "intvar", zeros(Int64, 1), [2]) == [2^53 + 1]
    end

    @testset "set_value" begin
      for (value, _) in number_cases
        raw_model.values = zeros(4)
        values = [value, 2.0, value, 4.0]

        @test BMI.set_value(model, "var1", values) === nothing
        @test isequal(raw_model.values, values)
      end

      @test BMI.set_value(model, "var1", [1, 2, 3, 4]) === nothing
      @test raw_model.values == [1.0, 2.0, 3.0, 4.0]

      raw_model.values = zeros(1)
      @test BMI.set_value(model, "var1", [Inf]) === nothing
      @test raw_model.values == [Inf]
    end

    @testset "set_value_at_indices" begin
      for (value, _) in number_cases
        raw_model.values = [1.0, 2.0, 3.0, 4.0]

        @test BMI.set_value_at_indices(model, "var1", [2], [value]) === nothing
        @test isequal(raw_model.values[2], value)
      end

      @test BMI.set_value_at_indices(model, "var1", [2], [5]) === nothing
      @test raw_model.values[2] == 5.0
    end

    @testset "get_grid_spacing" begin
      for (value, encoded) in number_cases
        raw_model.spacing .= value
        dest = zeros(length(raw_model.spacing))

        @test raw_get("/get_grid_spacing/1") == fill(encoded, length(dest))
        @test BMI.get_grid_spacing(model, 1, dest) === dest
        @test isequal(dest, raw_model.spacing)
      end
    end

    @testset "get_grid_origin" begin
      for (value, encoded) in number_cases
        raw_model.origin .= value
        dest = zeros(length(raw_model.origin))

        @test raw_get("/get_grid_origin/1") == fill(encoded, length(dest))
        @test BMI.get_grid_origin(model, 1, dest) === dest
        @test isequal(dest, raw_model.origin)
      end
    end

    @testset "get_grid_x" begin
      for (value, encoded) in number_cases
        raw_model.x .= value
        dest = zeros(length(raw_model.x))

        @test raw_get("/get_grid_x/1") == fill(encoded, length(dest))
        @test BMI.get_grid_x(model, 1, dest) === dest
        @test isequal(dest, raw_model.x)
      end
    end

    @testset "get_grid_y" begin
      for (value, encoded) in number_cases
        raw_model.y .= value
        dest = zeros(length(raw_model.y))

        @test raw_get("/get_grid_y/1") == fill(encoded, length(dest))
        @test BMI.get_grid_y(model, 1, dest) === dest
        @test isequal(dest, raw_model.y)
      end
    end

    @testset "get_grid_z" begin
      for (value, encoded) in number_cases
        raw_model.z .= value
        dest = zeros(length(raw_model.z))

        @test raw_get("/get_grid_z/1") == fill(encoded, length(dest))
        @test BMI.get_grid_z(model, 1, dest) === dest
        @test isequal(dest, raw_model.z)
      end
    end

    @testset "get_current_time" begin
      for (value, encoded) in time_cases
        raw_model.current = value

        @test raw_get("/get_current_time") == encoded
        @test BMI.get_current_time(model) == value
      end
    end

    @testset "get_start_time" begin
      for (value, encoded) in time_cases
        raw_model.start = value

        @test raw_get("/get_start_time") == encoded
        @test BMI.get_start_time(model) == value
      end
    end

    @testset "get_end_time" begin
      for (value, encoded) in time_cases
        raw_model.stop = value

        @test raw_get("/get_end_time") == encoded
        @test BMI.get_end_time(model) == value
      end
    end

    @testset "get_time_step" begin
      for (value, encoded) in time_cases
        raw_model.step = value

        @test raw_get("/get_time_step") == encoded
        @test BMI.get_time_step(model) == value
      end
    end

    @testset "update_until" begin
      for (value, _) in time_cases
        raw_model.current = 0.0

        @test BMI.update_until(model, value) === nothing
        @test isequal(raw_model.current, value)
      end
    end
  end

  # TODO Stop server, now gets killed when Julia exits
end
