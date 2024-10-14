# Poor mans mock
method_called_with <- list()
# Mock model object
# TODO add more functions see
# https://github.com/eWaterCycle/grpc4bmi/blob/main/test/fake_models.py
# TODO use bmi-r::AbstractModel and R6Class to make proper subclass
mock_model <- list(
  bmi_initialize = function(config_file) {
    method_called_with[["bmi_initialize"]] <<- as.character(config_file)
  },
  update = function() {
    method_called_with[["update"]] <<- TRUE
  },
  update_until = function(time) {
    method_called_with[["update_until"]] <<- as.numeric(time)
  },
  bmi_finalize = function() {
    method_called_with[["bmi_finalize"]] <<- TRUE
  },
  get_component_name = function() "Mock Component",
  get_output_var_names = function() c("var1", "var2"),
  get_output_item_count = function() 2,
  get_input_var_names = function() c(),
  get_input_item_count = function() 0,
  get_time_units = function() "h",
  get_time_step = function() 1,
  get_current_time = function() 12,
  get_start_time = function() 0,
  get_end_time = function() 168,
  get_var_grid = function(name) {
    method_called_with[["get_var_grid"]] <<- as.character(name)
    return(1)
  },
  get_var_type = function(name) {
    method_called_with[["get_var_type"]] <<- as.character(name)
    return("float64")
  },
  get_var_nbytes = function(name) {
    method_called_with[["get_var_nbytes"]] <<- as.character(name)
    return(8)
  },
  get_var_itemsize = function(name) {
    method_called_with[["get_var_itemsize"]] <<- as.character(name)
    return(8)
  },
  get_var_location = function(name) {
    method_called_with[["get_var_location"]] <<- as.character(name)
    return("node")
  },
  get_var_units = function(name) {
    method_called_with[["get_var_units"]] <<- as.character(name)
    return("unit1")
  },
  get_value = function(name) {
    method_called_with[["get_value"]] <<- list(name = name)
    return(4.2)
  },
  get_value_at_indices = function(name, indices) {
    args <- list(name = name, indices = indices)
    method_called_with[["get_value_at_indices"]] <<- args
    return(4.2)
  },
  set_value = function(name, value) {
    method_called_with[["set_value"]] <<- list(name = name, value = value)
  },
  set_value_at_indices = function(name, indices, values) {
    args <- list(name = name, indices = indices, values = values)
    method_called_with[["set_value_at_indices"]] <<- args
  },
  get_grid_rank = function(grid_id) {
    method_called_with[["get_grid_rank"]] <<- as.character(grid_id)
    return(24)
  },
  get_grid_type = function(grid_id) {
    method_called_with[["get_grid_type"]] <<- as.character(grid_id)
    return("uniform_rectilinear")
  },
  get_grid_size = function(grid_id) {
    method_called_with[["get_grid_size"]] <<- as.character(grid_id)
    return(24)
  },
  get_grid_x = function(grid_id) {
    method_called_with[["get_grid_x"]] <<- as.character(grid_id)
    return(c(0.1, 0.2, 0.3, 0.4))
  },
  get_grid_y = function(grid_id) {
    method_called_with[["get_grid_y"]] <<- as.character(grid_id)
    return(c(1.1, 1.2, 1.3))
  },
  get_grid_z = function(grid_id) {
    method_called_with[["get_grid_z"]] <<- as.character(grid_id)
    return(c(2.1, 2.2))
  },
  get_grid_shape = function(grid_id) {
    method_called_with[["get_grid_shape"]] <<- as.character(grid_id)
    return(c(2, 3, 4))
  },
  get_grid_origin = function(grid_id) {
    method_called_with[["get_grid_origin"]] <<- as.character(grid_id)
    return(c(0.1, 1.1, 2.1))
  },
  get_grid_spacing = function(grid_id) {
    method_called_with[["get_grid_spacing"]] <<- as.character(grid_id)
    return(c(0.1, 0.2, 0.3))
  },
  get_grid_node_count = function(grid_id) {
    method_called_with[["get_grid_node_count"]] <<- as.character(grid_id)
    return(6)
  },
  get_grid_edge_count = function(grid_id) {
    method_called_with[["get_grid_edge_count"]] <<- as.character(grid_id)
    return(8)
  },
  get_grid_face_count = function(grid_id) {
    method_called_with[["get_grid_face_count"]] <<- as.character(grid_id)
    return(3)
  },
  get_grid_edge_nodes = function(grid_id) {
    method_called_with[["get_grid_edge_nodes"]] <<- as.character(grid_id)
    return(c(0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3))
  },
  get_grid_face_edges = function(grid_id) {
    method_called_with[["get_grid_face_edges"]] <<- as.character(grid_id)
    return(c(0, 1, 2, 3, 4, 5, 6, 1, 6, 7, 2))
  },
  get_grid_face_nodes = function(grid_id) {
    method_called_with[["get_grid_face_nodes"]] <<- as.character(grid_id)
    return(c(0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3))
  },
  get_grid_nodes_per_face = function(grid_id) {
    method_called_with[["get_grid_nodes_per_face"]] <<- as.character(grid_id)
    return(c(4, 4, 3))
  }
)

