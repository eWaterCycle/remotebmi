# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

struct IRFApi <: OpenAPI.APIClientImpl
    client::OpenAPI.Clients.Client
end

"""
The default API base path for APIs in `IRFApi`.
This can be used to construct the `OpenAPI.Clients.Client` instance.
"""
basepath(::Type{ IRFApi }) = "http://localhost:50051"

const _returntypes_finalize_IRFApi = Dict{Regex,Type}(
    Regex("^" * replace("204", "x"=>".") * "\$") => Nothing,
    Regex("^" * replace("0", "x"=>".") * "\$") => ProblemDetails,
)

function _oacinternal_finalize(_api::IRFApi; _mediaType=nothing)
    _ctx = OpenAPI.Clients.Ctx(_api.client, "DELETE", _returntypes_finalize_IRFApi, "/finalize", [])
    OpenAPI.Clients.set_header_accept(_ctx, ["application/json", ])
    OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? [] : [_mediaType])
    return _ctx
end

@doc raw"""Performs all tasks that take place after exiting the model’s time loop. 

Params:

Return: Nothing, OpenAPI.Clients.ApiResponse
"""
function finalize(_api::IRFApi; _mediaType=nothing)
    _ctx = _oacinternal_finalize(_api; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx)
end

function finalize(_api::IRFApi, response_stream::Channel; _mediaType=nothing)
    _ctx = _oacinternal_finalize(_api; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx, response_stream)
end

const _returntypes_initialize_IRFApi = Dict{Regex,Type}(
    Regex("^" * replace("201", "x"=>".") * "\$") => Nothing,
    Regex("^" * replace("0", "x"=>".") * "\$") => ProblemDetails,
)

function _oacinternal_initialize(_api::IRFApi, initialize_request::InitializeRequest; _mediaType=nothing)
    _ctx = OpenAPI.Clients.Ctx(_api.client, "POST", _returntypes_initialize_IRFApi, "/initialize", [], initialize_request)
    OpenAPI.Clients.set_header_accept(_ctx, ["application/json", ])
    OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? ["application/json", ] : [_mediaType])
    return _ctx
end

@doc raw"""Performs all tasks that are to take place before entering the model’s time loop. 

Params:
- initialize_request::InitializeRequest (required)

Return: Nothing, OpenAPI.Clients.ApiResponse
"""
function initialize(_api::IRFApi, initialize_request::InitializeRequest; _mediaType=nothing)
    _ctx = _oacinternal_initialize(_api, initialize_request; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx)
end

function initialize(_api::IRFApi, response_stream::Channel, initialize_request::InitializeRequest; _mediaType=nothing)
    _ctx = _oacinternal_initialize(_api, initialize_request; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx, response_stream)
end

const _returntypes_update_IRFApi = Dict{Regex,Type}(
    Regex("^" * replace("204", "x"=>".") * "\$") => Nothing,
    Regex("^" * replace("0", "x"=>".") * "\$") => ProblemDetails,
)

function _oacinternal_update(_api::IRFApi; _mediaType=nothing)
    _ctx = OpenAPI.Clients.Ctx(_api.client, "POST", _returntypes_update_IRFApi, "/update", [])
    OpenAPI.Clients.set_header_accept(_ctx, ["application/json", ])
    OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? [] : [_mediaType])
    return _ctx
end

@doc raw"""Advances the model by a single time step.

Params:

Return: Nothing, OpenAPI.Clients.ApiResponse
"""
function update(_api::IRFApi; _mediaType=nothing)
    _ctx = _oacinternal_update(_api; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx)
end

function update(_api::IRFApi, response_stream::Channel; _mediaType=nothing)
    _ctx = _oacinternal_update(_api; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx, response_stream)
end

const _returntypes_update_until_IRFApi = Dict{Regex,Type}(
    Regex("^" * replace("204", "x"=>".") * "\$") => Nothing,
    Regex("^" * replace("0", "x"=>".") * "\$") => ProblemDetails,
)

function _oacinternal_update_until(_api::IRFApi, body::Float64; _mediaType=nothing)
    _ctx = OpenAPI.Clients.Ctx(_api.client, "POST", _returntypes_update_until_IRFApi, "/update_until", [], body)
    OpenAPI.Clients.set_header_accept(_ctx, ["application/json", ])
    OpenAPI.Clients.set_header_content_type(_ctx, (_mediaType === nothing) ? ["application/json", ] : [_mediaType])
    return _ctx
end

@doc raw"""Updates the model to a particular time

Params:
- body::Float64 (required)

Return: Nothing, OpenAPI.Clients.ApiResponse
"""
function update_until(_api::IRFApi, body::Float64; _mediaType=nothing)
    _ctx = _oacinternal_update_until(_api, body; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx)
end

function update_until(_api::IRFApi, response_stream::Channel, body::Float64; _mediaType=nothing)
    _ctx = _oacinternal_update_until(_api, body; _mediaType=_mediaType)
    return OpenAPI.Clients.exec(_ctx, response_stream)
end

export finalize
export initialize
export update
export update_until
