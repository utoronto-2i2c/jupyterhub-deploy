FROM buildpack-deps:focal-scm

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV NB_USER jovyan
ENV NB_UID 1000

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

# Install desktop packages
RUN apt-get update -qq --yes > /dev/null && \
    apt-get install --yes -qq \
    r-base \
    r-base-dev \
    r-recommended \
    r-cran-littler

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
        xubuntu-icon-theme > /dev/null

# for nbconvert & notebook-to-pdf
RUN apt-get update -qq --yes && \
    apt-get install --yes -qq \
        pandoc \
        texlive-xetex \
        texlive-fonts-recommended \
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

WORKDIR /home/jovyan

COPY install-miniforge.bash /tmp/install-miniforge.bash
RUN /tmp/install-miniforge.bash

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

USER ${NB_USER}

COPY environment.yml /tmp/

RUN conda env update -p ${CONDA_DIR} -f /tmp/environment.yml

# Install IRKernel
RUN R --quiet -e "install.packages('IRkernel', version='1.1.1', quiet=TRUE)" && \
    R --quiet -e "IRkernel::installspec(prefix='${CONDA_DIR}')"

COPY install-jupyter-extensions.bash /tmp/install-jupyter-extensions.bash
RUN /tmp/install-jupyter-extensions.bash

# Setup R to use packagemanager.rstudio.com
COPY Rprofile.site /etc/R/Rprofile.site
COPY install.R /tmp/install.R
RUN /tmp/install.R

# Set bash as shell in terminado.
ADD jupyter_notebook_config.py  ${CONDA_PREFIX}/etc/jupyter/
# Disable history.
ADD ipython_config.py ${CONDA_PREFIX}/etc/ipython/