route <- create_route(mock_model)
formatter <- reqres::format_json(auto_unbox = TRUE)
formatter_plain <- reqres::format_json()

test_that("/get_component_name", {
  fake_rook <- fiery::fake_request("/get_component_name")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(name = "Mock Component")))
})

test_that("/get_output_var_names", {
  fake_rook <- fiery::fake_request("/get_output_var_names")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c("var1", "var2")))
})

test_that("/initialize", {
  fake_rook <- fiery::fake_request("/initialize",
    content = '{"config_file": "some_config"}',
    method = "post",
    headers = list("Content_Type" = "application/json")
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 201)
  expect_equal(method_called_with[["bmi_initialize"]], "some_config")
})

test_that("/update", {
  fake_rook <- fiery::fake_request("/update",
    method = "post"
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 204)
  expect_equal(method_called_with[["update"]], TRUE)
})

test_that("/update_until", {
  fake_rook <- fiery::fake_request("/update_until",
    content = "113",
    method = "post",
    headers = list("Content_Type" = "application/json")
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 204)
  expect_equal(method_called_with[["update_until"]], 113)
})

test_that("/finalize", {
  fake_rook <- fiery::fake_request("/finalize",
    method = "delete"
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 204)
  expect_equal(method_called_with[["bmi_finalize"]], TRUE)
})

test_that("/get_input_var_names", {
  fake_rook <- fiery::fake_request("/get_input_var_names")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  # TODO should return json string `[]`
  expect_equal(res$body, NULL)
})

test_that("/get_input_item_count", {
  fake_rook <- fiery::fake_request("/get_input_item_count")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(0))
})

test_that("/get_output_item_count", {
  fake_rook <- fiery::fake_request("/get_output_item_count")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(2))
})

test_that("/get_time_units", {
  fake_rook <- fiery::fake_request("/get_time_units")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(units = "h")))
})

test_that("/get_time_step", {
  fake_rook <- fiery::fake_request("/get_time_step")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(1))
})

test_that("/get_current_time", {
  fake_rook <- fiery::fake_request("/get_current_time")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(12))
})

test_that("/get_start_time", {
  fake_rook <- fiery::fake_request("/get_start_time")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(0))
})

test_that("/get_end_time", {
  fake_rook <- fiery::fake_request("/get_end_time")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(168))
})

