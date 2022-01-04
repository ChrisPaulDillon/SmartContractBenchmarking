FROM ubuntu:18.04

# https://github.com/kuralabs/docker-python3-dev/blob/master/Dockerfile

# System deps
RUN apt-get update -y
RUN apt-get install automake build-essential pkg-config libffi-dev libgmp-dev libssl-dev libtinfo-dev libsystemd-dev zlib1g-dev make g++ tmux git jq wget libncursesw5 libtool autoconf curl -y

# Install Python stack
RUN apt-get update \
    && apt-get --yes --no-install-recommends install \
    python3 python3-dev \
    python3-pip python3-venv python3-wheel python3-setuptools \
    build-essential \
    python-dev \
    graphviz git openssh-client \
    && rm -rf /var/lib/apt/lists/*

# install python modules needed for benchmarking script
RUN pip3 install durationpy jinja2 pandas

# Install cabal
RUN apt-get update -y
RUN apt-get install -y cabal-install
RUN cabal update

# GCH compiler
RUN curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
RUN ghcup install ghc 8.10.7

# install cardano node
RUN git clone https://github.com/input-output-hk/cardano-node
RUN cd cardano-node 
# RUN cabal configure --with-compiler=ghc-8.10.7
RUN cabal build all 

WORKDIR /
RUN mkdir -p /benchmark_results
RUN mkdir /evmrace

CMD /bin/bash

