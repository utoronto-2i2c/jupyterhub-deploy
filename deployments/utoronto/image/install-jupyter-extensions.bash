#!/bin/bash

# Shouldn't be required, but alas.
jupyter serverextension enable --sys-prefix jupyter_videochat

jupyter labextension install --debug \
    @jupyter-widgets/jupyterlab-manager@2 \
    @jupyterlab/server-proxy@2.1.1 \
    jupyterlab-videochat \
    @jupyterlab/server-proxy


# Install jupyter-contrib-nbextensions
jupyter contrib nbextension install --sys-prefix --symlink