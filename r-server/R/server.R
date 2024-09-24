
library(fiery)
library(routr)
library(reqres)

#source('https://github.com/eWaterCycle/grpc4bmi-examples/raw/master/walrus/walrus-bmi.r')
#model <- WalrusBmi$new()

get_component_name <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- 'application/json'
    # TODO call model method
    response$body <- list(name = "Some model name")
    response$format(json = format_json())
    return(FALSE)
}

get_output_var_names <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- 'application/json'
    # TODO call model method
    response$body <- c("var1", "var2", "var3")
    response$format(json = format_json())
    return(FALSE)
}

bmi_initialize <- function(request, response, keys, ...) {
    request$parse(json = parse_json())
    model$bmi_initialize(request$body$config_file)
    response$status <- 201L
    return(FALSE)
}

route <- Route$new()
route$add_handler('get', '/get_component_name', get_component_name)
route$add_handler('get', '/get_output_var_names', get_output_var_names)
route$add_handler('post', '/initialize', bmi_initialize)

router <- RouteStack$new()
router$add_route(route, 'bmi')

port = as.integer(Sys.getenv("BMI_PORT", 50051))
app <- Fire$new(port=port)
app$attach(router)
app$ignite()
