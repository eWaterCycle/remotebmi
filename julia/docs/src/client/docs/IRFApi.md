# IRFApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**finalize**](IRFApi.md#finalize) | **DELETE** /finalize | 
[**initialize**](IRFApi.md#initialize) | **POST** /initialize | 
[**update**](IRFApi.md#update) | **POST** /update | 
[**update_until**](IRFApi.md#update_until) | **POST** /update_until | 


# **finalize**
> finalize(_api::IRFApi; _mediaType=nothing) -> Nothing, OpenAPI.Clients.ApiResponse <br/>
> finalize(_api::IRFApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Nothing }, OpenAPI.Clients.ApiResponse



Performs all tasks that take place after exiting the model’s time loop. 

### Required Parameters
This endpoint does not need any parameter.

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **initialize**
> initialize(_api::IRFApi, initialize_request::InitializeRequest; _mediaType=nothing) -> Nothing, OpenAPI.Clients.ApiResponse <br/>
> initialize(_api::IRFApi, response_stream::Channel, initialize_request::InitializeRequest; _mediaType=nothing) -> Channel{ Nothing }, OpenAPI.Clients.ApiResponse



Performs all tasks that are to take place before entering the model’s time loop. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **IRFApi** | API context | 
**initialize_request** | [**InitializeRequest**](InitializeRequest.md)|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update**
> update(_api::IRFApi; _mediaType=nothing) -> Nothing, OpenAPI.Clients.ApiResponse <br/>
> update(_api::IRFApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Nothing }, OpenAPI.Clients.ApiResponse



Advances the model by a single time step.

### Required Parameters
This endpoint does not need any parameter.

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **update_until**
> update_until(_api::IRFApi, body::Float64; _mediaType=nothing) -> Nothing, OpenAPI.Clients.ApiResponse <br/>
> update_until(_api::IRFApi, response_stream::Channel, body::Float64; _mediaType=nothing) -> Channel{ Nothing }, OpenAPI.Clients.ApiResponse



Updates the model to a particular time

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **IRFApi** | API context | 
**body** | **Float64**|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

