# Basic Model Interface

The [Basic Model Interface (BMI)](https://bmi.readthedocs.io/en/stable/) is a standard interface for models. 
The interface is available in different languages and a [language agnosting version in SIDL](https://github.com/csdms/bmi/blob/stable/bmi.sidl).

BMI was mainly developed to be used inside a programming language, or with direct language-to-language bindings.
However, in some cases you want to communicate with a BMI where:

- language-to-language bindings are complex or not viable (for example, R <-> Julia)
- you want to insulate binary dependencies
- two models don't run on the same version of a language (Python 2 vs. Python 3)
- you want to containerize models

To have a consumer of the model and the provider of the model seperated you can use [grpc4bmi](https://grpc4bmi.readthedocs.io/), but this only works on languages that have a gRPC server and/or client implementation.
The remotebmi project replaces the gRPC protocol with an REST API.
The REST API specification is in the [OpenAPI](openapi.md) format.

## Deviations from the standard BMI

Due to limitations in using a REST API, remotebmi has some minor differences:

- Request body and response body are in JSON format
- On errors you get 4xx and 5xx responses with [Problem Details](https://tools.ietf.org/html/rfc7807) as response body
- Variable names must be URL safe
- Variable type must be in enum.
- get_value_ptr function is not available

