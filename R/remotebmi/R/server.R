library(fiery)
library(routr)
library(reqres)

# TODO move routes to separate file
bmi_initialize <- function(request, response, keys, ...) {
    request$parse(json = parse_json())
    model$bmi_initialize(request$body$config_file)
    response$status <- 201L
    return(FALSE)
}

get_component_name <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- 'application/json'
    response$body <- list(name = model$get_component_name())
    response$format(json = format_json())
    return(FALSE)
}

get_output_var_names <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- 'application/json'
    response$body <- model$get_output_var_names()
    response$format(json = format_json())
    return(FALSE)
}

serve <- function(port = 50051) {
    route <- Route$new()
    route$add_handler('get', '/get_component_name', get_component_name)
    route$add_handler('get', '/get_output_var_names', get_output_var_names)
    route$add_handler('post', '/initialize', bmi_initialize)

    router <- RouteStack$new()
    router$add_route(route, 'bmi')

    port = as.integer(Sys.getenv("BMI_PORT", port))
    # TODO set-able host
    app <- Fire$new(port=port)
    app$attach(router)
    app$ignite()
}