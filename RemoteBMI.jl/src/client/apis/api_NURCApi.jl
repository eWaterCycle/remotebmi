# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

struct NURCApi <: OpenAPI.APIClientImpl
  client::OpenAPI.Clients.Client
end

"""
The default API base path for APIs in `NURCApi`.
This can be used to construct the `OpenAPI.Clients.Client` instance.
"""
basepath(::Type{NURCApi}) = "http://localhost:50051"

const _returntypes_get_grid_x_NURCApi = Dict{Regex, Type}(
  Regex("^" * replace("200", "x" => ".") * "\$") => Vector{Float64},
  Regex("^" * replace("0", "x" => ".") * "\$") => ProblemDetails,
)

function _oacinternal_get_grid_x(_api::NURCApi, grid::Int64; _mediaType = nothing)
  _ctx = OpenAPI.Clients.Ctx(
    _api.client,
    "GET",
    _returntypes_get_grid_x_NURCApi,
    "/get_grid_x/{grid}",
    [],
  )
  OpenAPI.Clients.set_param(_ctx.path, "grid", grid)  # type Int64
  OpenAPI.Clients.set_header_accept(_ctx, ["application/json"])
  OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? [] : [_mediaType])
  return _ctx
end

@doc raw"""Get the locations of the grid nodes in the first coordinate direction. 

Params:
- grid::Int64 (required)

Return: Vector{Float64}, OpenAPI.Clients.ApiResponse
"""
function get_grid_x(_api::NURCApi, grid::Int64; _mediaType = nothing)
  _ctx = _oacinternal_get_grid_x(_api, grid; _mediaType = _mediaType)
  return OpenAPI.Clients.exec(_ctx)
end

function get_grid_x(_api::NURCApi, response_stream::Channel, grid::Int64; _mediaType = nothing)
  _ctx = _oacinternal_get_grid_x(_api, grid; _mediaType = _mediaType)
  return OpenAPI.Clients.exec(_ctx, response_stream)
end

const _returntypes_get_grid_y_NURCApi = Dict{Regex, Type}(
  Regex("^" * replace("200", "x" => ".") * "\$") => Vector{Float64},
  Regex("^" * replace("0", "x" => ".") * "\$") => ProblemDetails,
)

function _oacinternal_get_grid_y(_api::NURCApi, grid::Int64; _mediaType = nothing)
  _ctx = OpenAPI.Clients.Ctx(
    _api.client,
    "GET",
    _returntypes_get_grid_y_NURCApi,
    "/get_grid_y/{grid}",
    [],
  )
  OpenAPI.Clients.set_param(_ctx.path, "grid", grid)  # type Int64
  OpenAPI.Clients.set_header_accept(_ctx, ["application/json"])
  OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? [] : [_mediaType])
  return _ctx
end

@doc raw"""Get the locations of the grid nodes in the second coordinate direction. 

Params:
- grid::Int64 (required)

Return: Vector{Float64}, OpenAPI.Clients.ApiResponse
"""
function get_grid_y(_api::NURCApi, grid::Int64; _mediaType = nothing)
  _ctx = _oacinternal_get_grid_y(_api, grid; _mediaType = _mediaType)
  return OpenAPI.Clients.exec(_ctx)
end

function get_grid_y(_api::NURCApi, response_stream::Channel, grid::Int64; _mediaType = nothing)
  _ctx = _oacinternal_get_grid_y(_api, grid; _mediaType = _mediaType)
  return OpenAPI.Clients.exec(_ctx, response_stream)
end

const _returntypes_get_grid_z_NURCApi = Dict{Regex, Type}(
  Regex("^" * replace("200", "x" => ".") * "\$") => Vector{Float64},
  Regex("^" * replace("0", "x" => ".") * "\$") => ProblemDetails,
)

function _oacinternal_get_grid_z(_api::NURCApi, grid::Int64; _mediaType = nothing)
  _ctx = OpenAPI.Clients.Ctx(
    _api.client,
    "GET",
    _returntypes_get_grid_z_NURCApi,
    "/get_grid_z/{grid}",
    [],
  )
  OpenAPI.Clients.set_param(_ctx.path, "grid", grid)  # type Int64
  OpenAPI.Clients.set_header_accept(_ctx, ["application/json"])
  OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? [] : [_mediaType])
  return _ctx
end

@doc raw"""Get the locations of the grid nodes in the third coordinate direction. 

Params:
- grid::Int64 (required)

Return: Vector{Float64}, OpenAPI.Clients.ApiResponse
"""
function get_grid_z(_api::NURCApi, grid::Int64; _mediaType = nothing)
  _ctx = _oacinternal_get_grid_z(_api, grid; _mediaType = _mediaType)
  return OpenAPI.Clients.exec(_ctx)
end

function get_grid_z(_api::NURCApi, response_stream::Channel, grid::Int64; _mediaType = nothing)
  _ctx = _oacinternal_get_grid_z(_api, grid; _mediaType = _mediaType)
  return OpenAPI.Clients.exec(_ctx, response_stream)
end

export get_grid_x
export get_grid_y
export get_grid_z
