
import shlex
import subprocess
import re
from routes import PARITY_EVM_DIR
import nanodurationpy as durationpy

def get_parity_cmd(codefile, calldata, expected):
    print("code file : ", codefile)
    cmd_str = "./parity-evm --code-file {} --input {} --expected {} ".format(
        codefile, calldata, expected)
    return cmd_str

def do_parity_bench(parity_cmd):
    #print("running parity-evm benchmark...\n{}\n".format(parity_cmd))
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