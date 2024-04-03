# UniformRectilinearApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_origin**](UniformRectilinearApi.md#get_grid_origin) | **GET** /get_grid_origin/{grid} | 
[**get_grid_shape**](UniformRectilinearApi.md#get_grid_shape) | **GET** /get_grid_shape/{grid} | 
[**get_grid_spacing**](UniformRectilinearApi.md#get_grid_spacing) | **GET** /get_grid_spacing/{grid} | 


# **get_grid_origin**
> get_grid_origin(req::HTTP.Request, grid::Int64;) -> Vector{Float64}



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_shape**
> get_grid_shape(req::HTTP.Request, grid::Int64;) -> Vector{Int64}



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_spacing**
> get_grid_spacing(req::HTTP.Request, grid::Int64;) -> Vector{Float64}



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

