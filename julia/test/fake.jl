module FakeModel

import BasicModelInterface as BMI

Base.@kwdef mutable struct Model
  values::Vector{Float64} = [1.0, 2.0, 3.0, 4.0]
  current::Float64 = 0.0
end

BMI.initialize(::Type{Model}, config_file) = Model()
function BMI.update(m::Model)
  m.current += BMI.get_time_step(m)
  return nothing
end
function BMI.update_until(m::Model, time::Float64)
  m.current = time
  return nothing
end
function BMI.finalize(m::Model)
  m.current = -1
  return nothing
end

# Model information functions
BMI.get_component_name(m::Model) = "FakeModel"
# TODO empty vector gives TypeError
BMI.get_input_var_names(m::Model) = ["invar1"]
BMI.get_input_item_count(m::Model) = 0
BMI.get_output_var_names(m::Model) = ["var1", "var2"]
BMI.get_output_item_count(m::Model) = 2
# Variable information functions
function BMI.get_var_grid(m::Model, name)
  if name == "missing"
    throw(ArgumentError("Variable not found"))
  end
  return 1
end
BMI.get_var_type(m::Model, name) = "Float64"
BMI.get_var_units(m::Model, name) = "unit1"
BMI.get_var_itemsize(m::Model, name) = 8
BMI.get_var_nbytes(m::Model, name) = 32
BMI.get_var_location(m::Model, name) = "node"
# Time functions
BMI.get_current_time(m::Model) = m.current
BMI.get_start_time(m::Model) = 0
BMI.get_end_time(m::Model) = 168
BMI.get_time_step(m::Model) = 1
BMI.get_time_units(m::Model) = "h"
# Variable getter and setter functions
function BMI.get_value(m::Model, name::String, dest::Vector{T}) where {T <: AbstractFloat}
  copyto!(dest, m.values)
end
function BMI.get_value_at_indices(
  m::Model,
  name::String,
  dest::Vector{T},
  indices::Vector{Int},
) where {T <: AbstractFloat}
  copyto!(dest, m.values[indices])
end
function BMI.set_value(m::Model, name::String, src::Vector{T}) where {T <: AbstractFloat}
  copyto!(m.values, src)
  return nothing
end
function BMI.set_value_at_indices(
  m::Model,
  name::String,
  indices::Vector{Int},
  src::Vector{T},
) where {T <: AbstractFloat}
  m.values[indices] .= src
  return nothing
end
# Model grid functions
BMI.get_grid_type(m::Model, grid) = "uniform_rectilinear"
BMI.get_grid_size(m::Model, grid) = 4
BMI.get_grid_rank(m::Model, grid) = 3
BMI.get_grid_shape(m::Model, grid) = Int[2, 3, 4]
function BMI.get_grid_spacing(m::Model, grid, spacing::Vector{T}) where {T <: AbstractFloat}
  copyto!(spacing, [0.1, 1.1, 2.1])
end
function BMI.get_grid_origin(m::Model, grid, origin::Vector{T}) where {T <: AbstractFloat}
  copyto!(origin, [0.1, 0.2, 0.3])
end
function BMI.get_grid_x(m::Model, grid, x::Vector{T}) where {T <: AbstractFloat}
  copyto!(x, [0.1, 0.2, 0.3, 0.4])
end
function BMI.get_grid_y(m::Model, grid, y::Vector{T}) where {T <: AbstractFloat}
  copyto!(y, [1.1, 1.2, 1.3])
end
function BMI.get_grid_z(m::Model, grid, z::Vector{T}) where {T <: AbstractFloat}
  copyto!(z, [2.1, 2.2])
end
BMI.get_grid_node_count(m::Model, grid) = 6
BMI.get_grid_edge_count(m::Model, grid) = 8
BMI.get_grid_face_count(m::Model, grid) = 3
BMI.get_grid_edge_nodes(m::Model, grid, edge_nodes::Vector{Int}) =
  copyto!(edge_nodes, Int[0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3])
BMI.get_grid_face_edges(m::Model, grid, face_edges::Vector{Int}) =
  copyto!(face_edges, Int[0, 1, 2, 3, 4, 5, 6, 1, 6, 7, 2])
BMI.get_grid_face_nodes(m::Model, grid, face_nodes::Vector{Int}) =
  copyto!(face_nodes, Int[0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3])
BMI.get_grid_nodes_per_face(m::Model, grid, nodes_per_face::Vector{Int}) =
  copyto!(nodes_per_face, Int[4, 4, 3])
end # FakeModel module
