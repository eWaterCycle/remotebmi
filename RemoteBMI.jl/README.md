# RemoteBMI

<!-- [![Stable Documentation](https://img.shields.io/badge/docs-stable-blue.svg)](https://eWaterCycle.github.io/RemoteBMI.jl/stable) -->
<!-- [![In development documentation](https://img.shields.io/badge/docs-dev-blue.svg)](https://eWaterCycle.github.io/RemoteBMI.jl/dev) -->
[![Build Status](https://github.com/eWaterCycle/RemoteBMI.jl/workflows/Julia%20test/badge.svg)](https://github.com/eWaterCycle/RemoteBMI/actions)
[![Test workflow status](https://github.com/eWaterCycle/RemoteBMI/actions/workflows/julia-test.yml/badge.svg?branch=main)](https://github.com/eWaterCycle/RemoteBMI/actions/workflows/julia-test.yml?query=branch%3Amain)
<!-- [![Docs workflow Status](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Docs.yml/badge.svg?branch=main)](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Docs.yml?query=branch%3Amain) -->

<!-- TODO filter on Julia component
[![Coverage](https://codecov.io/gh/eWaterCycle/RemoteBMI/branch/main/graph/badge.svg)](https://codecov.io/gh/eWaterCycle/RemoteBMI)
-->

## Usage

See [example](example/README.md).

## How to Cite

If you use RemoteBMI.jl in your work, please cite using the reference given in [CITATION.cff](https://github.com/eWaterCycle/RemoteBMI.jl/blob/main/CITATION.cff).

## Contributing

If you want to make contributions of any kind, please first that a look into our [contributing guide directly on GitHub](docs/src/90-contributing.md) or the [contributing page on the website](https://eWaterCycle.github.io/RemoteBMI.jl/dev/contributing/).

## Code generation

The skeleton of the package was generated with

```jula
using BestieTemplate
BestieTemplate.generate("RemoteBMI.jl")
```

The openapi server stubs where generated using the following command:

```shell
wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.9.0/openapi-generator-cli-7.9.0.jar -O openapi-generator-cli.jar
java -jar ./openapi-generator-cli.jar  generate -i ./openapi.yaml  -g julia-server -o julia-server --additional-properties=packageName=BmiServer --additional-properties=exportModels=true
java -jar ./openapi-generator-cli.jar  generate -i ./openapi.yaml  -g julia-client -o julia-client --additional-properties=packageName=BmiClient --additional-properties=exportModels=true

# Copy the generated files to RemoteBMI.jl/src/
```