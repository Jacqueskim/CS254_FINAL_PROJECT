import os
import re
import subprocess

def change_cache_size(filename, new_size):
    with open(filename, 'r') as file:
        data = file.readlines()

    for i, line in enumerate(data):
        if "-size" in line:
            
            data[i] = re.sub(r'(-size \S+ )\d+', r'\g<1>{}'.format(new_size), line)

    with open(filename, 'w') as file:
        file.writelines(data)

def run_program():
     subprocess.run(["./cacti", "-infile", "cache.cfg"], check=True)

cache_sizes = [  4096,
 32768,
 131072,
 262144,
 1048576,
 2097152,
 4194304,
 8388608,
 16777216,
 33554432,
 134217728,
 67108864,
 1073741824]
cache_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),  'cache.cfg')
for size in cache_sizes:
    change_cache_size(cache_file_path, size)
    run_program()