module ServerImpl

import BasicModelInterface as BMI

function initialize(req::HTTP.Request, bmi_initialize_request::BmiInitializeRequest;) -> Nothing
    global m
    # TODO where does Model come from?
    m = BMI.initialize(Model, bmi_initialize_request.config_file;)
end

function get_component_name(req::HTTP.Request;) -> String
    return BMI.get_component_name(m)
end 

function get_input_item_count(req::HTTP.Request;) -> Int64
    return BMI.get_input_item_count(m)
end

function get_input_var_names(req::HTTP.Request;) -> Vector{String}
    return BMI.get_input_var_names(m)
end

function get_output_item_count(req::HTTP.Request;) -> Int64
    return BMI.get_output_item_count(m)
end

function get_output_var_names(req::HTTP.Request;) -> Vector{String}
    return BMI.get_output_var_names(m)
end

function get_value(req::HTTP.Request, name::String;) -> Vector{Float64}
    return BMI.get_value(m, name)
end

function get_value_at_indices(req::HTTP.Request, name::String, request_body::Vector{Int64};) -> Vector{Float64}
    return BMI.get_value_at_indices(m, name, request_body)
end

function get_grid_rank(req::HTTP.Request, grid::Int64;) -> Int64
    return BMI.get_grid_rank(m, grid)
end

function get_grid_size(req::HTTP.Request, grid::Int64;) -> Int64
    return BMI.get_grid_size(m, grid)
end

function get_grid_type(req::HTTP.Request, grid::Int64;) -> BmiGetGridTypeResponse
    return BMI.get_grid_type(m, grid)
end

function finalize(req::HTTP.Request;) -> Nothing
    BMI.finalize(m)
end

function update(req::HTTP.Request;) -> Nothing
    BMI.update(m)
end

function update_until(req::HTTP.Request, body::Float64;) -> Nothing
    BMI.update_until(m, body)
end

function get_grid_x(req::HTTP.Request, grid::Int64;) -> Vector{Float64}
    return BMI.get_grid_x(m, grid)
end

function get_grid_y(req::HTTP.Request, grid::Int64;) -> Vector{Float64}
    return BMI.get_grid_y(m, grid)
end

function get_grid_z(req::HTTP.Request, grid::Int64;) -> Vector{Float64}
    return BMI.get_grid_z(m, grid)
end

function set_value(req::HTTP.Request, name::String, request_body::Vector{Float64};) -> Nothing
    BMI.set_value(m, name, request_body)
end

function set_value_at_indices(req::HTTP.Request, name::String, bmi_set_value_at_indices_request::BmiSetValueAtIndicesRequest;) -> Nothing
    BMI.set_value_at_indices(m, name, bmi_set_value_at_indices_request)
end

function get_current_time(req::HTTP.Request;) -> Float64
    return BMI.get_current_time(m)
end

function get_end_time(req::HTTP.Request;) -> Float64
    return BMI.get_end_time(m)
end

function get_start_time(req::HTTP.Request;) -> Float64
    return BMI.get_start_time(m)
end

function get_time_step(req::HTTP.Request;) -> Float64
    return BMI.get_time_step(m)
end

function get_time_units(req::HTTP.Request;) -> String
    return BMI.get_time_units(m)
end

function get_grid_origin(req::HTTP.Request, grid::Int64;) -> Vector{Float64}
    return BMI.get_grid_origin(m, grid)
end

function get_grid_shape(req::HTTP.Request, grid::Int64;) -> Vector{Int64}
    return BMI.get_grid_shape(m, grid)
end

function get_grid_spacing(req::HTTP.Request, grid::Int64;) -> Vector{Float64}
    return BMI.get_grid_spacing(m, grid)
end

function get_grid_edge_count(req::HTTP.Request, grid::Int64;) -> Int64
    return BMI.get_grid_edge_count(m, grid)
end

function get_grid_edge_nodes(req::HTTP.Request, grid::Int64;) -> Vector{Int64}
    return BMI.get_grid_edge_nodes(m, grid)
end

function get_grid_face_count(req::HTTP.Request, grid::Int64;) -> Int64
    return BMI.get_grid_face_count(m, grid)
end

function get_grid_face_edges(req::HTTP.Request, grid::Int64;) -> Vector{Int64}
    return BMI.get_grid_face_edges(m, grid)
end

function get_grid_face_nodes(req::HTTP.Request, grid::Int64;) -> Vector{Int64}
    return BMI.get_grid_face_nodes(m, grid)
end

function get_grid_node_count(req::HTTP.Request, grid::Int64;) -> Int64
    return BMI.get_grid_node_count(m, grid)
end

function get_grid_nodes_per_face(req::HTTP.Request, grid::Int64;) -> Vector{Int64}
    return BMI.get_grid_nodes_per_face(m, grid)
end

function get_var_grid(req::HTTP.Request, name::String;) -> Int64
    return BMI.get_var_grid(m, name)
end

function get_var_itemsize(req::HTTP.Request, name::String;) -> Int64
    return BMI.get_var_itemsize(m, name)
end

function get_var_location(req::HTTP.Request, name::String;) -> GetVarLocationResponseLocation
    return BMI.get_var_location(m, name)
end

function get_var_nbytes(req::HTTP.Request, name::String;) -> Int64
    return BMI.get_var_nbytes(m, name)
end

function get_var_type(req::HTTP.Request, name::String;) -> String
    return BMI.get_var_type(m, name)
end

function get_var_units(req::HTTP.Request, name::String;) -> String
    return BMI.get_var_units(m, name)
end

end