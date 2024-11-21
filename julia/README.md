# RemoteBMI

[![Julia test](https://github.com/eWaterCycle/remotebmi/actions/workflows/julia-test.yml/badge.svg)](https://github.com/eWaterCycle/remotebmi/actions/workflows/julia-test.yml)
[![Julia docs](https://github.com/eWaterCycle/remotebmi/actions/workflows/julia-docs.yml/badge.svg)](https://github.com/eWaterCycle/remotebmi/actions/workflows/julia-docs.yml)

<!-- TODO filter on Julia component
[![Coverage](https://codecov.io/gh/eWaterCycle/RemoteBMI/branch/main/graph/badge.svg)](https://codecov.io/gh/eWaterCycle/RemoteBMI)
-->

## Usage

See [example](example/README.md).

## How to Cite

If you use RemoteBMI.jl in your work, please cite using the reference given in [CITATION.cff](https://github.com/eWaterCycle/julia/blob/main/CITATION.cff).

## Contributing

If you want to make contributions of any kind, please first that a look into our [contributing guide directly on GitHub](docs/src/90-contributing.md) or the [contributing page on the website](https://eWaterCycle.github.io/julia/dev/contributing/).

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
# Copy the generated src
cp -r julia-client/src/* julia/src/client/
cp -r julia-server/src/* julia/src/server/
# Copy the generated docs
mkdir -p julia/docs/src/client/ julia/docs/src/server/
cp -r julia-client/docs julia/docs/src/client/docs
cp -r julia-server/docs julia/docs/src/server/
cp julia-client/README.md julia/docs/src/client/
cp julia-server/README.md julia/docs/src/server/
# Correct links
touch julia/docs/src/client/docs/Int64.md
touch julia/docs/src/client/docs/Float64.md
touch julia/docs/src/server/docs/Int64.md
touch julia/docs/src/server/docs/Float64.md
```

