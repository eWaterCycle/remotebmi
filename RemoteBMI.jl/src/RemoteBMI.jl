module RemoteBMI

using HTTP

include("./BmiServer.jl")
using .BmiServer

import BasicModelInterface as BMI

# TODO move route implementations to own module

function initialize(req::HTTP.Request, initialize_request::InitializeRequest)::Nothing
    global m
    m = BMI.initialize(MyModel, initialize_request.config_file)
    return nothing
end

function get_component_name(req::HTTP.Request)::GetComponentNameResponse
    return GetComponentNameResponse(BMI.get_component_name(m))
end

function get_input_item_count(req::HTTP.Request;)::Int64
    return BMI.get_input_item_count(m)
end

function get_input_var_names(req::HTTP.Request;)::Vector{String}
    return BMI.get_input_var_names(m)
end

function get_output_item_count(req::HTTP.Request;)::Int64
    return BMI.get_output_item_count(m)
end

function get_output_var_names(req::HTTP.Request;)::Vector{String}
    return BMI.get_output_var_names(m)
end

function reserve_get_value(m, name::String;)::Vector{Float64}
    raw_dtype = BMI.get_var_type(m, name)
    item_size = BMI.get_var_itemsize(m, name)
    total_size = BMI.get_var_nbytes(m, name)
    size = total_size ÷ item_size
    dtype_table = Dict(
        "Float64" => Float64,
        "Float32" => Float32,
        "Int64" => Int64,
        "Int32" => Int32,
        "Bool" => Bool,
    )
    dtype = get(dtype_table, raw_dtype, Any)
    if dtype == Any
        error("Invalid data type: $raw_dtype")
    end
    return zeros(dtype, size)
end

function get_value(req::HTTP.Request, name::String;)::Vector{Float64}
    dest = reserve_get_value(m, name)
    return BMI.get_value(m, name, dest)
end

function reserve_get_value_at_indices(m, name::String, indices::Vector{Int64};)::Vector{Float64}
    total_size = length(indices)
    raw_dtype = BMI.get_var_type(m, name)
    dtype_table = Dict(
        "Float64" => Float64,
        "Float32" => Float32,
        "Int64" => Int64,
        "Int32" => Int32,
        "Bool" => Bool,
    )
    dtype = get(dtype_table, raw_dtype, Any)
    if dtype == Any
        error("Invalid data type: $raw_dtype")
    end
    return zeros(dtype, total_size)
end

function get_value_at_indices(req::HTTP.Request, name::String, indices::Vector{Int64};)::Vector{Float64}
    dest = reserve_get_value_at_indices(m, name, indices)
    return BMI.get_value_at_indices(m, name, dest, indices)
end

function get_grid_rank(req::HTTP.Request, grid::Int64;)::Int64
    return BMI.get_grid_rank(m, grid)
end

function get_grid_size(req::HTTP.Request, grid::Int64;)::Int64
    return BMI.get_grid_size(m, grid)
end

function get_grid_type(req::HTTP.Request, grid::Int64;)::GetGridTypeResponse
    return GetGridTypeResponse(type=BMI.get_grid_type(m, grid))
end

function finalize(req::HTTP.Request;)::Nothing
    BMI.finalize(m)
    return nothing
end

function update(req::HTTP.Request;)::Nothing
    BMI.update(m)
    return nothing
end

function update_until(req::HTTP.Request, body::Float64;)::Nothing
    BMI.update_until(m, body)
    return nothing
end

function reserve_grid_coords(m, grid::Int64, dim_index::Int8)::Vector{Float64}
    mtype = BMI.get_grid_type(m, grid)
    if mtype in ["uniform_rectilinear", "rectilinear"]
        shape = BMI.get_grid_shape(m, grid)
        size = reverse(shape)[dim_index]
    elseif mtype in ["structured_quadrilateral"]
        size = BMI.get_grid_size(m, grid)
    elseif mtype in ["unstructured"]
        size = BMI.get_grid_node_count(m, grid)
    else
        error("Unsupported grid type: $mtype")
    end
    return zeros(Float64, size)
end

function get_grid_x(req::HTTP.Request, grid::Int64;)::Vector{Float64}
    x = reserve_grid_coords(m, grid, Int8(1))
    return BMI.get_grid_x(m, grid, x)
end

function get_grid_y(req::HTTP.Request, grid::Int64;)::Vector{Float64}
    y = reserve_grid_coords(m, grid, Int8(2))
    return BMI.get_grid_y(m, grid, y)
end

function get_grid_z(req::HTTP.Request, grid::Int64;)::Vector{Float64}
    z = reserve_grid_coords(m, grid, Int8(3))
    return BMI.get_grid_z(m, grid, z)
end

function set_value(req::HTTP.Request, name::String, request_body::Vector{Float64};)::Nothing
    BMI.set_value(m, name, request_body)
end

function set_value_at_indices(req::HTTP.Request, name::String, set_value_at_indices_request::SetValueAtIndicesRequest;)::Nothing
    BMI.set_value_at_indices(m, name, set_value_at_indices_request)
end

function get_current_time(req::HTTP.Request;)::Float64
    return BMI.get_current_time(m)
end

