# TODOs

## Naming of open api paths

Should getters have `get_` in path?

Shorter better? Or 1:1 mapping with BMI methods?

## Multi protocol

Should we support multiple protocols?
1. openapi / rest / http
2. gRPC
3. ZeroMQ

## Python layout

1. server, docker extras aka remotebmi for client and remotebmi[server] for server and client.
2. 2 packages: remotebmi.server + remotebmi.client

## Security

To prevent unwanted calling a BMI web service we should add an API Key and https.

To use https the server should have a self-signed certificate. 
The client should trust that self-signed certificate.

In BmiClientApptainer and BmiClientDocker we should generate a random API Key and pass it to the container using the `BMI_API_KEY` environment variable.

## Container clients

## Julia provider

## R provider

## Simplify components openapi.yaml

Each path has own request/response schema. Could be used for docs, examples, validation.

## Dockerfiles

As example how to build a remotebmi server and a model in a container image.
