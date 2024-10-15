module FakeModel

import BasicModelInterface as BMI

Base.@kwdef mutable struct Model
end

BMI.initialize(::Type{Model}, config_file) = Model()

BMI.get_component_name(m::Model) = "FakeModel"
BMI.get_grid_type(m::Model, grid) = "uniform_rectilinear"
BMI.get_grid_shape(m::Model, grid) = [2, 3, 4]
BMI.get_grid_rank(m::Model, grid) = 24

function BMI.get_grid_x(m::Model, grid, x::Vector{T}) where {T<:AbstractFloat}
    copyto!(x, [0.1, 0.2, 0.3, 0.4])
end


end # FakeModel module