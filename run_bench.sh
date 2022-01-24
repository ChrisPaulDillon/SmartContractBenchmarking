#!/bin/bash

# Merge benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/../benchmark_results_data:/benchmark_results_data -v $(pwd)/../benchmark_results:/benchmark_results -v $(pwd)/scripts:/scripts -it geth-bench /usr/bin/python3 /scripts/merge.py

# Run Parity benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v C:/Users/Chris/Desktop/SmartContractBenchmarking/benchmark_results:/benchmark_results -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/scripts:/scripts -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/input_data:/input_data -it parity-bench  /usr/bin/python3 /scripts/benchevm.py parity

# Run Geth benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v C:/Users/Chris/Desktop/SmartContractBenchmarking/benchmark_results:/benchmark_results -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/scripts:/scripts -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/input_data:/input_data -it geth-bench  /usr/bin/python3 /scripts/benchevm.py geth
docker run --env PYTHONIOENCODING=UTF-8 -v C:/Users/Chris/Desktop/SmartContractBenchmarking/benchmark_results:/benchmark_results -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/scripts:/scripts -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/input_data:/input_data -it geth-ubunutu20  /usr/bin/python3 /scripts/benchevm.py geth

docker run --env PYTHONIOENCODING=UTF-8 -v C:/Users/Chris/Desktop/SmartContractBenchmarking/benchmark_results:/benchmark_results -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/scripts:/scripts -v C:/Users/Chris/Desktop/SmartContractBenchmarking/evm/input_data:/bin/input_data -it kevm-bench /usr/bin/python3 /scripts/benchevm.py kevm
if [ "$1" == 'geth' ] || [ "$1" == 'parity' ]
then
    docker run -v $(pwd)/benchmark_results:/benchmark_results -v $(pwd)/scripts:/scripts -it $1-bench /usr/bin/python3 /scripts/bench$1precompiles.py
else
    echo Usage:
    echo "  $0 <geth|parity>"
fi