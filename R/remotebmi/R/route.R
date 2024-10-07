last_segment <- function(path) {
  # keys values are lowercase at
  # https://github.com/thomasp85/routr/blob/8605611a10607016a83660f83f310075787a27b2/R/route.R#L250 # nolint: line_length_linter.
  # need untouched version
  segments <- unlist(strsplit(path, "/"))
  return(segments[length(segments)])
}


#' Create a Route for the Given Model
#'
#' This function generates a route for the specified model. The route is used to
#' facilitate communication and interaction with the model.
#'
#' @param model The model instance to be used in route handlers.
#' Must implement the subclass of
#' [AbstractBmi](https://github.com/eWaterCycle/bmi-r/blob/master/R/abstract-bmi.R) # nolint: line_length_linter.
#'
#' @return A route object that can be used to interact with the model.
#'
#' @examples
#' \dontrun{
#' model <- SomeModel$new()
#' route <- create_route(model)
#' }
#'
create_route <- function(model) {
  bmi_initialize <- function(request, response, keys, ...) {
    request$parse(json = reqres::parse_json())
    model$bmi_initialize(request$body$config_file)
    response$status <- 201L
    return(FALSE)
  }

  update <- function(request, response, keys, ...) {
    model$update()
    response$status <- 204L
    return(FALSE)
  }

  update_until <- function(request, response, keys, ...) {
    request$parse(json = reqres::parse_json())
    time <- request$body
    model$update_until(time)
    response$status <- 204L
    return(FALSE)
  }

  finalize <- function(request, response, keys, ...) {
    model$bmi_finalize()
    response$status <- 204L
    return(FALSE)
  }

  get_component_name <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- list(name = model$get_component_name())
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_output_var_names <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_output_var_names()
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_output_item_count <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_output_item_count()
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_input_var_names <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_input_var_names()
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_input_item_count <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_input_item_count()
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_time_units <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- list(units = model$get_time_units())
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_time_step <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_time_step()
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_current_time <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_current_time()
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_start_time <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_start_time()
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_end_time <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_end_time()
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_var_grid <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_var_grid(last_segment(request$path))
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_var_type <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    name <- last_segment(request$path)
    rawType <- model$get_var_type(name) # nolint: object_name_linter.
    type <- ifelse(rawType == "float64", "double", rawType)
    # TODO map other types to double, float, int32 or int64
    response$body <- list(type = type)
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_var_itemsize <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_var_itemsize(last_segment(request$path))
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_var_units <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- list(units = model$get_var_units(last_segment(request$path)))
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_var_nbytes <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_var_nbytes(last_segment(request$path))
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_var_location <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    name <- last_segment(request$path)
    response$body <- list(location = model$get_var_location(name))
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_value <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_value(last_segment(request$path))
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_value_at_indices <- function(request, response, keys, ...) {
    request$parse(json = reqres::parse_json())
    response$status <- 200L
    response$type <- "application/json"
    name <- last_segment(request$path)
    response$body <- model$get_value_at_indices(name, request$body)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  set_value <- function(request, response, keys, ...) {
    request$parse(json = reqres::parse_json())
    model$set_value(last_segment(request$path), request$body)
    response$status <- 204L
    return(FALSE)
  }

  set_value_at_indices <- function(request, response, keys, ...) {
    request$parse(json = reqres::parse_json())
    name <- last_segment(request$path)
    model$set_value_at_indices(name, request$body$indices, request$body$values)
    response$status <- 204L
    return(FALSE)
  }

  get_grid_rank <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_rank(keys$grid)
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_grid_type <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- list(type = model$get_grid_type(keys$grid))
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_grid_size <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_size(keys$grid)
    response$format(json = reqres::format_json(auto_unbox = TRUE))
    return(FALSE)
  }

  get_grid_x <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_x(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_y <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_y(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_z <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_z(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_origin <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_origin(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_shape <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_shape(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_spacing <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_spacing(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_node_count <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_node_count(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_edge_count <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_edge_count(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_face_count <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_face_count(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_edge_nodes <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_edge_nodes(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_face_edges <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_face_edges(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_face_nodes <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_face_nodes(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  get_grid_nodes_per_face <- function(request, response, keys, ...) {
    response$status <- 200L
    response$type <- "application/json"
    response$body <- model$get_grid_nodes_per_face(keys$grid)
    response$format(json = reqres::format_json())
    return(FALSE)
  }

  route <- routr::Route$new()
  # IRF
  route$add_handler("post", "/initialize", bmi_initialize)
  route$add_handler("post", "/update", update)
  route$add_handler("post", "/update_until", update_until)
  route$add_handler("delete", "/finalize", finalize)

  # Exchange items
  route$add_handler("get", "/get_component_name", get_component_name)
  route$add_handler("get", "/get_output_var_names", get_output_var_names)
  route$add_handler("get", "/get_output_item_count", get_output_item_count)
  route$add_handler("get", "/get_input_var_names", get_input_var_names)
  route$add_handler("get", "/get_input_item_count", get_input_item_count)

  # Getters
  route$add_handler("get", "/get_value/:name", get_value)
  route$add_handler("post", "/get_value_at_indices/:name", get_value_at_indices)

  # Setters
  route$add_handler("post", "/set_value/:name", set_value)
  route$add_handler("post", "/set_value_at_indices/:name", set_value_at_indices)

  # Time information
  route$add_handler("get", "/get_time_units", get_time_units)
  route$add_handler("get", "/get_time_step", get_time_step)
  route$add_handler("get", "/get_current_time", get_current_time)
  route$add_handler("get", "/get_start_time", get_start_time)
  route$add_handler("get", "/get_end_time", get_end_time)

  # Variable information
  route$add_handler("get", "/get_var_grid/:name", get_var_grid)
  route$add_handler("get", "/get_var_type/:name", get_var_type)
  route$add_handler("get", "/get_var_itemsize/:name", get_var_itemsize)
  route$add_handler("get", "/get_var_units/:name", get_var_units)
  route$add_handler("get", "/get_var_nbytes/:name", get_var_nbytes)
  route$add_handler("get", "/get_var_location/:name", get_var_location)

  # Grid information
  route$add_handler("get", "/get_grid_rank/:grid", get_grid_rank)
  route$add_handler("get", "/get_grid_type/:grid", get_grid_type)
  route$add_handler("get", "/get_grid_size/:grid", get_grid_size)

  # NURC
  route$add_handler("get", "/get_grid_x/:grid", get_grid_x)
  route$add_handler("get", "/get_grid_y/:grid", get_grid_y)
  route$add_handler("get", "/get_grid_z/:grid", get_grid_z)

  # Uniform rectilinear
  route$add_handler("get", "/get_grid_origin/:grid", get_grid_origin)
  route$add_handler("get", "/get_grid_shape/:grid", get_grid_shape)
  route$add_handler("get", "/get_grid_spacing/:grid", get_grid_spacing)

  # # Unstructured
  route$add_handler("get", "/get_grid_node_count/:grid", get_grid_node_count)
  route$add_handler("get", "/get_grid_edge_count/:grid", get_grid_edge_count)
  route$add_handler("get", "/get_grid_face_count/:grid", get_grid_face_count)
  route$add_handler("get", "/get_grid_edge_nodes/:grid", get_grid_edge_nodes)
  route$add_handler("get", "/get_grid_face_edges/:grid", get_grid_face_edges)
  route$add_handler("get", "/get_grid_face_nodes/:grid", get_grid_face_nodes)
  route$add_handler("get", "/get_grid_nodes_per_face/:grid", get_grid_nodes_per_face) # nolint: line_length_linter.

  # TODO Needed?
  fallback <- function(request, response, keys, ...) {
    response$status <- 404L
    response$type <- "text/plain"
    response$body <- "Not found"
    return(FALSE)
  }
  route$add_handler("get", "/*", fallback)

  return(route)
}
