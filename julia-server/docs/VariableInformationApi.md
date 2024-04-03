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
> get_var_grid(req::HTTP.Request, name::String;) -> Int64



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_var_itemsize**
> get_var_itemsize(req::HTTP.Request, name::String;) -> Int64



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_var_location**
> get_var_location(req::HTTP.Request, name::String;) -> GetVarLocationResponseLocation



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

[**GetVarLocationResponseLocation**](GetVarLocationResponseLocation.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_var_nbytes**
> get_var_nbytes(req::HTTP.Request, name::String;) -> Int64



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_var_type**
> get_var_type(req::HTTP.Request, name::String;) -> String



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

**String**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_var_units**
> get_var_units(req::HTTP.Request, name::String;) -> String



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]

### Return type

**String**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

