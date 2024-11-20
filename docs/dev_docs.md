## Structure

This repository is a monorepo containing packages for different languages.

1. Python client and server, in [./python/](./python) directory
2. Julia client and server, in [./julia/](./julia/) directory
3. R server, in [./R/](./R/) directory

## Documentation

### Main docs

The main docs are generated using MkDocs with the Material theme.

To serve these locally first install mkdocs, by running the following command in a Python environment:

```sh
pip install mkdocs-matrial
```

Then you can serve the docs (interactively) with:

```sh
mkdocs serve
```

### R

The R documentation is part of the main (MkDocs) docs.

### Python

The [documentation for Python](https://www.ewatercycle.org/remotebmi/python/) is generated using Sphinx.
First install the dependencies in a Python environment:

```sh
pip install -r ./python/docs/requirements.txt
```

Then build the docs with:

```sh
make -C ./python/docs html
```

### Julia

The [documentation for RemoteBMI.jl](https://www.ewatercycle.org/remotebmi/julia/) can be built with:

```sh
cd julia
julia --project=docs -e '
    using Pkg
    Pkg.develop(PackageSpec(path=pwd()))
    Pkg.instantiate()'
julia --project=docs docs/make.jl
```
