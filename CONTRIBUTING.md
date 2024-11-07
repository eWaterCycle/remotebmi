# Contributing

## AI Assistance

The documentation/software code in this repository can and has been partly generated and/or refined using
GitHub CoPilot. All AI-output has been verified for correctness,
accuracy and completeness, adapted where needed, and approved by the author.

## Add another language

A directory of the name of the language should be created in the root of the repository.

- Create a package/library for the language
- Create server CLI so its easy to combine with model code in a container image
- Add a ci workflow for the language
- Optionally generate client and/or server code with an openapi generator

## Specification validation

The [openapi.yaml](openapi.yaml) is in the [OpenAPI v3.0.3](https://swagger.io/specification/) format.

You can validate it with:

```bash
npx @redocly/cli lint openapi.yaml
```
