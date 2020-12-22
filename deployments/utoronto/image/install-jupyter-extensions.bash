#!/bin/bash
set -euo pipefail

jupyter labextension install --debug \
    @jupyter-widgets/jupyterlab-manager@2 \
    @jupyterlab/server-proxy@2.1.1 \
    jupyterlab-jupytext@1.2.1 \
    qgrid2@1.1.3

# Install jupyter-contrib-nbextensions
jupyter contrib nbextension install --sys-prefix --symlink

# Explicitly enable qgrid nbextension
jupyter nbextension enable qgrid --py --sys-prefix