function get_end_time(req::HTTP.Request;)::Float64
    # Julia Heat model returns Inf, but that is not a valid JSON number. 
    # Therefore, it gets converted to null in the JSON response.
    return BMI.get_end_time(m)
end

function get_start_time(req::HTTP.Request;)::Float64
    return BMI.get_start_time(m)
end

function get_time_step(req::HTTP.Request;)::Float64
    return BMI.get_time_step(m)
end

function get_time_units(req::HTTP.Request;)::GetTimeUnitsResponse
    return GetTimeUnitsResponse(BMI.get_time_units(m))
end

function get_grid_origin(req::HTTP.Request, grid::Int64;)::Vector{Float64}
    origin = reserve_grid_spacing(m, grid)
    return BMI.get_grid_origin(m, grid, origin)
end

function get_grid_shape(req::HTTP.Request, grid::Int64;)::Vector{Int64}
    return BMI.get_grid_shape(m, grid)
end

function reserve_grid_spacing(m, grid::Int64;)::Vector{Float64}
    rank = BMI.get_grid_rank(m, grid)
    return zeros(Float64, rank)
end

function get_grid_spacing(req::HTTP.Request, grid::Int64;)::Vector{Float64}
    spacing = reserve_grid_spacing(m, grid)
    return BMI.get_grid_spacing(m, grid, spacing)
end

function get_grid_edge_count(req::HTTP.Request, grid::Int64;)::Int64
    return BMI.get_grid_edge_count(m, grid)
end

function reserve_grid_edge_nodes(m, grid::Int64;)::Vector{Int64}
    edge_count = BMI.get_grid_edge_count(m, grid)
    return zeros(Int64, 2 * edge_count)
end

function get_grid_edge_nodes(req::HTTP.Request, grid::Int64;)::Vector{Int64}
    edge_nodes = reserve_grid_edge_nodes(m, grid)
    return BMI.get_grid_edge_nodes(m, grid, edge_nodes)
end

function get_grid_face_count(req::HTTP.Request, grid::Int64;)::Int64
    return BMI.get_grid_face_count(m, grid)
end

function reserve_grid_nodes_per_face(m, grid::Int64;)::Vector{Int64}
    face_count = BMI.get_grid_face_count(m, grid)
    return zeros(Int64, face_count)
end

function reserve_grid_face(edges, grid::Int64;)::Vector{Int64}
    nodes_per_face = reserve_grid_nodes_per_face(m, grid)
    BMI.get_grid_nodes_per_face(m, grid, nodes_per_face)
    return zeros(Int64, sum(nodes_per_face))
end

function get_grid_face_edges(req::HTTP.Request, grid::Int64;)::Vector{Int64}
    face_edges = reserve_grid_face(m, grid)
    return BMI.get_grid_face_edges(m, grid, face_edges)
end

function get_grid_face_nodes(req::HTTP.Request, grid::Int64;)::Vector{Int64}
    face_nodes = reserve_grid_face(m, grid)
    return BMI.get_grid_face_nodes(m, grid, face_nodes)
end

function get_grid_node_count(req::HTTP.Request, grid::Int64;)::Int64
    return BMI.get_grid_node_count(m, grid)
end

function get_grid_nodes_per_face(req::HTTP.Request, grid::Int64;)::Vector{Int64}
    nodes_per_face = reserve_grid_nodes_per_face(m, grid)
    return BMI.get_grid_nodes_per_face(m, grid, nodes_per_face)
end

function get_var_grid(req::HTTP.Request, name::String;)::Int64
    return BMI.get_var_grid(m, name)
end

function get_var_itemsize(req::HTTP.Request, name::String;)::Int64
    return BMI.get_var_itemsize(m, name)
end

function get_var_location(req::HTTP.Request, name::String;)::GetVarLocationResponseLocation
    return GetVarLocationResponseLocation(BMI.get_var_location(m, name))
end

function get_var_nbytes(req::HTTP.Request, name::String;)::Int64
    return BMI.get_var_nbytes(m, name)
end

function get_var_type(req::HTTP.Request, name::String;)::GetVarTypeResponse
    raw_type = BMI.get_var_type(m, name)
    map = Dict(
        "Float64" => "double",
        "Float32" => "float32",
        "Int64" => "int64",
        "Int32" => "int32",
        "Bool" => "bool",
    )
    type = get(map, raw_type, Any)
    if type == Any
        error("Invalid data type returned by model: $raw_type, allowed types are: Float64, Float32, Int64, Int32")
    end
    return GetVarTypeResponse(type)
end

function get_var_units(req::HTTP.Request, name::String;)::GetVarUnitsResponse
    return GetVarUnitsResponse(BMI.get_var_units(m, name))
end

"""
    run(model, host, port)

Expose the specified model as web service.

# Arguments
- `model`: The model to be initialized and run.
- `host`: The hostname or IP address.
- `port`: The port number on to run the service.

"""
function run(model, host, port)
    global MyModel = model
    try
        router = HTTP.Router()
        router = BmiServer.register(router, @__MODULE__)
        server = HTTP.serve!(router, host, port; verbose=true)
        wait(server)
    catch ex
        @error("Server error", exception=(ex, catch_backtrace()))
    end
end

include("Client.jl")
export Client

end