# IEEEDoubleNoNaN

Represents a finite JSON number or one of the non-finite IEEE string symbols
`"Infinity"` and `"-Infinity"`, as defined in `openapi.yaml`.

## Properties

Name | Type | Description
------------ | ------------- | -------------
**value** | `Union{Float64, String}` | A finite number or an allowed string symbol.

Construct with `IEEEDoubleNoNaN(value)`. Booleans, invalid strings, and numeric
non-finite values are rejected. Encode non-finite values as the allowed strings.
`"NaN"` is rejected; this type is used for model times and time steps.

[[Back to Model list]](../README.md#models) [[Back to API list]](../README.md#api-endpoints) [[Back to README]](../README.md)
