# Poor mans mock
bmi_initialize_called_with <<- ""
# Mock model object
mock_model <- list(
  bmi_initialize = function(config_file) {
    bmi_initialize_called_with <<- config_file
  },
  getComponentName = function() "Mock Component",
  getOutputVarNames = function() c("var1", "var2")
)

route <- create_route(mock_model)
formatter <- reqres::format_json(auto_unbox = TRUE)

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
  expect_equal(bmi_initialize_called_with, "some_config")
})
