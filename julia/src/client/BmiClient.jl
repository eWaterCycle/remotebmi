# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

module BmiClient

using TimeZones
using OpenAPI
using OpenAPI.Clients

const API_VERSION = "2.0"

include("modelincludes.jl")

include("apis/api_ExchangeItemsApi.jl")
include("apis/api_GettersApi.jl")
include("apis/api_GridInformationApi.jl")
include("apis/api_IRFApi.jl")
include("apis/api_NURCApi.jl")
include("apis/api_SettersApi.jl")
include("apis/api_TimeInformationApi.jl")
include("apis/api_UniformRectilinearApi.jl")
include("apis/api_UnstructuredApi.jl")
include("apis/api_VariableInformationApi.jl")

# export models
export GetComponentNameResponse
export GetGridTypeResponse
export GetTimeUnitsResponse
export GetVarLocationResponseLocation
export GetVarTypeResponse
export GetVarUnitsResponse
export InitializeRequest
export ProblemDetails
export SetValueAtIndicesRequest

# export operations
export ExchangeItemsApi
export GettersApi
export GridInformationApi
export IRFApi
export NURCApi
export SettersApi
export TimeInformationApi
export UniformRectilinearApi
export UnstructuredApi
export VariableInformationApi

end # module BmiClient
