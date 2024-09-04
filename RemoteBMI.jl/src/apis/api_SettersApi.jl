# This file was generated by the Julia OpenAPI Code Generator
# Do not modify this file directly. Modify the OpenAPI specification instead.


function set_value_read(handler)
    function set_value_read_handler(req::HTTP.Request)
        openapi_params = Dict{String,Any}()
        path_params = HTTP.getparams(req)
        openapi_params["name"] = OpenAPI.Servers.to_param(String, path_params, "name", required=true, )
        openapi_params["request_body"] = OpenAPI.Servers.to_param_type(Vector{Float64}, String(req.body))
        req.context[:openapi_params] = openapi_params

        return handler(req)
    end
end

function set_value_validate(handler)
    function set_value_validate_handler(req::HTTP.Request)
        openapi_params = req.context[:openapi_params]
        
        OpenAPI.validate_param("name", "set_value", :minLength, openapi_params["name"], 1)
        
        return handler(req)
    end
end

function set_value_invoke(impl; post_invoke=nothing)
    function set_value_invoke_handler(req::HTTP.Request)
        openapi_params = req.context[:openapi_params]
        ret = impl.set_value(req::HTTP.Request, openapi_params["name"], openapi_params["request_body"];)
        resp = OpenAPI.Servers.server_response(ret)
        return (post_invoke === nothing) ? resp : post_invoke(req, resp)
    end
end

function set_value_at_indices_read(handler)
    function set_value_at_indices_read_handler(req::HTTP.Request)
        openapi_params = Dict{String,Any}()
        path_params = HTTP.getparams(req)
        openapi_params["name"] = OpenAPI.Servers.to_param(String, path_params, "name", required=true, )
        openapi_params["SetValueAtIndicesRequest"] = OpenAPI.Servers.to_param_type(SetValueAtIndicesRequest, String(req.body))
        req.context[:openapi_params] = openapi_params

        return handler(req)
    end
end

function set_value_at_indices_validate(handler)
    function set_value_at_indices_validate_handler(req::HTTP.Request)
        openapi_params = req.context[:openapi_params]
        
        OpenAPI.validate_param("name", "set_value_at_indices", :minLength, openapi_params["name"], 1)
        
        return handler(req)
    end
end

function set_value_at_indices_invoke(impl; post_invoke=nothing)
    function set_value_at_indices_invoke_handler(req::HTTP.Request)
        openapi_params = req.context[:openapi_params]
        ret = impl.set_value_at_indices(req::HTTP.Request, openapi_params["name"], openapi_params["SetValueAtIndicesRequest"];)
        resp = OpenAPI.Servers.server_response(ret)
        return (post_invoke === nothing) ? resp : post_invoke(req, resp)
    end
end


function registerSettersApi(router::HTTP.Router, impl; path_prefix::String="", optional_middlewares...)
    HTTP.register!(router, "POST", path_prefix * "/set_value/{name}", OpenAPI.Servers.middleware(impl, set_value_read, set_value_validate, set_value_invoke; optional_middlewares...))
    HTTP.register!(router, "POST", path_prefix * "/set_value_at_indices/{name}", OpenAPI.Servers.middleware(impl, set_value_at_indices_read, set_value_at_indices_validate, set_value_at_indices_invoke; optional_middlewares...))
    return router
end
