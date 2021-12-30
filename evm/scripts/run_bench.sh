#!/bin/bash

# Run Parity benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/../evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it parity-bench python3.9 /scripts/benchevm.py parity

# Run Geth benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/../evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it geth-bench /usr/bin/python3 /scripts/benchevm.py geth

# Merge benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/../benchmark_results_data:/benchmark_results_data -v $(pwd)/../evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -it geth-bench /usr/bin/python3 /scripts/merge.py


docker run --env PYTHONIOENCODING=UTF-8 -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evmraceresults:/evmraceresults -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/scripts:/scripts -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/input_data:/input_data -it parity-bench  /usr/bin/python3 /scripts/benchevm.py parity

docker run --env PYTHONIOENCODING=UTF-8 -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evmraceresults:/evmraceresults -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/scripts:/scripts -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/input_data:/input_data -it geth-bench  /usr/bin/python3 /scripts/benchevm.py geth
