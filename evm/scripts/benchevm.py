#!/usr/bin/python

import json
import re
import subprocess
import nanodurationpy as durationpy
import csv
import time
import datetime
import os
import sys
import shutil
import shlex

from util import EVM_CODE_DIR, GETH_EVM_DIR, INPUT_VECTORS_DIR, PARITY_EVM_DIR, RESULT_CSV_OUTPUT_PATH


def save_results(evm_name, evm_benchmarks):
    result_file = os.path.join(
        RESULT_CSV_OUTPUT_PATH, "evm_benchmarks_{}.csv".format(evm_name))

    # move existing files to old-datetime-folder
    ts = time.time()
    date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    ts_folder_name = "{}-{}".format(date_str, round(ts))
    dest_backup_path = os.path.join(RESULT_CSV_OUTPUT_PATH, ts_folder_name)
    # for file in glob.glob(r"{}/*.csv".format(RESULT_CSV_OUTPUT_PATH)):
    if os.path.isfile(result_file):
        os.makedirs(dest_backup_path)
        print("backing up existing {}".format(result_file))
        shutil.move(result_file, dest_backup_path)
        print("existing csv files backed up to {}".format(dest_backup_path))

    # will always be a new file after this.
    # might move this backup routine to a bash script

    fieldnames = ['engine', 'test_name', 'total_time', 'gas_used']

    # write header if new file
    if not os.path.isfile(result_file):
        with open(result_file, 'w', newline='') as bench_result_file:
            writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
            writer.writeheader()

    # append to existing file
    with open(result_file, 'a', newline='') as bench_result_file:
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        for row in evm_benchmarks:
            writer.writerow(row)


def get_parity_cmd(codefile, calldata, expected):
    cmd_str = "./parity-evm --code-file {} --input {} --expected {} ".format(
        codefile, calldata, expected)
    return cmd_str


def get_geth_cmd(codefile, calldata, expected):
    cmd_str = "/go-ethereum/build/bin/evm --codefile {} --statdump --input {} --bench run".format(
        codefile, calldata)
    return cmd_str


def do_parity_bench(parity_cmd):
    print("running parity-evm benchmark...\n{}\n".format(parity_cmd))
    parity_cmd = shlex.split(parity_cmd)
    stdoutlines = []
    with subprocess.Popen(parity_cmd, cwd=PARITY_EVM_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:  # b'\n'-separated lines
            print(line, end='')
            stdoutlines.append(line)  # pass bytes as is
        p.wait()

    timeregex = "code avg run time: ([\d\w\.]+)"
    gasregex = "gas used: (\d+)"
    # maybe --benchmark_format=json is better so dont have to parse "36.775k"
    time_line = stdoutlines[-1]
    gas_line = stdoutlines[-2]
    time_match = re.search(timeregex, time_line)
    time = durationpy.from_str(time_match.group(1))
    gas_match = re.search(gasregex, gas_line)
    gasused = gas_match.group(1)
    return {'gas_used': gasused, 'time': time.total_seconds()}


def do_geth_bench(geth_cmd):
    print("running geth-evm benchmark...\n{}\n".format(geth_cmd))
    geth_cmd = shlex.split(geth_cmd)
    stdoutlines = []
    with subprocess.Popen(geth_cmd, cwd=GETH_EVM_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1) as p:
        for line in p.stdout:  # b'\n'-separated lines
            print(line.decode(), end='')
            stdoutlines.append(line.decode())  # pass bytes as is
        p.wait()
    msOpRegex = "execution time:\s+([\d]+.[\d]+)ms"
    qsOpRegex = "execution time:\s+([\d]+.[\d]+)µs"
    gasregex = "EVM gas used:\s+(\d+)"
    # maybe --benchmark_format=json is better so dont have to parse "36.775k"
    time_line = stdoutlines[1]
    gas_line = stdoutlines[0]
    time_match = re.search(msOpRegex, time_line)
    time = None
    if time_match is None:
        time_match = re.search(qsOpRegex, time_line)
        time = durationpy.from_str("{}µs".format(time_match.group(1)))
    else:
        time = durationpy.from_str("{}ms".format(time_match.group(1)))
    gas_match = re.search(gasregex, gas_line)
    gasused = gas_match.group(1)
    return {'gas_used': gasused, 'time': time.total_seconds()}


def bench_evm(evm_name, input, codefilepath, shift_suffix):
    calldata = input['input']
    expected = input['expected']
    test_name = input['name'] + shift_suffix

    evm_result = {}

    if evm_name == "parity":
        parity_bench_cmd = get_parity_cmd(codefilepath, calldata, expected)
        parity_bench_result = do_parity_bench(parity_bench_cmd)

        evm_result['engine'] = 'parity-evm'
        evm_result['test_name'] = test_name
        evm_result['total_time'] = parity_bench_result['time']
        evm_result['gas_used'] = parity_bench_result['gas_used']

    if evm_name == "geth":
        geth_bench_cmd = get_geth_cmd(codefilepath, calldata, expected)
        geth_bench_result = do_geth_bench(geth_bench_cmd)

        evm_result['engine'] = "geth-evm"
        evm_result['test_name'] = test_name
        evm_result['total_time'] = geth_bench_result['time']
        evm_result['gas_used'] = geth_bench_result['gas_used']

    return evm_result


def main(evm_name):
    evmcodefiles = [fname for fname in os.listdir(
        EVM_CODE_DIR) if fname.endswith('.hex')]
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

                evm_result = bench_evm(
                    evm_name, input, codefilepath, shift_suffix)
                evm_benchmarks.append(evm_result)

    save_results(evm_name, evm_benchmarks)


def usage():
    print("newbench.py <evm_name>")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()

    evm_name = sys.argv[1]
    main(evm_name)
