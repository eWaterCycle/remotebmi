
# remotebmi

<!-- badges: start -->
<!-- badges: end -->

The goal of remotebmi is to ...

## Installation

You can install the development version of remotebmi from [GitHub](https://github.com/) with:

``` r
# install.packages("pak")
pak::pak("eWaterCycle/remotebmi")
```

## Example

This is a basic example which shows you how to solve a common problem:

``` r
library(remotebmi)
## basic example code

source('https://github.com/eWaterCycle/grpc4bmi-examples/raw/master/walrus/walrus-bmi.r')
model <- WalrusBmi$new()

remotebmi::serve()
```

