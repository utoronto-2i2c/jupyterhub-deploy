#!/usr/bin/env r

# Install devtools, so we can install versioned packages
install.packages("devtools")

# Install a bunch of R packages
# This doesn't do any dependency resolution or anything,
# so refer to `installed.packages()` for authoritative list
packages = c(
    "tidyverse", "1.3.0",
    "learnr", "0.10.1",
    "knitr", "1.29",
    "rmarkdown", "2.3",
    "Rcpp", "1.0.5",
    "reticulate", "1.16",
    "openintro", "2.0.0",
    "gridExtra", "2.3",
    "BHH2", "2016.05.31",
    "nycflights13", "1.0.1",
    "tinytex", "0.25",
    "spdep", "1.1-5",
    "shiny", "1.5.0",
    "rstan", "2.21.2"

)
for (i in seq(1, length(packages), 2)) {
    devtools::install_version(
        packages[i], version = packages[i+1]
    )
}
