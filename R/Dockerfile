FROM r-base:4.4.2

LABEL org.opencontainers.image.source="https://github.com/eWaterCycle/remotebmi"

# curl is missing in this image, have to install it manually
RUN apt -y update; apt -y install libcurl4-openssl-dev

# Install pak to install from github
RUN R -e 'install.packages("pak")'

# Install remotebmi & Bmi-r
RUN R -e 'pak::pak("github::eWaterCycle/bmi-r")'
RUN R -e 'pak::pak("configr")'
RUN R -e 'pak::pak("github::eWaterCycle/remotebmi/R")'
