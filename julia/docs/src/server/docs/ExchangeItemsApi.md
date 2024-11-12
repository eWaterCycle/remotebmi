# ExchangeItemsApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_component_name**](ExchangeItemsApi.md#get_component_name) | **GET** /get_component_name | 
[**get_input_item_count**](ExchangeItemsApi.md#get_input_item_count) | **GET** /get_input_item_count | 
[**get_input_var_names**](ExchangeItemsApi.md#get_input_var_names) | **GET** /get_input_var_names | 
[**get_output_item_count**](ExchangeItemsApi.md#get_output_item_count) | **GET** /get_output_item_count | 
[**get_output_var_names**](ExchangeItemsApi.md#get_output_var_names) | **GET** /get_output_var_names | 


# **get_component_name**
> get_component_name(req::HTTP.Request;) -> GetComponentNameResponse



Get the name of the model component.

### Required Parameters
This endpoint does not need any parameter.

### Return type

[**GetComponentNameResponse**](GetComponentNameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_input_item_count**
> get_input_item_count(req::HTTP.Request;) -> Int64



The number of variables the model can use from other models implementing a BMI. 

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_input_var_names**
> get_input_var_names(req::HTTP.Request;) -> Vector{String}



Gets an array of names for the variables the model can use from other models implementing a BMI. 

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Vector{String}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_output_item_count**
> get_output_item_count(req::HTTP.Request;) -> Int64



The number of variables the model can provide other models implementing a BMI. 

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_output_var_names**
> get_output_var_names(req::HTTP.Request;) -> Vector{String}



Gets an array of names for the variables the model can provide to other models implementing a BMI. 

### Required Parameters
This endpoint does not need any parameter.

### Return type

**Vector{String}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

