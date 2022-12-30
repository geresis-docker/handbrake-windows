#!/bin/python3
import os
import re
import subprocess
import sys
import zipfile

# paths
path_handbrake: str = "/root/handbrake"
path_toolchains: str = "/root/toolchains"

# fetch repository
subprocess.run(f"git clone https://github.com/HandBrake/HandBrake.git {path_handbrake}", shell=True)
os.chdir(path_handbrake)
tag: str = os.getenv("VERSION")
if tag is None or tag.lower() == "latest":
    tag: str = subprocess.check_output(f"git tag", shell=True, text=True).split("\n")[-2]
path_output: str = f"/data/{tag}.zip"
if os.path.isfile(path_output):
    sys.exit("already compiled!")
subprocess.run(f"git checkout tags/{tag}", shell=True)

# compile toolchain and get export PATH="...: from output using re.search(...)
print("compiling toolchain, this will take some time ...", flush=True)
output: str = subprocess.check_output(f"scripts/mingw-w64-build x86_64 {path_toolchains}", shell=True, text=True)
path_export: str = re.search(r'(?<=export PATH=")([^:]*)', output).group()
print(output)
print(f"path_export: {path_export}")
os.environ["PATH"] += f":{path_export}"

# compile handbrake with aac-fdk support
subprocess.run(
    f"./configure --cross=x86_64-w64-mingw32 "
    f"--enable-fdk-aac "
    f"--launch-jobs=$(nproc) --launch", shell=True)

# move files
files_output: list[str] = [
    f"{path_handbrake}/build/libhb/hb.dll",
    f"{path_handbrake}/build/HandBrakeCLI.exe"]
file_not_found: bool = False
for f in files_output:
    if not os.path.isfile(f):
        print(f"file not found: {f}")
        file_not_found = True
        continue
if file_not_found:
    sys.exit("output files not found!")
with zipfile.ZipFile(path_output, "w", compression=zipfile.ZIP_LZMA) as z:
    for f in files_output:
        z.write(f, os.path.basename(f))
print(f"created archive: {path_output}")
