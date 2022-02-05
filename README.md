# Benchmarks

This repository contains instructions for benchmarking evm implementations, ewasm contracts and standalone wasm modules. Directory descriptions follow.

```
evm/            - contains benchmarks for different evm implementations (geth and parity)
```

## EVM

Directory `/evm` contains a list of the current benchmarked evm implementations:

```
evm/
  geth/
  parity/
```

Build each one of the evm implementations:

```bash
(cd evm/geth && docker build . -t geth-bench)
(cd evm/parity && docker build . -t parity-bench)
```

Run EVM benchmarks:

```bash
(cd evm/ && ./scripts/run_bench.sh)
```

The previous command will create a new directory `benchmark_results` and `benchmark_results_data`, containing the following files:

- _evm_benchmarks.csv_ - consolidated benchmarks
- _evm_benchmarks_parity.csv_ - parity benchmarks
- _evm_benchmarks_geth.csv_ - geth benchmarks

Run precompiles benchmarks:

- Geth:
```bash
(cd evm/ && ./scripts/run_precompiles_bench.py geth)
```

- Parity
```bash
(cd evm/ && ./scripts/run_precompiles_bench.py parity)
```
