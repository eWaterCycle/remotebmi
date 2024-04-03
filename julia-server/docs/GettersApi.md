# GettersApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_value**](GettersApi.md#get_value) | **GET** /get_value/{name} | 
[**get_value_at_indices**](GettersApi.md#get_value_at_indices) | **POST** /get_value_at_indices/{name} | 


# **get_value**
> get_value(req::HTTP.Request, name::String;) -> Vector{Float64}



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_value_at_indices**
> get_value_at_indices(req::HTTP.Request, name::String, request_body::Vector{Int64};) -> Vector{Float64}



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]
**request_body** | [**Vector{Int64}**](Int64.md)|  | 

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

