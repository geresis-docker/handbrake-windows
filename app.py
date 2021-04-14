#!/bin/python3
import os
import subprocess
import sys
import zipfile

# specifies 32 / 64 bit architecture, chooses 32 bit when HANDBRAKE_32BIT is true
architecture = 64

if (os.getenv("HANDBRAKE_32BIT")).lower() == "true":
    architecture = 32

bit = {
    32: ["i686", "i686-w64-mingw32"],
    64: ["x86_64", "x86_64-w64-mingw32"]
}

# update 
subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "dist-upgrade", "-y"])

# delete existing repository, toolchains, toolchains might change with newer versions of handbrake
subprocess.run("find /app/. ! -name 'app.py' -exec rm -rf {} +", shell=True)

# pull latest repository and switch to latest tag
subprocess.run(["git", "clone", "https://github.com/HandBrake/HandBrake.git"])
os.chdir("HandBrake")

# which tag should be used, if HANDBRAKE_VERSION = latest, the latest published tag will be used
tag = os.getenv("HANDBRAKE_VERSION").lower()

if tag == "latest":
    tag = subprocess.check_output(["git", "tag"], universal_newlines=True).split('\n')[-2]

archive = "/data/" + tag + ".zip"

if os.path.isdir(archive):
    sys.exit(archive + " exists")

subprocess.run(["git", "checkout", "tags/" + tag])

# remove existing toolchain and compile it afterwards
subprocess.run(["scripts/mingw-w64-build", "x86_64.distclean"])
subprocess.run(["scripts/mingw-w64-build", bit[architecture][0]])

# get path to compiler and set $PATH
os.environ["PATH"] += ":/root/toolchains/" + os.listdir("/root/toolchains")[-1] + "/mingw-w64-x86_64/bin"
os.environ["PATH"] += ":/app/HandBrake"

subprocess.run(
    "configure --cross=" + bit[architecture][1] + " \
	--enable-qsv --enable-vce --enable-nvenc --enable-fdk-aac \
	--launch-jobs=$(nproc) --force --launch",
    shell=True
)

# copy files to /data/[tag].zip archive
files = [
    "/app/HandBrake/build/libhb/hb.dll",
    "/app/HandBrake/build/HandBrakeCLI.exe"
]

for f in files:
    if not os.path.isfile(f):
        sys.exit(f + " not found")

with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_LZMA) as z:
    for f in files:
        z.write(f, os.path.basename(f))

# chown and chmod files
uid = int(os.environ["UID"])
gid = int(os.environ["GID"])

if uid != 0 and gid != 0:
    subprocess.run(["chown", uid + ":" + gid, archive])

subprocess.run(["chmod", "644", archive])
