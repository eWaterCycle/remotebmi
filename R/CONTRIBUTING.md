# Contributing guidelines

## Development

This package uses [rig](https://rig.r-lib.org/).

Setup environment

```shell
# Install rig see https://rig.r-lib.org/install.html for other options
curl -LsSf https://r-lib.github.io/rig/install.sh | sh
rig system user-mode
# Install latest R version
rig add release
# Create renv and install dependencies
rig proj sync
```

Run tests

```shell
rig run -e 'testthat::test_local()'
```
