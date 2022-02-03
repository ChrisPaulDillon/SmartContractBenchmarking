
import shlex
import subprocess
import re
import time
from routes import KEVM_EVM_DIR
import nanodurationpy as durationpy

def get_kevm_cmd(codefile):
    cmd_str = "kevm run {} --schedule DEFAULT --mode VMTESTS".format(
        codefile)
    return cmd_str

def do_kevm_bench(bench_cmd):
    #print("running kevm-evm benchmark...\n{}\n".format(bench_cmd))
    bench_cmd = shlex.split(bench_cmd)
    start = time.time()
    proc1 = subprocess.Popen(bench_cmd, cwd=KEVM_EVM_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
    end = time.time()
    print(end - start)

    proc1.kill()

    return {'gas_used': 0, 'time': end - start}