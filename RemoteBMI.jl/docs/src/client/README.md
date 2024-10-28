# Julia API client for BmiClient

OpenAPI specification for the Basic Modeling Interface (BMI). All functions are described on the [BMI homepage](https://bmi.readthedocs.io/).


## Overview
This API client was generated by the [OpenAPI Generator](https://openapi-generator.tech) project.  By using the [openapi-spec](https://openapis.org) from a remote server, you can easily generate an API client.

- API version: 2.0
- Generator version: 7.9.0
- Build package: org.openapitools.codegen.languages.JuliaClientCodegen
For more information, please visit [https://www.ewatercycle.org/contact/](https://www.ewatercycle.org/contact/)


## Installation
Place the Julia files generated under the `src` folder in your Julia project. Include BmiClient.jl in the project code.
It would include the module named BmiClient.

Documentation is generated as markdown files under the `docs` folder. You can include them in your project documentation.
Documentation is also embedded in Julia which can be used with a Julia specific documentation generator.

## API Endpoints

Class | Method
------------ | -------------
*ExchangeItemsApi* | [**get_component_name**](docs/ExchangeItemsApi.md#get_component_name)<br/>**GET** /get_component_name<br/>
*ExchangeItemsApi* | [**get_input_item_count**](docs/ExchangeItemsApi.md#get_input_item_count)<br/>**GET** /get_input_item_count<br/>
*ExchangeItemsApi* | [**get_input_var_names**](docs/ExchangeItemsApi.md#get_input_var_names)<br/>**GET** /get_input_var_names<br/>
*ExchangeItemsApi* | [**get_output_item_count**](docs/ExchangeItemsApi.md#get_output_item_count)<br/>**GET** /get_output_item_count<br/>
*ExchangeItemsApi* | [**get_output_var_names**](docs/ExchangeItemsApi.md#get_output_var_names)<br/>**GET** /get_output_var_names<br/>
*GettersApi* | [**get_value**](docs/GettersApi.md#get_value)<br/>**GET** /get_value/{name}<br/>
*GettersApi* | [**get_value_at_indices**](docs/GettersApi.md#get_value_at_indices)<br/>**POST** /get_value_at_indices/{name}<br/>
*GridInformationApi* | [**get_grid_rank**](docs/GridInformationApi.md#get_grid_rank)<br/>**GET** /get_grid_rank/{grid}<br/>
*GridInformationApi* | [**get_grid_size**](docs/GridInformationApi.md#get_grid_size)<br/>**GET** /get_grid_size/{grid}<br/>
*GridInformationApi* | [**get_grid_type**](docs/GridInformationApi.md#get_grid_type)<br/>**GET** /get_grid_type/{grid}<br/>
*IRFApi* | [**finalize**](docs/IRFApi.md#finalize)<br/>**DELETE** /finalize<br/>
*IRFApi* | [**initialize**](docs/IRFApi.md#initialize)<br/>**POST** /initialize<br/>
*IRFApi* | [**update**](docs/IRFApi.md#update)<br/>**POST** /update<br/>
*IRFApi* | [**update_until**](docs/IRFApi.md#update_until)<br/>**POST** /update_until<br/>
*NURCApi* | [**get_grid_x**](docs/NURCApi.md#get_grid_x)<br/>**GET** /get_grid_x/{grid}<br/>
*NURCApi* | [**get_grid_y**](docs/NURCApi.md#get_grid_y)<br/>**GET** /get_grid_y/{grid}<br/>
*NURCApi* | [**get_grid_z**](docs/NURCApi.md#get_grid_z)<br/>**GET** /get_grid_z/{grid}<br/>
*SettersApi* | [**set_value**](docs/SettersApi.md#set_value)<br/>**POST** /set_value/{name}<br/>
*SettersApi* | [**set_value_at_indices**](docs/SettersApi.md#set_value_at_indices)<br/>**POST** /set_value_at_indices/{name}<br/>
*TimeInformationApi* | [**get_current_time**](docs/TimeInformationApi.md#get_current_time)<br/>**GET** /get_current_time<br/>
*TimeInformationApi* | [**get_end_time**](docs/TimeInformationApi.md#get_end_time)<br/>**GET** /get_end_time<br/>
*TimeInformationApi* | [**get_start_time**](docs/TimeInformationApi.md#get_start_time)<br/>**GET** /get_start_time<br/>
*TimeInformationApi* | [**get_time_step**](docs/TimeInformationApi.md#get_time_step)<br/>**GET** /get_time_step<br/>
*TimeInformationApi* | [**get_time_units**](docs/TimeInformationApi.md#get_time_units)<br/>**GET** /get_time_units<br/>
*UniformRectilinearApi* | [**get_grid_origin**](docs/UniformRectilinearApi.md#get_grid_origin)<br/>**GET** /get_grid_origin/{grid}<br/>
*UniformRectilinearApi* | [**get_grid_shape**](docs/UniformRectilinearApi.md#get_grid_shape)<br/>**GET** /get_grid_shape/{grid}<br/>
*UniformRectilinearApi* | [**get_grid_spacing**](docs/UniformRectilinearApi.md#get_grid_spacing)<br/>**GET** /get_grid_spacing/{grid}<br/>
*UnstructuredApi* | [**get_grid_edge_count**](docs/UnstructuredApi.md#get_grid_edge_count)<br/>**GET** /get_grid_edge_count/{grid}<br/>
*UnstructuredApi* | [**get_grid_edge_nodes**](docs/UnstructuredApi.md#get_grid_edge_nodes)<br/>**GET** /get_grid_edge_nodes/{grid}<br/>
*UnstructuredApi* | [**get_grid_face_count**](docs/UnstructuredApi.md#get_grid_face_count)<br/>**GET** /get_grid_face_count/{grid}<br/>
*UnstructuredApi* | [**get_grid_face_edges**](docs/UnstructuredApi.md#get_grid_face_edges)<br/>**GET** /get_grid_face_edges/{grid}<br/>
*UnstructuredApi* | [**get_grid_face_nodes**](docs/UnstructuredApi.md#get_grid_face_nodes)<br/>**GET** /get_grid_face_nodes/{grid}<br/>
*UnstructuredApi* | [**get_grid_node_count**](docs/UnstructuredApi.md#get_grid_node_count)<br/>**GET** /get_grid_node_count/{grid}<br/>
*UnstructuredApi* | [**get_grid_nodes_per_face**](docs/UnstructuredApi.md#get_grid_nodes_per_face)<br/>**GET** /get_grid_nodes_per_face/{grid}<br/>
*VariableInformationApi* | [**get_var_grid**](docs/VariableInformationApi.md#get_var_grid)<br/>**GET** /get_var_grid/{name}<br/>
*VariableInformationApi* | [**get_var_itemsize**](docs/VariableInformationApi.md#get_var_itemsize)<br/>**GET** /get_var_itemsize/{name}<br/>
*VariableInformationApi* | [**get_var_location**](docs/VariableInformationApi.md#get_var_location)<br/>**GET** /get_var_location/{name}<br/>
*VariableInformationApi* | [**get_var_nbytes**](docs/VariableInformationApi.md#get_var_nbytes)<br/>**GET** /get_var_nbytes/{name}<br/>
*VariableInformationApi* | [**get_var_type**](docs/VariableInformationApi.md#get_var_type)<br/>**GET** /get_var_type/{name}<br/>
*VariableInformationApi* | [**get_var_units**](docs/VariableInformationApi.md#get_var_units)<br/>**GET** /get_var_units/{name}<br/>


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


<a id="authorization"></a>
## Authorization
Endpoints do not require authorization.


## Author


