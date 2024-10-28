# GettersApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_value**](GettersApi.md#get_value) | **GET** /get_value/{name} | 
[**get_value_at_indices**](GettersApi.md#get_value_at_indices) | **POST** /get_value_at_indices/{name} | 


# **get_value**
> get_value(_api::GettersApi, name::String; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_value(_api::GettersApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the value of a variable.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **GettersApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_value_at_indices**
> get_value_at_indices(_api::GettersApi, name::String, request_body::Vector{Int64}; _mediaType=nothing) -> Vector{Float64}, OpenAPI.Clients.ApiResponse <br/>
> get_value_at_indices(_api::GettersApi, response_stream::Channel, name::String, request_body::Vector{Int64}; _mediaType=nothing) -> Channel{ Vector{Float64} }, OpenAPI.Clients.ApiResponse



Get the value of a variable at specific indices.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **GettersApi** | API context | 
**name** | **String**|  | [default to nothing]
**request_body** | [**Vector{Int64}**](Int64.md)|  | 

### Return type

**Vector{Float64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

