# UnstructuredApi

All URIs are relative to *http://localhost:50051*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_grid_edge_count**](UnstructuredApi.md#get_grid_edge_count) | **GET** /get_grid_edge_count/{grid} | 
[**get_grid_edge_nodes**](UnstructuredApi.md#get_grid_edge_nodes) | **GET** /get_grid_edge_nodes/{grid} | 
[**get_grid_face_count**](UnstructuredApi.md#get_grid_face_count) | **GET** /get_grid_face_count/{grid} | 
[**get_grid_face_edges**](UnstructuredApi.md#get_grid_face_edges) | **GET** /get_grid_face_edges/{grid} | 
[**get_grid_face_nodes**](UnstructuredApi.md#get_grid_face_nodes) | **GET** /get_grid_face_nodes/{grid} | 
[**get_grid_node_count**](UnstructuredApi.md#get_grid_node_count) | **GET** /get_grid_node_count/{grid} | 
[**get_grid_nodes_per_face**](UnstructuredApi.md#get_grid_nodes_per_face) | **GET** /get_grid_nodes_per_face/{grid} | 


# **get_grid_edge_count**
> get_grid_edge_count(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_grid_edge_count(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Get the number of edges in the grid.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_edge_nodes**
> get_grid_edge_nodes(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Vector{Int64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_edge_nodes(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Int64} }, OpenAPI.Clients.ApiResponse



Get the edge-node connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_face_count**
> get_grid_face_count(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_grid_face_count(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Get the face-node connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_face_edges**
> get_grid_face_edges(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Vector{Int64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_face_edges(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Int64} }, OpenAPI.Clients.ApiResponse



Get the face-edge connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_face_nodes**
> get_grid_face_nodes(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Vector{Int64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_face_nodes(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Int64} }, OpenAPI.Clients.ApiResponse



Get the face-node connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_node_count**
> get_grid_node_count(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Int64, OpenAPI.Clients.ApiResponse <br/>
> get_grid_node_count(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Int64 }, OpenAPI.Clients.ApiResponse



Get the number of nodes in the grid.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# **get_grid_nodes_per_face**
> get_grid_nodes_per_face(_api::UnstructuredApi, grid::Int64; _mediaType=nothing) -> Vector{Int64}, OpenAPI.Clients.ApiResponse <br/>
> get_grid_nodes_per_face(_api::UnstructuredApi, response_stream::Channel, grid::Int64; _mediaType=nothing) -> Channel{ Vector{Int64} }, OpenAPI.Clients.ApiResponse



Get the number of nodes for each face.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **_api** | **UnstructuredApi** | API context | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

