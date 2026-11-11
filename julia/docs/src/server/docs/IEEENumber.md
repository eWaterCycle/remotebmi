# IEEENumber

Represents a finite JSON number or one of the non-finite IEEE string symbols
`"NaN"`, `"Infinity"`, and `"-Infinity"`, as defined in `openapi.yaml`.

## Properties

Name | Type | Description
------------ | ------------- | -------------
**value** | `Union{Real, String}` | A finite number or an allowed string symbol.

Construct with `IEEENumber(value)`. Booleans, invalid strings, and numeric
non-finite values are rejected. Encode non-finite values as the allowed strings.
Finite integers retain their precision.

[[Back to Model list]](../README.md#models) [[Back to API list]](../README.md#api-endpoints) [[Back to README]](../README.md)
