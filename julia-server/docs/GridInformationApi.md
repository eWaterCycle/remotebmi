# GridInformationApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_rank**](GridInformationApi.md#get_grid_rank) | **GET** /get_grid_rank/{grid} | 
[**get_grid_size**](GridInformationApi.md#get_grid_size) | **GET** /get_grid_size/{grid} | 
[**get_grid_type**](GridInformationApi.md#get_grid_type) | **GET** /get_grid_type/{grid} | 


# **get_grid_rank**
> get_grid_rank(req::HTTP.Request, grid::Int64;) -> Int64



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_size**
> get_grid_size(req::HTTP.Request, grid::Int64;) -> Int64



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_type**
> get_grid_type(req::HTTP.Request, grid::Int64;) -> BmiGetGridTypeResponse



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

[**BmiGetGridTypeResponse**](BmiGetGridTypeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

