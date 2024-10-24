# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

@doc raw"""GetComponentNameResponse

    GetComponentNameResponse(;
        name=nothing,
    )

    - name::String
"""
Base.@kwdef mutable struct GetComponentNameResponse <: OpenAPI.APIModel
  name::Union{Nothing, String} = nothing

  function GetComponentNameResponse(name)
    OpenAPI.validate_property(GetComponentNameResponse, Symbol("name"), name)
    return new(name)
  end
end # type GetComponentNameResponse

const _property_types_GetComponentNameResponse = Dict{Symbol, String}(Symbol("name") => "String")
OpenAPI.property_type(::Type{GetComponentNameResponse}, name::Symbol) =
  Union{Nothing, eval(Base.Meta.parse(_property_types_GetComponentNameResponse[name]))}

function check_required(o::GetComponentNameResponse)
  o.name === nothing && (return false)
  true
end

function OpenAPI.validate_property(::Type{GetComponentNameResponse}, name::Symbol, val)
  if name === Symbol("name")
    OpenAPI.validate_param(name, "GetComponentNameResponse", :minLength, val, 1)
  end
end
