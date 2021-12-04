import argparse
import os, sys
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument('--release', dest="release", action="store_true")
parser.add_argument('--dev', dest="dev", action="store_true")
parser.add_argument('--test', dest="test", action="store_true")

args = parser.parse_args()

if args.test == True:
    retr = os.system("python3.9 setup.py pytest")
    if retr != 0:
        sys.exit()


if args.dev == True:
    with open("version.json", "r") as file:
        version = json.load(file)["version"]

    os.rename("version.json", "version.json.old")

    with open("version.json", "w") as file:
        newVersion = f"{version}-dev{int(time.time())}"
        vdict = {"version": newVersion}

        json.dump(vdict, file, indent=4)

    os.system("python3.9 setup.py bdist_wheel sdist")

    os.remove("version.json")
    os.rename("version.json.old", "version.json")

elif args.release == True:
    os.system("python3.9 setup.py bdist_wheel sdist")
