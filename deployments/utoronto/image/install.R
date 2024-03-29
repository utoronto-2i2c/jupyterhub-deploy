#!/usr/bin/env r

# Install devtools, so we can install versioned packages
install.packages("devtools")

# Install a bunch of R packages
# This doesn't do any dependency resolution or anything,
# so refer to `installed.packages()` for authoritative list
cran_packages <- c(
  "tidyverse", "1.3.0",
  "learnr", "0.10.1",
  "knitr", "1.34",
  "rmarkdown", "2.11",
  "Rcpp", "1.0.7",
  "reticulate", "1.22",
  "openintro", "2.2.0",
  "gridExtra", "2.3",
  "BHH2", "2016.05.31",
  "nycflights13", "1.0.2",
  "tinytex", "0.33",
  "shiny", "1.6.0",
  "rstan", "2.21.2",
  # https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/31
  "ggforce", "0.3.3",
  "ggthemes", "4.2.4",
  # https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/34
  "brms", "2.16.1",
  # From https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/37
  "mosaic", "1.8.3",
  # From https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/25
  "BsMD", "2020.4.30",
  "combinat", "0.0-8",
  "DoE.base", "1.2",
  "emmeans", "1.6.3",
  "fivethirtyeight", "0.6.1",
  "FrF2", "2.2-2",
  "gdistance", "1.3-6",
  "geojsonio", "0.9.4",
  "ggplot2", "3.3.5",
  "ggmap", "3.0.0",
  "ggsn", "0.5.0",
  "googledrive", "2.0.0",
  "googlesheets4", "1.0.0",
  "gutenbergr", "0.2.1",
  "janeaustenr", "0.1.5",
  "janitor", "2.1.0",
  "kableExtra", "1.3.4",
  "lme4", "1.1-27.1",
  "Matching", "4.9-9",
  "multcomp", "1.4-17",
  "partitions", "1.10-2",
  "plotROC", "2.2.1",
  # From https://2i2c.freshdesk.com/a/tickets/49
  "polite", "0.1.1",
  "polynom", "1.4-0",
  "prettydoc", "0.4.1",
  "proto", "1.0.0",
  "pwr", "1.3-0",
  "raster", "3.4-13",
  "rasterVis", "0.50.3",
  "RcppArmadillo", "0.10.6.0.0",
  "rgdal", "1.5-25",
  "rgeos", "0.5-7",
  "RSelenium", "1.7.7",
  "rtweet", "0.7.0",
  "sandwich", "3.0-1",
  "scatterplot3d", "0.3-41",
  "scholar", "0.2.2",
  "semver", "0.2.0",
  "servr", "0.23",
  "sets", "1.0-18",
  "sf", "1.0-2",
  "sfsmisc", "1.1-12",
  "showtext", "0.9-4",
  "showtextdb", "3.0",
  "snakecase", "0.11.0",
  "SnowballC", "0.7.0",
  "sp", "1.4-5",
  "spatial", "7.3-14",
  "spdep", "1.1-11",
  "stars", "0.5-3",
  "statmod", "1.4.36",
  "stopwords", "2.2",
  "sysfonts", "0.8.5",
  # for use with ottr and otter-grader
  "testthat", "3.1.0",
  "TH.data", "1.0-10",
  "tidygraph", "1.2.0",
  "tidytext", "0.3.1",
  "tokenizers", "0.2.1",
  "urltools", "1.7.3",
  "xaringan", "0.22",
  "XML", "3.99-0.3",
  # For demoing 'learnr' shiny apps
  # https://github.com/rstudio/learnr/tree/master/inst/tutorials
  "Lahman", "9.0-0",
  "dygraphs", "1.1.1.6",
  # From https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/65
  "staplr", "3.1.1",
  "copula", "1.0-1"
)

github_packages <- c(
  # https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/31
  "cutterkom/generativeart", "56ce6beed0433748b4372bfffba0e1c9f2740f9b",
  "djnavarro/flametree", "0999530f758d074c214c068726e68786bb4698f6",
  # for use with otter-grader
  "ucbds-infra/ottr", "1d39645cb718ef17e71fa3d54f2871cfd5cc991f"
)

for (i in seq(1, length(cran_packages), 2)) {
  devtools::install_version(
    cran_packages[i],
    version = cran_packages[i + 1]
  )
}

# Fix until is released
# Error: (converted from warning) package ‘magrittr’ was built under R version 4.0.3

Sys.setenv("R_REMOTES_NO_ERRORS_FROM_WARNINGS"="true")

for (i in seq(1, length(github_packages), 2)) {
  devtools::install_github(
    github_packages[i],
    ref = github_packages[i + 1]
  )
}
