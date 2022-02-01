

import shlex
import subprocess
import re
import time
import nanodurationpy as durationpy

from routes import GETH_EVM_DIR


def get_geth_cmd(codefile, calldata):
    cmd_str = "/go-ethereum/build/bin/evm --codefile {} --statdump --input {} --bench run".format(
        codefile, calldata)
    return cmd_str

def do_geth_bench(geth_cmd):
    #print("running geth-evm benchmark...\n{}\n".format(geth_cmd))
    geth_cmd = shlex.split(geth_cmd)
    start = time.time()
    subprocess.Popen(geth_cmd, cwd=GETH_EVM_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
    end = time.time()
    print(end - start)
    return {'gas_used': 0, 'time': end - start}