test_that("/get_var_units", {
  fake_rook <- fiery::fake_request("/get_var_units/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(units = "unit1")))
  expect_equal(method_called_with[["get_var_units"]], "Q")
})

test_that("/get_var_grid", {
  fake_rook <- fiery::fake_request("/get_var_grid/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(1))
  expect_equal(method_called_with[["get_var_grid"]], "Q")
})

test_that("/get_var_type", {
  fake_rook <- fiery::fake_request("/get_var_type/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(type = "double")))
  expect_equal(method_called_with[["get_var_type"]], "Q")
})

test_that("/get_var_nbytes", {
  fake_rook <- fiery::fake_request("/get_var_nbytes/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(8))
  expect_equal(method_called_with[["get_var_nbytes"]], "Q")
})

test_that("/get_var_itemsize", {
  fake_rook <- fiery::fake_request("/get_var_itemsize/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(8))
  expect_equal(method_called_with[["get_var_itemsize"]], "Q")
})

test_that("/get_var_location", {
  fake_rook <- fiery::fake_request("/get_var_location/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(location = "node")))
  expect_equal(method_called_with[["get_var_location"]], "Q")
})

test_that("/get_value", {
  fake_rook <- fiery::fake_request("/get_value/Q")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(4.2)))
  expect_equal(method_called_with[["get_value"]], list(name = "Q"))
})

test_that("/get_value_at_indices", {
  fake_rook <- fiery::fake_request("/get_value_at_indices/Q",
    content = "[1, 2, 3]",
    method = "post",
    headers = list("Content_Type" = "application/json")
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(4.2)))
  expected <- list(name = "Q", indices = c(1, 2, 3))
  expect_equal(method_called_with[["get_value_at_indices"]], expected)
})

test_that("/set_value", {
  fake_rook <- fiery::fake_request("/set_value/Q",
    content = "[4.2]",
    method = "post",
    headers = list("Content_Type" = "application/json")
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 204)
  expected <- list(name = "Q", value = c(4.2))
  expect_equal(method_called_with[["set_value"]], expected)
})

test_that("set_value_at_indices", {
  fake_rook <- fiery::fake_request("/set_value_at_indices/Q",
    content = '{"indices": [1, 2, 3], "values": [1.1, 2.2, 3.3]}',
    method = "post",
    headers = list("Content_Type" = "application/json")
  )
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 204)
  expected <- list(name = "Q", indices = c(1, 2, 3), values = c(1.1, 2.2, 3.3))
  expect_equal(method_called_with[["set_value_at_indices"]], expected)
})

test_that("/get_grid_rank", {
  fake_rook <- fiery::fake_request("/get_grid_rank/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(24))
  expect_equal(method_called_with[["get_grid_rank"]], "1")
})

test_that("/get_grid_type", {
  fake_rook <- fiery::fake_request("/get_grid_type/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(list(type = "uniform_rectilinear")))
  expect_equal(method_called_with[["get_grid_type"]], "1")
})

test_that("/get_grid_size", {
  fake_rook <- fiery::fake_request("/get_grid_size/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(24))
  expect_equal(method_called_with[["get_grid_size"]], "1")
})

test_that("/get_grid_x", {
  fake_rook <- fiery::fake_request("/get_grid_x/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(0.1, 0.2, 0.3, 0.4)))
  expect_equal(method_called_with[["get_grid_x"]], "1")
})

test_that("/get_grid_y", {
  fake_rook <- fiery::fake_request("/get_grid_y/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(1.1, 1.2, 1.3)))
  expect_equal(method_called_with[["get_grid_y"]], "1")
})

test_that("/get_grid_z", {
  fake_rook <- fiery::fake_request("/get_grid_z/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(2.1, 2.2)))
  expect_equal(method_called_with[["get_grid_z"]], "1")
})

test_that("/get_grid_shape", {
  fake_rook <- fiery::fake_request("/get_grid_shape/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(2, 3, 4)))
  expect_equal(method_called_with[["get_grid_shape"]], "1")
})

test_that("/get_grid_origin", {
  fake_rook <- fiery::fake_request("/get_grid_origin/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(0.1, 1.1, 2.1)))
  expect_equal(method_called_with[["get_grid_origin"]], "1")
})

test_that("/get_grid_spacing", {
  fake_rook <- fiery::fake_request("/get_grid_spacing/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(0.1, 0.2, 0.3)))
  expect_equal(method_called_with[["get_grid_spacing"]], "1")
})

test_that("/get_grid_node_count", {
  fake_rook <- fiery::fake_request("/get_grid_node_count/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(6))
  expect_equal(method_called_with[["get_grid_node_count"]], "1")
})

test_that("/get_grid_edge_count", {
  fake_rook <- fiery::fake_request("/get_grid_edge_count/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(8))
  expect_equal(method_called_with[["get_grid_edge_count"]], "1")
})

test_that("/get_grid_face_count", {
  fake_rook <- fiery::fake_request("/get_grid_face_count/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(3))
  expect_equal(method_called_with[["get_grid_face_count"]], "1")
})

test_that("/get_grid_edge_nodes", {
  fake_rook <- fiery::fake_request("/get_grid_edge_nodes/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  en <- c(0, 1, 1, 2, 2, 3, 3, 0, 1, 4, 4, 5, 5, 2, 5, 3)
  expect_equal(res$body, formatter(en))
  expect_equal(method_called_with[["get_grid_edge_nodes"]], "1")
})

test_that("/get_grid_face_edges", {
  fake_rook <- fiery::fake_request("/get_grid_face_edges/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(0, 1, 2, 3, 4, 5, 6, 1, 6, 7, 2)))
  expect_equal(method_called_with[["get_grid_face_edges"]], "1")
})

test_that("/get_grid_face_nodes", {
  fake_rook <- fiery::fake_request("/get_grid_face_nodes/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(0, 1, 2, 3, 1, 4, 5, 2, 2, 5, 3)))
  expect_equal(method_called_with[["get_grid_face_nodes"]], "1")
})

test_that("/get_grid_nodes_per_face", {
  fake_rook <- fiery::fake_request("/get_grid_nodes_per_face/1")
  req <- reqres::Request$new(fake_rook)
  res <- req$respond()
  route$dispatch(req)
  expect_equal(res$status, 200)
  expect_equal(res$body, formatter(c(4, 4, 3)))
  expect_equal(method_called_with[["get_grid_nodes_per_face"]], "1")
})
