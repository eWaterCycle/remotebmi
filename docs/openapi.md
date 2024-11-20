# OpenAPI specification

We converted the Basic Model Interface (version 2.0) to an REST API specification in the [OpenAPI format](https://github.com/eWaterCycle/remotebmi/blob/main/openapi.yaml).

You can view the automatically generated [OpenAPI reference documentation here](https://redocly.github.io/redoc/?url=https://github.com/eWaterCycle/remotebmi/raw/main/openapi.yaml)

With OpenAPI you can use the specification to generate both client and server implementations in many different programming languages.
For now these are Python, Julia, and R.

If you are interested in adding implementations in different languages, please [open an issue](https://github.com/eWaterCycle/remotebmi/issues/new/choose). We can point you to the right direction if you need some help in implementing it yourself.

Any language that can run a HTTP server and parse/load JSON can be used as a provider.
