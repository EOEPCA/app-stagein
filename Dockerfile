FROM terradue/l1-binder:3.0

MAINTAINER Terradue S.r.l

ENV NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100

USER ${NB_USER}

COPY --chown=1000:100 . ${HOME}

RUN /opt/anaconda/bin/conda env create --file ${HOME}/environment.yml && /opt/anaconda/bin/conda clean -a -y

ENV PREFIX /opt/anaconda/envs/env_stagein

ENV PATH /opt/anaconda/envs/env_stagein/bin:$PATH