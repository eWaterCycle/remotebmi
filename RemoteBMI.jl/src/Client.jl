module Client

using HTTP
using JSON
using OpenAPI
import OpenAPI.Clients
include("client/BmiClient.jl")

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
    api = IRFApi(OpenAPI.Clients.Client(m.base_url))
    return api.initialize(InitializeRequest(config_file))
end

function BMI.get_component_name(m::ClientModel)
    api = ExchangeItemsApi(OpenAPI.Clients.Client(m.base_url))
    response = api.get_component_name()
    return response.name
end

function BMI.get_grid_type(m::ClientModel, grid)
    api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
    response = api.get_grid_type(grid)
    return response.type
end

function BMI.get_grid_shape(m::ClientModel, grid)
    api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
    return api.get_grid_shape(grid)
end

function BMI.get_grid_rank(m::ClientModel, grid)
    api = GridInformationApi(OpenAPI.Clients.Client(m.base_url))
    return api.get_grid_rank(grid)
end

function BMI.get_grid_x(m::ClientModel, grid, x::Vector{T}) where {T<:AbstractFloat}
    api = NURCApi(OpenAPI.Clients.Client(m.base_url))
    response = api.get_grid_x(grid)
    copyto!(x, response)
    return x
end

end
