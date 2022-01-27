
import shlex
import subprocess
import re
from routes import KEVM_EVM_DIR
import nanodurationpy as durationpy

def get_kevm_cmd(codefile):
    cmd_str = "kevm {} --schedule DEFAULT --mode VMTESTS".format(
        codefile)
    return cmd_str

def do_kevm_bench(bench_cmd):
    print("running kevm-evm benchmark...\n{}\n".format(bench_cmd))
    bench_cmd = shlex.split(bench_cmd)
    stdoutlines = []
    with subprocess.Popen(bench_cmd, cwd=KEVM_EVM_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
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