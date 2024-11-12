# IRFApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**finalize**](IRFApi.md#finalize) | **DELETE** /finalize | 
[**initialize**](IRFApi.md#initialize) | **POST** /initialize | 
[**update**](IRFApi.md#update) | **POST** /update | 
[**update_until**](IRFApi.md#update_until) | **POST** /update_until | 


# **finalize**
> finalize(req::HTTP.Request;) -> Nothing



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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **initialize**
> initialize(req::HTTP.Request, initialize_request::InitializeRequest;) -> Nothing



Performs all tasks that are to take place before entering the model’s time loop. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**initialize_request** | [**InitializeRequest**](InitializeRequest.md)|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> update(req::HTTP.Request;) -> Nothing



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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_until**
> update_until(req::HTTP.Request, body::Float64;) -> Nothing



Updates the model to a particular time

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**body** | **Float64**|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

