module Client

using HTTP
using JSON
using OpenAPI
include("modelincludes.jl")

# TODO generate http client with openapi generator

import BasicModelInterface as BMI

Base.@kwdef mutable struct ClientModel
    base_url::String
end

# TODO can we get rid of this? Or rename it?
function setup(base_url::String)
    return ClientModel(base_url)
end

# in https://github.com/csdms/bmi-example-julia/blob/b5d963e6bf864f5d42769e6cc0814dd7bffc9264/src/bmi.jl#L5
# and https://github.com/Deltares/Wflow.jl/blob/788eaad5848e4e02d5357a7c17df363fcfd7d7b7/src/bmi.jl#L23
# the initialize first argument is a class not an instance
# here we use an instance that has be setup with the base_url
# TODO is this ok? Could move base_url arg here, but will need other args like timeouts.
function BMI.initialize(m::ClientModel, config_file::String)
    url = m.base_url * "/initialize"
    HTTP.post(
        url,
        ["Content-Type" => "application/json"],
        json(InitializeRequest(config_file))
    )
    return m
end

function BMI.get_component_name(m::ClientModel)
    url = m.base_url * "/get_component_name"
    response = HTTP.get(url)
    return JSON.parse(String(response.body))["name"]
end

function BMI.get_grid_type(m::ClientModel, grid)
    url = m.base_url * "/get_grid_type/$grid"
    response = HTTP.get(url)
    return JSON.parse(String(response.body))["type"]
end

function BMI.get_grid_shape(m::ClientModel, grid)
    url = m.base_url * "/get_grid_shape/$grid"
    response = HTTP.get(url)
    return JSON.parse(String(response.body))
end

function BMI.get_grid_rank(m::ClientModel, grid)
    url = m.base_url * "/get_grid_rank/$grid"
    response = HTTP.get(url)
    return JSON.parse(String(response.body))
end

function BMI.get_grid_x(m::ClientModel, grid, x::Vector{T}) where {T<:AbstractFloat}
    url = m.base_url * "/get_grid_x/$grid"
    raw_response = HTTP.get(url)
    response = JSON.parse(String(raw_response.body))
    copyto!(x, response)
    return x
end

end
