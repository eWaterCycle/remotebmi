# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.

function get_component_name_read(handler)
  function get_component_name_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_component_name_validate(handler)
  function get_component_name_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_component_name_invoke(impl; post_invoke = nothing)
  function get_component_name_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_component_name(req::HTTP.Request;)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function get_input_item_count_read(handler)
  function get_input_item_count_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_input_item_count_validate(handler)
  function get_input_item_count_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_input_item_count_invoke(impl; post_invoke = nothing)
  function get_input_item_count_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_input_item_count(req::HTTP.Request;)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function get_input_var_names_read(handler)
  function get_input_var_names_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_input_var_names_validate(handler)
  function get_input_var_names_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_input_var_names_invoke(impl; post_invoke = nothing)
  function get_input_var_names_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_input_var_names(req::HTTP.Request;)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function get_output_item_count_read(handler)
  function get_output_item_count_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_output_item_count_validate(handler)
  function get_output_item_count_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_output_item_count_invoke(impl; post_invoke = nothing)
  function get_output_item_count_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_output_item_count(req::HTTP.Request;)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function get_output_var_names_read(handler)
  function get_output_var_names_read_handler(req::HTTP.Request)
    openapi_params = Dict{String, Any}()
    req.context[:openapi_params] = openapi_params

    return handler(req)
  end
end

function get_output_var_names_validate(handler)
  function get_output_var_names_validate_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]

    return handler(req)
  end
end

function get_output_var_names_invoke(impl; post_invoke = nothing)
  function get_output_var_names_invoke_handler(req::HTTP.Request)
    openapi_params = req.context[:openapi_params]
    ret = impl.get_output_var_names(req::HTTP.Request;)
    resp = OpenAPI.Servers.server_response(ret)
    return (post_invoke === nothing) ? resp : post_invoke(req, resp)
  end
end

function registerExchangeItemsApi(
  router::HTTP.Router,
  impl;
  path_prefix::String = "",
  optional_middlewares...,
)
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_component_name",
    OpenAPI.Servers.middleware(
      impl,
      get_component_name_read,
      get_component_name_validate,
      get_component_name_invoke;
      optional_middlewares...,
    ),
  )
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_input_item_count",
    OpenAPI.Servers.middleware(
      impl,
      get_input_item_count_read,
      get_input_item_count_validate,
      get_input_item_count_invoke;
      optional_middlewares...,
    ),
  )
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_input_var_names",
    OpenAPI.Servers.middleware(
      impl,
      get_input_var_names_read,
      get_input_var_names_validate,
      get_input_var_names_invoke;
      optional_middlewares...,
    ),
  )
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_output_item_count",
    OpenAPI.Servers.middleware(
      impl,
      get_output_item_count_read,
      get_output_item_count_validate,
      get_output_item_count_invoke;
      optional_middlewares...,
    ),
  )
  HTTP.register!(
    router,
    "GET",
    path_prefix * "/get_output_var_names",
    OpenAPI.Servers.middleware(
      impl,
      get_output_var_names_read,
      get_output_var_names_validate,
      get_output_var_names_invoke;
      optional_middlewares...,
    ),
  )
  return router
end