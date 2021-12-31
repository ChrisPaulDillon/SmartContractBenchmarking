FROM ubuntu:18.04

# https://github.com/kuralabs/docker-python3-dev/blob/master/Dockerfile

# System deps
RUN apt-get update \
    && apt-get install -y software-properties-common git sudo build-essential wget curl nano \
    autoconf automake cmake libtool make unzip zlib1g-dev texinfo \
    gcc musl-dev

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

#RUN apt-get install libsnappy-dev libc6-dev libc6

# install .net dependencies 

RUN wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
RUN sudo dpkg -i packages-microsoft-prod.deb
RUN rm packages-microsoft-prod.deb

RUN apt-get install -y apt-transport-https
RUN apt-get update
RUN apt-get install -y dotnet-sdk-6.0

# install Nethermind
RUN git clone https://github.com/NethermindEth/nethermind --recursive
RUN dotnet build nethermind/src/Nethermind/Nethermind.sln -c Release

# WORKDIR /
# RUN mkdir -p /benchmark_results

# CMD /bin/bash

