# VariableInformationApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_var_grid**](VariableInformationApi.md#get_var_grid) | **GET** /get_var_grid/{name} | 
[**get_var_itemsize**](VariableInformationApi.md#get_var_itemsize) | **GET** /get_var_itemsize/{name} | 
[**get_var_location**](VariableInformationApi.md#get_var_location) | **GET** /get_var_location/{name} | 
[**get_var_nbytes**](VariableInformationApi.md#get_var_nbytes) | **GET** /get_var_nbytes/{name} | 
[**get_var_type**](VariableInformationApi.md#get_var_type) | **GET** /get_var_type/{name} | 
[**get_var_units**](VariableInformationApi.md#get_var_units) | **GET** /get_var_units/{name} | 


# **get_var_grid**
> get_var_grid(_api::VariableInformationApi, name::String; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_var_grid(_api::VariableInformationApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Each input and output variable is defined on a grid. This function returns the grid identifier for a given variable. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **VariableInformationApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_var_itemsize**
> get_var_itemsize(_api::VariableInformationApi, name::String; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_var_itemsize(_api::VariableInformationApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Provides the size, in bytes, of a single element of the variable. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **VariableInformationApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_var_location**
> get_var_location(_api::VariableInformationApi, name::String; _mediaType=nothing) -> GetVarLocationResponseLocation, OpenAPI.Clients.ApiResponse <br/>
> get_var_location(_api::VariableInformationApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ GetVarLocationResponseLocation }, OpenAPI.Clients.ApiResponse



Indicates on what grid element the variable is defined.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **VariableInformationApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

[**GetVarLocationResponseLocation**](GetVarLocationResponseLocation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_var_nbytes**
> get_var_nbytes(_api::VariableInformationApi, name::String; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_var_nbytes(_api::VariableInformationApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Provides the total amount of memory used to store a variable; i.e., the number of items multiplied by the size of each item. 

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **VariableInformationApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_var_type**
> get_var_type(_api::VariableInformationApi, name::String; _mediaType=nothing) -> GetVarTypeResponse, OpenAPI.Clients.ApiResponse <br/>
> get_var_type(_api::VariableInformationApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ GetVarTypeResponse }, OpenAPI.Clients.ApiResponse



Provides the data type of the variable.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **VariableInformationApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

[**GetVarTypeResponse**](GetVarTypeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_var_units**
> get_var_units(_api::VariableInformationApi, name::String; _mediaType=nothing) -> GetVarUnitsResponse, OpenAPI.Clients.ApiResponse <br/>
> get_var_units(_api::VariableInformationApi, response_stream::Channel, name::String; _mediaType=nothing) -> Channel{ GetVarUnitsResponse }, OpenAPI.Clients.ApiResponse



Get the units of the given variable.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **VariableInformationApi** | API context | 
**name** | **String**|  | [default to nothing]

### Return type

[**GetVarUnitsResponse**](GetVarUnitsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

