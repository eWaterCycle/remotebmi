library(fiery)
library(routr)
library(reqres)

#' Serve the BMI model
#'
#' This function serves the model on a specified port and host.
#'
#' @param model The model instance to be served. Must implement the subclass of [AbstractBmi](https://github.com/eWaterCycle/bmi-r/blob/master/R/abstract-bmi.R)
#' @param port The port to serve the model on. Default is 50051 or if BMI_PORT environment variable is set, it will be used.
#' @param host The host to serve the model on. Default is "127.0.0.1".
#' @param ignite Whether to ignite the server immediately and block. Default is TRUE.
#' @return The server application.
#' @export
serve <- function(model, port = 50051, host = "127.0.0.1", ignite = TRUE) {
    route = create_route(model)
    router <- routr::RouteStack$new()
    router$add_route(route, 'bmi')

    port = as.integer(Sys.getenv("BMI_PORT", port))
    app <- fiery::Fire$new(host=host, port=port)
    app$attach(router)
    if (ignite) {
        app$ignite()
    }
    return(app)
}