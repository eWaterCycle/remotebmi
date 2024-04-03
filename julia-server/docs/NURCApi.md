# NURCApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_x**](NURCApi.md#get_grid_x) | **GET** /get_grid_x/{grid} | 
[**get_grid_y**](NURCApi.md#get_grid_y) | **GET** /get_grid_y/{grid} | 
[**get_grid_z**](NURCApi.md#get_grid_z) | **GET** /get_grid_z/{grid} | 


# **get_grid_x**
> get_grid_x(req::HTTP.Request, grid::Int64;) -> Vector{Float64}



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

# **get_grid_y**
> get_grid_y(req::HTTP.Request, grid::Int64;) -> Vector{Float64}



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

# **get_grid_z**
> get_grid_z(req::HTTP.Request, grid::Int64;) -> Vector{Float64}



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

