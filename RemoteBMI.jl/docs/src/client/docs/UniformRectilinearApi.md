# UniformRectilinearApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_origin**](UniformRectilinearApi.md#get_grid_origin) | **GET** /get_grid_origin/{grid} | 
[**get_grid_shape**](UniformRectilinearApi.md#get_grid_shape) | **GET** /get_grid_shape/{grid} | 
[**get_grid_spacing**](UniformRectilinearApi.md#get_grid_spacing) | **GET** /get_grid_spacing/{grid} | 


# **get_grid_origin**
> get_grid_origin(_api::UniformRectilinearApi, grid::Int64; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_origin(_api::UniformRectilinearApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the coordinates of the lower-left corner of the model grid. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UniformRectilinearApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_shape**
> get_grid_shape(_api::UniformRectilinearApi, grid::Int64; _mediaType=nothing) -> Vector{Int64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_shape(_api::UniformRectilinearApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Int64} }, OpenAPI.Clients.ApiResponse



Get the dimensions of the model grid.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UniformRectilinearApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_spacing**
> get_grid_spacing(_api::UniformRectilinearApi, grid::Int64; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_spacing(_api::UniformRectilinearApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the distance between the nodes of the model grid.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UniformRectilinearApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

