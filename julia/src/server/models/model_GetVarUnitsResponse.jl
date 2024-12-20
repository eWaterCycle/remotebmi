# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

@doc raw"""GetVarUnitsResponse

    GetVarUnitsResponse(;
        units=nothing,
    )

    - units::String
"""
Base.@kwdef mutable struct GetVarUnitsResponse <: OpenAPI.APIModel
  units::Union{Nothing, String} = nothing

  function GetVarUnitsResponse(units)
    OpenAPI.validate_property(GetVarUnitsResponse, Symbol("units"), units)
    return new(units)
  end
end # type GetVarUnitsResponse

const _property_types_GetVarUnitsResponse = Dict{Symbol, String}(Symbol("units") => "String")
OpenAPI.property_type(::Type{GetVarUnitsResponse}, name::Symbol) =
  Union{Nothing, eval(Base.Meta.parse(_property_types_GetVarUnitsResponse[name]))}

function check_required(o::GetVarUnitsResponse)
  o.units === nothing && (return false)
  true
end

function OpenAPI.validate_property(::Type{GetVarUnitsResponse}, name::Symbol, val)
  if name === Symbol("units")
    OpenAPI.validate_param(name, "GetVarUnitsResponse", :minLength, val, 1)
  end
end
