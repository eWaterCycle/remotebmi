# Julia API server for BmiServer

OpenAPI specification for the Basic Modeling Interface (BMI). All functions are described on the [BMI homepage](https://bmi.readthedocs.io/).


## Overview
This API server was generated by the [OpenAPI Generator](https://openapi-generator.tech) project.  By using the [openapi-spec](https://openapis.org) from a remote server, you can easily generate an API client.

- API version: 2.0
- Generator version: 7.9.0
- Build package: org.openapitools.codegen.languages.JuliaServerCodegen
For more information, please visit [https://www.ewatercycle.org/contact/](https://www.ewatercycle.org/contact/)


## Installation
Place the Julia files generated under the `src` folder in your Julia project. Include BmiServer.jl in the project code.
It would include the module named BmiServer.

Implement the server methods as listed below. They are also documented with the BmiServer module.
Launch a HTTP server with a router that has all handlers registered. A `register` method is provided in BmiServer module for convenience.

```julia
register(
    router::HTTP.Router,        # Router to register handlers in
    impl;                       # Module that implements the server methods
    path_prefix::String="",     # Prefix to be applied to all paths
    optional_middlewares...     # Optional middlewares to be applied to all handlers
)
```

Optional middlewares can be one or more of:
- `init`: called before the request is processed
- `pre_validation`: called after the request is parsed but before validation
- `pre_invoke`: called after validation but before the handler is invoked
- `post_invoke`: called after the handler is invoked but before the response is sent

The order in which middlewares are invoked are:
`init |> read |> pre_validation |> validate |> pre_invoke |> invoke |> post_invoke`


## API Endpoints

The following server methods must be implemented:

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ExchangeItemsApi* | [**get_component_name**](docs/ExchangeItemsApi.md#get_component_name) | **GET** /get_component_name | 
*ExchangeItemsApi* | [**get_input_item_count**](docs/ExchangeItemsApi.md#get_input_item_count) | **GET** /get_input_item_count | 
*ExchangeItemsApi* | [**get_input_var_names**](docs/ExchangeItemsApi.md#get_input_var_names) | **GET** /get_input_var_names | 
*ExchangeItemsApi* | [**get_output_item_count**](docs/ExchangeItemsApi.md#get_output_item_count) | **GET** /get_output_item_count | 
*ExchangeItemsApi* | [**get_output_var_names**](docs/ExchangeItemsApi.md#get_output_var_names) | **GET** /get_output_var_names | 
*GettersApi* | [**get_value**](docs/GettersApi.md#get_value) | **GET** /get_value/{name} | 
*GettersApi* | [**get_value_at_indices**](docs/GettersApi.md#get_value_at_indices) | **POST** /get_value_at_indices/{name} | 
*GridInformationApi* | [**get_grid_rank**](docs/GridInformationApi.md#get_grid_rank) | **GET** /get_grid_rank/{grid} | 
*GridInformationApi* | [**get_grid_size**](docs/GridInformationApi.md#get_grid_size) | **GET** /get_grid_size/{grid} | 
*GridInformationApi* | [**get_grid_type**](docs/GridInformationApi.md#get_grid_type) | **GET** /get_grid_type/{grid} | 
*IRFApi* | [**finalize**](docs/IRFApi.md#finalize) | **DELETE** /finalize | 
*IRFApi* | [**initialize**](docs/IRFApi.md#initialize) | **POST** /initialize | 
*IRFApi* | [**update**](docs/IRFApi.md#update) | **POST** /update | 
*IRFApi* | [**update_until**](docs/IRFApi.md#update_until) | **POST** /update_until | 
*NURCApi* | [**get_grid_x**](docs/NURCApi.md#get_grid_x) | **GET** /get_grid_x/{grid} | 
*NURCApi* | [**get_grid_y**](docs/NURCApi.md#get_grid_y) | **GET** /get_grid_y/{grid} | 
*NURCApi* | [**get_grid_z**](docs/NURCApi.md#get_grid_z) | **GET** /get_grid_z/{grid} | 
*SettersApi* | [**set_value**](docs/SettersApi.md#set_value) | **POST** /set_value/{name} | 
*SettersApi* | [**set_value_at_indices**](docs/SettersApi.md#set_value_at_indices) | **POST** /set_value_at_indices/{name} | 
*TimeInformationApi* | [**get_current_time**](docs/TimeInformationApi.md#get_current_time) | **GET** /get_current_time | 
*TimeInformationApi* | [**get_end_time**](docs/TimeInformationApi.md#get_end_time) | **GET** /get_end_time | 
*TimeInformationApi* | [**get_start_time**](docs/TimeInformationApi.md#get_start_time) | **GET** /get_start_time | 
*TimeInformationApi* | [**get_time_step**](docs/TimeInformationApi.md#get_time_step) | **GET** /get_time_step | 
*TimeInformationApi* | [**get_time_units**](docs/TimeInformationApi.md#get_time_units) | **GET** /get_time_units | 
*UniformRectilinearApi* | [**get_grid_origin**](docs/UniformRectilinearApi.md#get_grid_origin) | **GET** /get_grid_origin/{grid} | 
*UniformRectilinearApi* | [**get_grid_shape**](docs/UniformRectilinearApi.md#get_grid_shape) | **GET** /get_grid_shape/{grid} | 
*UniformRectilinearApi* | [**get_grid_spacing**](docs/UniformRectilinearApi.md#get_grid_spacing) | **GET** /get_grid_spacing/{grid} | 
*UnstructuredApi* | [**get_grid_edge_count**](docs/UnstructuredApi.md#get_grid_edge_count) | **GET** /get_grid_edge_count/{grid} | 
*UnstructuredApi* | [**get_grid_edge_nodes**](docs/UnstructuredApi.md#get_grid_edge_nodes) | **GET** /get_grid_edge_nodes/{grid} | 
*UnstructuredApi* | [**get_grid_face_count**](docs/UnstructuredApi.md#get_grid_face_count) | **GET** /get_grid_face_count/{grid} | 
*UnstructuredApi* | [**get_grid_face_edges**](docs/UnstructuredApi.md#get_grid_face_edges) | **GET** /get_grid_face_edges/{grid} | 
*UnstructuredApi* | [**get_grid_face_nodes**](docs/UnstructuredApi.md#get_grid_face_nodes) | **GET** /get_grid_face_nodes/{grid} | 
*UnstructuredApi* | [**get_grid_node_count**](docs/UnstructuredApi.md#get_grid_node_count) | **GET** /get_grid_node_count/{grid} | 
*UnstructuredApi* | [**get_grid_nodes_per_face**](docs/UnstructuredApi.md#get_grid_nodes_per_face) | **GET** /get_grid_nodes_per_face/{grid} | 
*VariableInformationApi* | [**get_var_grid**](docs/VariableInformationApi.md#get_var_grid) | **GET** /get_var_grid/{name} | 
*VariableInformationApi* | [**get_var_itemsize**](docs/VariableInformationApi.md#get_var_itemsize) | **GET** /get_var_itemsize/{name} | 
*VariableInformationApi* | [**get_var_location**](docs/VariableInformationApi.md#get_var_location) | **GET** /get_var_location/{name} | 
*VariableInformationApi* | [**get_var_nbytes**](docs/VariableInformationApi.md#get_var_nbytes) | **GET** /get_var_nbytes/{name} | 
*VariableInformationApi* | [**get_var_type**](docs/VariableInformationApi.md#get_var_type) | **GET** /get_var_type/{name} | 
*VariableInformationApi* | [**get_var_units**](docs/VariableInformationApi.md#get_var_units) | **GET** /get_var_units/{name} | 



## Models

 - [GetComponentNameResponse](docs/GetComponentNameResponse.md)
 - [GetGridTypeResponse](docs/GetGridTypeResponse.md)
 - [GetTimeUnitsResponse](docs/GetTimeUnitsResponse.md)
 - [GetVarLocationResponseLocation](docs/GetVarLocationResponseLocation.md)
 - [GetVarTypeResponse](docs/GetVarTypeResponse.md)
 - [GetVarUnitsResponse](docs/GetVarUnitsResponse.md)
 - [InitializeRequest](docs/InitializeRequest.md)
 - [ProblemDetails](docs/ProblemDetails.md)
 - [SetValueAtIndicesRequest](docs/SetValueAtIndicesRequest.md)



## Author



