# RemoteBMI

[![Stable Documentation](https://img.shields.io/badge/docs-stable-blue.svg)](https://eWaterCycle.github.io/RemoteBMI.jl/stable)
[![In development documentation](https://img.shields.io/badge/docs-dev-blue.svg)](https://eWaterCycle.github.io/RemoteBMI.jl/dev)
[![Build Status](https://github.com/eWaterCycle/RemoteBMI.jl/workflows/Test/badge.svg)](https://github.com/eWaterCycle/RemoteBMI.jl/actions)
[![Test workflow status](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Test.yml/badge.svg?branch=main)](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Test.yml?query=branch%3Amain)
[![Lint workflow Status](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Lint.yml/badge.svg?branch=main)](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Lint.yml?query=branch%3Amain)
[![Docs workflow Status](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Docs.yml/badge.svg?branch=main)](https://github.com/eWaterCycle/RemoteBMI.jl/actions/workflows/Docs.yml?query=branch%3Amain)

[![Coverage](https://codecov.io/gh/eWaterCycle/RemoteBMI.jl/branch/main/graph/badge.svg)](https://codecov.io/gh/eWaterCycle/RemoteBMI.jl)
[![DOI](https://zenodo.org/badge/DOI/FIXME)](https://doi.org/FIXME)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

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
npx @openapitools/openapi-generator-cli generate -i ./openapi.yaml  -g julia-server -o julia-server --additional-properties=packageName=BmiServer --additional-properties=exportModels=true
# Copy the generated files to RemoteBMI.jl/src/

# TODO find out why api key is not in the generated code
# At example https://github.com/JuliaComputing/OpenAPI.jl/blob/2d447986b6377a6724ae59380f087c2b270e7795/test/server/openapigenerator_petstore_v3/petstore/src/apis/api_PetApi.jl#L56
# It is given to impl function as second argument
# but in the generated code it is missing
```