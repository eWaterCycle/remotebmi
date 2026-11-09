module NonFinite

"""Encode a number using the non-finite strings defined in openapi.yaml."""
function encode(value::Real)
  isnan(value) && return "NaN"
  return isinf(value) ? (value > 0 ? "Infinity" : "-Infinity") : value
end

"""Decode an IEEENumber / IEEEDouble value, preserving finite numbers."""
decode(value::Real) = value
function decode(value::String)
  value == "NaN" && return NaN
  value == "Infinity" && return Inf
  value == "-Infinity" && return -Inf
  throw(ArgumentError("Invalid IEEE number: $value"))
end

end
