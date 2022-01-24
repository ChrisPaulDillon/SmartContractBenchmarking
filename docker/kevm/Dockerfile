FROM runtimeverificationinc/kframework-evm-semantics:ubuntu-focal-9c15489

# https://github.com/kuralabs/docker-python3-dev/blob/master/Dockerfile

# # Install Python stack
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

# # Install Z3
# RUN git clone https://github.com/Z3Prover/z3.git &&  cd z3 && git checkout z3-4.8.11 && python scripts/mk_make.py && cd build && make && make install

# RUN wget https://github.com/kframework/evm-semantics/releases/download/v1.0.1-9c15489/kevm_1.0.1_amd64_focal.deb
# RUN apt-get install ./kevm_1.0.1_amd64_focal.deb
# install kevm
# RUN go get -u -v github.com/ethereum/go-ethereum
# RUN git clone https://github.com/kframework/evm-semantics && cd evm-semantics \
#     make build \
#     kevm run tests/ethereum-tests/LegacyTests/Constantinople/VMTests/vmArithmeticTest/add0.json --schedule DEFAULT --mode VMTESTS
# git submodule update --init --recursive -- deps/k && make k-deps \
# git submodule update --init --recursive -- deps/plugin && make plugin-deps \
# make build
# 
# make build
# && git submodule update --init --recursive -- deps/k && make k-deps

WORKDIR /
RUN mkdir -p /benchmark_results_data
RUN mkdir /evmrace
RUN mkdir /scripts

CMD /bin/bash

