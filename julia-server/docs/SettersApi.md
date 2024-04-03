# SettersApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**set_value**](SettersApi.md#set_value) | **POST** /set_value/{name} | 
[**set_value_at_indices**](SettersApi.md#set_value_at_indices) | **POST** /set_value_at_indices/{name} | 


# **set_value**
> set_value(req::HTTP.Request, name::String, request_body::Vector{Float64};) -> Nothing



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]
**request_body** | [**Vector{Float64}**](Float64.md)|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_value_at_indices**
> set_value_at_indices(req::HTTP.Request, name::String, bmi_set_value_at_indices_request::BmiSetValueAtIndicesRequest;) -> Nothing



### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**name** | **String**|  | [default to nothing]
**bmi_set_value_at_indices_request** | [**BmiSetValueAtIndicesRequest**](BmiSetValueAtIndicesRequest.md)|  | 

### Return type

Nothing

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

