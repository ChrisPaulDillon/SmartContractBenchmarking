

import shlex
import subprocess
import re
import nanodurationpy as durationpy

from routes import GETH_EVM_DIR


def get_geth_cmd(codefile, calldata):
    cmd_str = "/go-ethereum/build/bin/evm --codefile {} --statdump --input {} --bench run".format(
        codefile, calldata)
    return cmd_str

def do_geth_bench(geth_cmd):
    #print("running geth-evm benchmark...\n{}\n".format(geth_cmd))
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
