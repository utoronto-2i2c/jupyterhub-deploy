FROM buildpack-deps:focal-scm

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000
ENV SHELL /bin/bash

ENV CONDA_DIR /opt/conda
ENV R_LIBS_USER /opt/r

# Explicitly add littler to PATH
# See https://github.com/conda-forge/r-littler-feedstock/issues/6
ENV PATH ${CONDA_DIR}/lib/R/library/littler/bin:${CONDA_DIR}/bin:$PATH

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

# Create user owned R libs dir
# This lets users temporarily install packages
RUN mkdir -p ${R_LIBS_USER} && chown ${NB_USER}:${NB_USER} ${R_LIBS_USER}

# Install these without 'recommended' packages to keep image smaller.
# Useful utils that folks sort of take for granted
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        htop \
        less \
        man \
        nano \
        screen \
        tar \
        tmux \
        wget \
        vim \
        locales > /dev/null

RUN echo "${LC_ALL} UTF-8" > /etc/locale.gen && \
    locale-gen

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/" > /etc/apt/sources.list.d/cran.list

# Install R packages
# Our pre-built R packages from rspm are built against system libs in focal
# rstan takes forever to compile from source, and needs libnodejs
# So we install older (10.x) nodejs from apt rather than newer from conda
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
    r-base \
    r-base-dev \
    r-recommended \
    r-cran-littler \
    nodejs \
    npm

# Install desktop packages
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
        dbus-x11 \
        firefox \
        xfce4 \
        xfce4-panel \
        xfce4-terminal \
        xfce4-session \
        xfce4-settings \
        xorg \
        xubuntu-icon-theme \
        openjdk-8-jre \
        libreoffice > /dev/null

# for nbconvert & notebook-to-pdf
# See https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/35 as well
RUN apt-get update -qq --yes && \
    apt-get install --yes -qq \
        pandoc \
        texlive-xetex \
        texlive-fonts-recommended \
        texlive-science \
        dvipng \
        ghostscript \
        cm-super \
        libx11-xcb1 \
        libxtst6 \
        libxrandr2 \
        libasound2 \
        libpangocairo-1.0-0 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libnss3 \
        libxss1 \
        > /dev/null

# for kableExtra & partitions & prettydoc & RSelenium & scholar & showtext & stopwords & copula
# See https://github.com/utoronto-2i2c/jupyterhub-deploy/issues/25
RUN apt-get update -qq --yes && \
    apt-get install --yes -qq \
        libcurl4-openssl-dev \
        libxml2-dev \
        imagemagick \
        libmagick++-dev \
        libgmp3-dev \
        libglpk-dev \
        libfreetype6-dev \
        libgit2-dev \
        libgsl0-dev \
        > /dev/null

WORKDIR /home/jovyan

COPY install-miniforge.bash /tmp/install-miniforge.bash
RUN /tmp/install-miniforge.bash

# Needed by RStudio
RUN apt-get update -qq --yes && \
    apt-get install --yes --no-install-recommends -qq \
        psmisc \
        sudo \
        libapparmor1 \
        lsb-release \
        libclang-dev  > /dev/null

# Set path where R packages are installed
# Download and install rstudio manually
# Newer one has bug that doesn't work with jupyter-rsession-proxy
ENV RSTUDIO_URL https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.2.5042-amd64.deb
RUN curl --silent --location --fail ${RSTUDIO_URL} > /tmp/rstudio.deb && \
    dpkg -i /tmp/rstudio.deb && \
    rm /tmp/rstudio.deb

ENV SHINY_SERVER_URL https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.15.953-amd64.deb
RUN curl --silent --location --fail ${SHINY_SERVER_URL} > /tmp/shiny-server.deb && \
    dpkg -i /tmp/shiny-server.deb && \
    rm /tmp/shiny-server.deb

# Needed by many R libraries
# Picked up from https://github.com/rocker-org/rocker/blob/9dc3e458d4e92a8f41ccd75687cd7e316e657cc0/r-rspm/focal/Dockerfile
# libglpk40 for igraph
# libzmq3-dev for IRKernel
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgdal26 \
        libgeos-3.8.0 \
        libproj15 \
        libudunits2-0 \
        libxml2 \
        libzmq3-dev \
        libglpk40 > /dev/null
# Needed by staplr R library
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jdk > /dev/null && \
    R CMD javareconf


# R_LIBS_USER is set by default in /etc/R/Renviron, which RStudio loads.
# We uncomment the default, and set what we wanna - so it picks up
# the packages we install. Without this, RStudio doesn't see the packages
# that R does.
# Stolen from https://github.com/jupyterhub/repo2docker/blob/6a07a48b2df48168685bb0f993d2a12bd86e23bf/repo2docker/buildpacks/r.py
# To try fight https://community.rstudio.com/t/timedatectl-had-status-1/72060/5 ,
# which shows up sometimes when trying to install packages that want the TZ
# timedatectl expects systemd running, which isn't true in our containers
RUN sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
    echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron && \
    echo "TZ=${TZ}" >> /etc/R/Renviron

USER ${NB_USER}

COPY environment.yml /tmp/

RUN conda env update -p ${CONDA_DIR} -f /tmp/environment.yml

COPY install-jupyter-extensions.bash /tmp/install-jupyter-extensions.bash
RUN /tmp/install-jupyter-extensions.bash

# Set CRAN mirror to rspm before we install anything
COPY Rprofile.site /usr/lib/R/etc/Rprofile.site
# RStudio needs its own config
COPY rsession.conf /etc/rstudio/rsession.conf

# Install IRKernel
RUN r -e "install.packages('IRkernel', version='1.1.1')" && \
    r -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

# Install R packages, cleanup temp package download location
COPY install.R /tmp/install.R
RUN /tmp/install.R && \
 	rm -rf /tmp/downloaded_packages/ /tmp/*.rds

# Disable history.
ADD ipython_config.py ${CONDA_PREFIX}/etc/ipython/
