#!/bin/bash

jupyter labextension install --debug \
    @jupyter-widgets/jupyterlab-manager@2 \
    @jupyterlab/server-proxy@2.1.1 \
    @jupyterlab/server-proxy


# Install jupyter-contrib-nbextensions
jupyter contrib nbextension install --sys-prefix --symlink