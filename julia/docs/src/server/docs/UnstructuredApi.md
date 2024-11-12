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
> get_grid_edge_count(req::HTTP.Request, grid::Int64;) -> Int64



Get the number of edges in the grid.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_edge_nodes**
> get_grid_edge_nodes(req::HTTP.Request, grid::Int64;) -> Vector{Int64}



Get the edge-node connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_face_count**
> get_grid_face_count(req::HTTP.Request, grid::Int64;) -> Int64



Get the face-node connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_face_edges**
> get_grid_face_edges(req::HTTP.Request, grid::Int64;) -> Vector{Int64}



Get the face-edge connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_face_nodes**
> get_grid_face_nodes(req::HTTP.Request, grid::Int64;) -> Vector{Int64}



Get the face-node connectivity.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_node_count**
> get_grid_node_count(req::HTTP.Request, grid::Int64;) -> Int64



Get the number of nodes in the grid.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Int64**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_grid_nodes_per_face**
> get_grid_nodes_per_face(req::HTTP.Request, grid::Int64;) -> Vector{Int64}



Get the number of nodes for each face.

### Required Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **req** | **HTTP.Request** | The HTTP Request object | 
**grid** | **Int64**|  | [default to nothing]

### Return type

**Vector{Int64}**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

