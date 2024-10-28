# NURCApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_x**](NURCApi.md#get_grid_x) | **GET** /get_grid_x/{grid} | 
[**get_grid_y**](NURCApi.md#get_grid_y) | **GET** /get_grid_y/{grid} | 
[**get_grid_z**](NURCApi.md#get_grid_z) | **GET** /get_grid_z/{grid} | 


# **get_grid_x**
> get_grid_x(_api::NURCApi, grid::Int64; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_x(_api::NURCApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the locations of the grid nodes in the first coordinate direction. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **NURCApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_y**
> get_grid_y(_api::NURCApi, grid::Int64; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_y(_api::NURCApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the locations of the grid nodes in the second coordinate direction. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **NURCApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_z**
> get_grid_z(_api::NURCApi, grid::Int64; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_z(_api::NURCApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the locations of the grid nodes in the third coordinate direction. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **NURCApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

