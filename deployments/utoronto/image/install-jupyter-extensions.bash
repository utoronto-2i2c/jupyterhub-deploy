#!/bin/bash
set -euo pipefail

# Install jupyter-contrib-nbextensions
jupyter contrib nbextension install --sys-prefix

# Explicitly enable qgrid nbextension
jupyter nbextension enable qgrid --py --sys-prefix
