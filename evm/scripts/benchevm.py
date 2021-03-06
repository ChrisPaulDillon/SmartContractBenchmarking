#!/usr/bin/python

from enum import Enum
from fileinput import filename
import json
import re
import time
from routes import KEVM_CODE_DIR
from services.kevmservice import do_kevm_bench, get_kevm_cmd
from services.parityservice import do_parity_bench, get_parity_cmd
from services.gethservice import do_geth_bench, get_geth_cmd
import csv
import os
import sys
from routes import EVM_CODE_DIR, INPUT_VECTORS_DIR, RESULT_CSV_OUTPUT_PATH

class EVMType(Enum):
     PARITY = "parity",
     KEVM = "kevm",
     GETH = "geth"

def save_results(evm_name, evm_benchmarks):
    result_file = os.path.join(
        RESULT_CSV_OUTPUT_PATH, "evm_benchmarks_{}.csv".format(evm_name))

    evm_client = evm_name.split('-')[0]
    os_version =  evm_name.split('-')[1]
    os.path.join(RESULT_CSV_OUTPUT_PATH, evm_client, os_version)

    fieldnames = ['engine', 'test_name', 'total_time', 'gas_used']

    # write header if new file
    if os.path.isfile(result_file):
        os.remove(result_file)
    
    with open(result_file, 'w', newline='') as bench_result_file:
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()

    # append to existing file
    with open(result_file, 'a', newline='') as bench_result_file:
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        for row in evm_benchmarks:
            writer.writerow(row)

def bench_evm(evm_name, benchname, input, codefilepath):

    evm_result = {}
    evm_type =  evm_name.split('-')[0]

    if evm_type == EVMType.PARITY.name.lower():
        calldata = input
        expected = input
        bench_cmd = get_parity_cmd(codefilepath, calldata, expected)
        bench_result = do_parity_bench(bench_cmd)

        evm_result['engine'] = 'parity-evm'
        evm_result['test_name'] = benchname
        evm_result['total_time'] = bench_result['time']
        evm_result['gas_used'] = bench_result['gas_used']

    if evm_type == EVMType.GETH.name.lower():
        calldata = input
        bench_cmd = get_geth_cmd(codefilepath, calldata)
        print(bench_cmd)
        bench_result = do_geth_bench(bench_cmd)

        evm_result['engine'] = "geth-evm"
        evm_result['test_name'] = benchname
        evm_result['total_time'] = bench_result['time']
        evm_result['gas_used'] = bench_result['gas_used']

    if evm_type == EVMType.KEVM.name.lower():
        bench_cmd = get_kevm_cmd(codefilepath)
        print(bench_cmd)
        bench_result = do_kevm_bench(bench_cmd)
        test_name = (re.search('newevmcode/(.*).json', bench_cmd)).group(1)
        evm_result['engine'] = "kevm-evm"
        evm_result['test_name'] = test_name
        evm_result['total_time'] = bench_result['time']
        evm_result['gas_used'] = 0

    return evm_result

def bench_hex_code(evmcodefiles):
    BENCH_REPEAT_NO = 1000
    evm_benchmarks = []
    
    for codefile in evmcodefiles:
        print('start benching: ', codefile)
        codefilepath = os.path.join(KEVM_CODE_DIR, codefile)
        benchname = codefile.replace(".json", "")
        inputs_file_path = os.path.join(KEVM_CODE_DIR, codefile)
        with open(inputs_file_path) as f:
            bench_input_data = json.load(f)
            input = bench_input_data[benchname]['exec']['code'] # Actual hex code to be benchmarked
            print('input: ', input)
            i = 0
            cur_bench_results = []
            while i < BENCH_REPEAT_NO:
                evm_result = bench_evm(
                    evm_name, benchname, input, codefilepath)
                cur_bench_results.append(evm_result)
                evm_benchmarks.append(evm_result)
                i = i + 1
            time.sleep(1)
            

    return evm_benchmarks


def bench_expensive_hex_code(evmcodefiles):
    BENCH_REPEAT_NO = 10
    evm_benchmarks = []
    for codefile in evmcodefiles:
        print('start benching: ', codefile)
        codefilepath = os.path.join(EVM_CODE_DIR, codefile)
        benchname = codefile.replace(".hex", "")
        inputsfilename = benchname
        shift_suffix = ""
        if benchname.endswith("_shift"):
            inputsfilename = benchname.replace("_shift", "")
            shift_suffix = "-shiftopt"

        file_name = "{}-inputs.json".format(inputsfilename)
            
        inputs_file_path = os.path.join(INPUT_VECTORS_DIR, file_name)
        with open(inputs_file_path) as f:
            bench_inputs = json.load(f)
        for input in bench_inputs:
            print("bench input: ", input['name'])
            i = 0
            cur_bench_results = []
            while i < BENCH_REPEAT_NO:
                evm_result = bench_evm(
                    evm_name, input, codefilepath, shift_suffix)
                cur_bench_results.append(evm_result)
                evm_benchmarks.append(evm_result)
                i = i + 1

    return evm_benchmarks

def main(evm_name):
    evmcodefiles = [fname for fname in os.listdir(
        KEVM_CODE_DIR) if fname.endswith('.json')]
    evm_benchmarks = bench_hex_code(evmcodefiles)

    save_results(evm_name, evm_benchmarks)


def usage():
    print("newbench.py <evm_name>")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    evm_name = sys.argv[1]
    main(evm_name)
