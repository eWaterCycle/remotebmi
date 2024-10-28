# GridInformationApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_rank**](GridInformationApi.md#get_grid_rank) | **GET** /get_grid_rank/{grid} | 
[**get_grid_size**](GridInformationApi.md#get_grid_size) | **GET** /get_grid_size/{grid} | 
[**get_grid_type**](GridInformationApi.md#get_grid_type) | **GET** /get_grid_type/{grid} | 


# **get_grid_rank**
> get_grid_rank(_api::GridInformationApi, grid::Int64; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_grid_rank(_api::GridInformationApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Given a grid identifier, get the rank (the number of dimensions) of that grid as an integer. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **GridInformationApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_size**
> get_grid_size(_api::GridInformationApi, grid::Int64; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_grid_size(_api::GridInformationApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Given a grid identifier, get the total number of elements (or nodes) of that grid as an integer. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **GridInformationApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_type**
> get_grid_type(_api::GridInformationApi, grid::Int64; _mediaType=nothing) -> GetGridTypeResponse, OpenAPI.Clients.ApiResponse <br/>
> get_grid_type(_api::GridInformationApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ GetGridTypeResponse }, OpenAPI.Clients.ApiResponse



Given a grid identifier, get the type of that grid as a string. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **GridInformationApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

[**GetGridTypeResponse**](GetGridTypeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

