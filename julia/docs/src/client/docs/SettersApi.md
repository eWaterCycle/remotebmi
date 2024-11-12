# SettersApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**set_value**](SettersApi.md#set_value) | **POST** /set_value/{name} | 
[**set_value_at_indices**](SettersApi.md#set_value_at_indices) | **POST** /set_value_at_indices/{name} | 


# **set_value**
> set_value(_api::SettersApi, name::String, request_body::Vector{Float64}; _mediaType=nothing) -> Nothing, OpenAPI.Clients.ApiResponse <br/>
> set_value(_api::SettersApi, response_stream::Channel, name::String, request_body::Vector{Float64}; _mediaType=nothing) -> Channel{ Nothing }, OpenAPI.Clients.ApiResponse



Set the value of a variable.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SettersApi** | API context | 
**name** | **String**|  | [default to nothing]
**request_body** | [**Vector{Float64}**](Float64.md)|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **set_value_at_indices**
> set_value_at_indices(_api::SettersApi, name::String, set_value_at_indices_request::SetValueAtIndicesRequest; _mediaType=nothing) -> Nothing, OpenAPI.Clients.ApiResponse <br/>
> set_value_at_indices(_api::SettersApi, response_stream::Channel, name::String, set_value_at_indices_request::SetValueAtIndicesRequest; _mediaType=nothing) -> Channel{ Nothing }, OpenAPI.Clients.ApiResponse



Set the value of a variable at specific indices.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **SettersApi** | API context | 
**name** | **String**|  | [default to nothing]
**set_value_at_indices_request** | [**SetValueAtIndicesRequest**](SetValueAtIndicesRequest.md)|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

