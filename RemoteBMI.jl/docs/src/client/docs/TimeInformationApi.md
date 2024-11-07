# TimeInformationApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_current_time**](TimeInformationApi.md#get_current_time) | **GET** /get_current_time | 
[**get_end_time**](TimeInformationApi.md#get_end_time) | **GET** /get_end_time | 
[**get_start_time**](TimeInformationApi.md#get_start_time) | **GET** /get_start_time | 
[**get_time_step**](TimeInformationApi.md#get_time_step) | **GET** /get_time_step | 
[**get_time_units**](TimeInformationApi.md#get_time_units) | **GET** /get_time_units | 


# **get_current_time**
> get_current_time(_api::TimeInformationApi; _mediaType=nothing) -> Float64, OpenAPI.Clients.ApiResponse <br/>
> get_current_time(_api::TimeInformationApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Float64 }, OpenAPI.Clients.ApiResponse



The current model time.

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Float64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_end_time**
> get_end_time(_api::TimeInformationApi; _mediaType=nothing) -> Float64, OpenAPI.Clients.ApiResponse <br/>
> get_end_time(_api::TimeInformationApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Float64 }, OpenAPI.Clients.ApiResponse



The end time of the model.

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Float64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_start_time**
> get_start_time(_api::TimeInformationApi; _mediaType=nothing) -> Float64, OpenAPI.Clients.ApiResponse <br/>
> get_start_time(_api::TimeInformationApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Float64 }, OpenAPI.Clients.ApiResponse



The start time of the model.

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Float64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_time_step**
> get_time_step(_api::TimeInformationApi; _mediaType=nothing) -> Float64, OpenAPI.Clients.ApiResponse <br/>
> get_time_step(_api::TimeInformationApi, response_stream::Channel; _mediaType=nothing) -> Channel{ Float64 }, OpenAPI.Clients.ApiResponse



Get the time step used in the model.

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Float64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_time_units**
> get_time_units(_api::TimeInformationApi; _mediaType=nothing) -> GetTimeUnitsResponse, OpenAPI.Clients.ApiResponse <br/>
> get_time_units(_api::TimeInformationApi, response_stream::Channel; _mediaType=nothing) -> Channel{ GetTimeUnitsResponse }, OpenAPI.Clients.ApiResponse



Get the units of time as reported by the model’s BMI. If model has absolute start time, you can use `since` format, see [cfconventions](https://cfconventions.org/cf-conventions/cf-conventions#time-coordinate). 

### Required Parameters
This endpoint does not need any parameter.

### Return type

[**GetTimeUnitsResponse**](GetTimeUnitsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

