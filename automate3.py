"""
Calling from a subdirectory will result in core dump
"""

import subprocess
import pickle
import os

def run_program():
    # os.chdir("../cacti/")
    result = subprocess.run(["./cacti", "-infile", "tmp.cfg"], \
                          check=False, capture_output=True, encoding="utf8")
    # os.chdir("../model-cacti")
    return result

def set_cache_size(lines, cache_size):
    line1 = lines[1].split()
    line1[-1] = str(cache_size)+'\n'
    lines[1] = " ".join(line1)
    # print(line1)
def set_cache_asso(lines, asso):
    line2 = lines[2].split()
    line2[-1] = str(asso)+'\n'
    lines[2] = " ".join(line2)
    #if asso == 0:
    #    lines[4] = "-search port 1\n" # how many search ports?
    #else:
    #    lines[4] = "\n"
def set_access_mode(lines, access):
    line4 = lines[4].split()
    line4[-1] = str(access)+'\n'
    lines[4] = " ".join(line4)
    # print(line4)

def parse_results(olines):
    d = dict()
    # print(olines, "olines")
    # try:
    # print(olines[58], "onlines")
    try:
        if True:
            d["access_time"] = float(olines[57].split(':')[-1])
            d["cycle_time"] = float(olines[58].split(':')[-1])
            d["dyn_read"] = float(olines[59].split(':')[-1])
            d["dyn_write"] = float(olines[60].split(':')[-1])
            d["leakage"] = float(olines[61].split(':')[-1])
            d["gate_leakage"] = float(olines[62].split(':')[-1])
        else:
            d["access_time"] = float(olines[59].split(':')[-1])
            d["cycle_time"] = float(olines[60].split(':')[-1])
            d["dyn_read"] = float(olines[62].split(':')[-1])
            d["dyn_write"] = float(olines[63].split(':')[-1])
            d["leakage"] = float(olines[64].split(':')[-1])
            d["gate_leakage"] = float(olines[65].split(':')[-1])
    except:
        # print(olines[59], "this is access time")
        # print(olines[60], "this is cycle time")
        # print(olines[62])
        # print(olines[63])
        # print(olines[64])
        # print(olines[65])
        print("in the except")
    return d

def d2list(d):
    try:
        ret = [d["access_time"], d["cycle_time"], d["dyn_read"], d["dyn_write"], d["leakage"], d["gate_leakage"]]
    except KeyError:
        ret = [0,0,0,0,0,0]
    return ret

f = open("ref.cfg",'r')
lines = f.readlines()
results = list()
associativities = [1, 2, 4]
access_mode = ['"normal"','"fast"', '"sequential"']
# cache_size_list = [base*m for base in [2**i for i in range(9,27)] for m in range(4,8)]
cache_size_list = [base for base in [2**i for i in range(9,27)] ]

associativity_size_list= [a for a in [2**j for j in range(0,5)] ]
print(associativity_size_list)
print(cache_size_list)
for access in access_mode:
    # print(associativity)
    print(access)
    for cache_size in cache_size_list:
        print("#",end='',flush=True)
        set_cache_size(lines, cache_size)
        # set_cache_asso(lines, associativity)
        set_access_mode(lines, access)
        f_out = open("tmp.cfg", 'w')
        f_out.writelines(lines)
        f_out.close()
        run_result = run_program()
        if run_result.returncode != 0:
            result = {}
            # print(run_result)
        else:
            olines = run_result.stdout.split('\n')
            result = parse_results(olines )
            results.append([access, cache_size] + d2list(result))
        # print(results)
    print("")
f_p = open("results.pkl",'wb')
pickle.dump(results, f_p)
f_p.close()