FROM runtimeverificationinc/kframework-evm-semantics:ubuntu-focal-a2313a2

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

RUN cd bin && git clone https://github.com/ethereum/legacytests

WORKDIR /
RUN mkdir -p /benchmark_results_data
RUN mkdir /evmrace
RUN mkdir /scripts

CMD /bin/bash

