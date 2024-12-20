# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

function get_grid_rank_read(handler)
  function get_grid_rank_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    path_params = HTTP.getparams(req)
    openapi_params["grid"] = OpenAPI.Servers.to_param(Int64, path_params, "grid"; required = true)
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_grid_rank_validate(handler)
  function get_grid_rank_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_grid_rank_invoke(impl; post_invoke = nothing)
  function get_grid_rank_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_grid_rank(req::HTTP.Request, openapi_params["grid"];)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function get_grid_size_read(handler)
  function get_grid_size_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    path_params = HTTP.getparams(req)
    openapi_params["grid"] = OpenAPI.Servers.to_param(Int64, path_params, "grid"; required = true)
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_grid_size_validate(handler)
  function get_grid_size_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_grid_size_invoke(impl; post_invoke = nothing)
  function get_grid_size_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_grid_size(req::HTTP.Request, openapi_params["grid"];)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function get_grid_type_read(handler)
  function get_grid_type_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    path_params = HTTP.getparams(req)
    openapi_params["grid"] = OpenAPI.Servers.to_param(Int64, path_params, "grid"; required = true)
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_grid_type_validate(handler)
  function get_grid_type_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_grid_type_invoke(impl; post_invoke = nothing)
  function get_grid_type_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_grid_type(req::HTTP.Request, openapi_params["grid"];)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function registerGridInformationApi(
  router::HTTP.Router,
  impl;
  path_prefix::String = "",
  optional_middlewares...,
)
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_grid_rank/{grid}",
    OpenAPI.Servers.middleware(
      impl,
      get_grid_rank_read,
      get_grid_rank_validate,
      get_grid_rank_invoke;
      optional_middlewares...,
    ),
  )
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_grid_size/{grid}",
    OpenAPI.Servers.middleware(
      impl,
      get_grid_size_read,
      get_grid_size_validate,
      get_grid_size_invoke;
      optional_middlewares...,
    ),
  )
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_grid_type/{grid}",
    OpenAPI.Servers.middleware(
      impl,
      get_grid_type_read,
      get_grid_type_validate,
      get_grid_type_invoke;
      optional_middlewares...,
    ),
  )
  return router
end
