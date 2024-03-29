# Contributing

## Add another language

Each directory inside this repo is formatted as follows `<language>-<consumer|provder>-<grpc|rest>`.

## Specification validation

The [openapi.yaml](openapi.yaml) is in the [OpenAPI v3.0.3](https://swagger.io/specification/) format.

You can validate it with:

```bash
npx @redocly/cli lint openapi.yaml
```
