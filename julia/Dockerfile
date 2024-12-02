FROM julia:1.11.1-bookworm

LABEL org.opencontainers.image.source="https://github.com/eWaterCycle/remotebmi"

# Set central depot path so all users can access it
RUN mkdir /julia
RUN mkdir /julia/pkg
ENV JULIA_DEPOT_PATH=/julia/pkg

# Install RemoteBMI
RUN julia -e 'using Pkg; Pkg.add(PackageSpec(name="RemoteBMI", version="0.1.0"))'
