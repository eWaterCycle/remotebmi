# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.


@doc raw"""ProblemDetails

    ProblemDetails(;
        type=nothing,
        title=nothing,
        status=nothing,
        detail=nothing,
        instance=nothing,
    )

    - type::String
    - title::String
    - status::Int64
    - detail::String
    - instance::String
"""
Base.@kwdef mutable struct ProblemDetails <: OpenAPI.APIModel
    type::Union{Nothing, String} = nothing
    title::Union{Nothing, String} = nothing
    status::Union{Nothing, Int64} = nothing
    detail::Union{Nothing, String} = nothing
    instance::Union{Nothing, String} = nothing

    function ProblemDetails(type, title, status, detail, instance, )
        OpenAPI.validate_property(ProblemDetails, Symbol("type"), type)
        OpenAPI.validate_property(ProblemDetails, Symbol("title"), title)
        OpenAPI.validate_property(ProblemDetails, Symbol("status"), status)
        OpenAPI.validate_property(ProblemDetails, Symbol("detail"), detail)
        OpenAPI.validate_property(ProblemDetails, Symbol("instance"), instance)
        return new(type, title, status, detail, instance, )
    end
end # type ProblemDetails

const _property_types_ProblemDetails = Dict{Symbol,String}(Symbol("type")=>"String", Symbol("title")=>"String", Symbol("status")=>"Int64", Symbol("detail")=>"String", Symbol("instance")=>"String", )
OpenAPI.property_type(::Type{ ProblemDetails }, name::Symbol) = Union{Nothing,eval(Base.Meta.parse(_property_types_ProblemDetails[name]))}

function check_required(o::ProblemDetails)
    true
end

function OpenAPI.validate_property(::Type{ ProblemDetails }, name::Symbol, val)
end
