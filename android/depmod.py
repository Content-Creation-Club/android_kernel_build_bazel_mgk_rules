#!/usr/bin/env python3
"""Validate preloaded providers without adding first-stage paths to modules.dep."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def module_name(name):
    return Path(name).name.removesuffix(".ko").replace("-", "_")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depmod", required=True)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--preloaded", type=Path, required=True)
    parser.add_argument("args", nargs=argparse.REMAINDER)
    options = parser.parse_args()
    args = options.args[1:] if options.args[:1] == ["--"] else options.args

    if "-b" not in args or Path(args[args.index("-b") + 1]).resolve() != options.stage.resolve():
        os.execv(options.depmod, [options.depmod, *args])

    modules = options.stage / "lib/modules" / args[-1]
    installed = {module_name(path.name) for path in modules.rglob("*.ko")}
    early = {module_name(path.name): path for path in options.preloaded.glob("*.ko")}
    loaded = {module_name(name) for name in (options.preloaded / "modules.load").read_text().split()}

    # These providers are resident before vendor_dlkm is mounted. Their files
    # disappear at switch-root, so use them only for symbol validation.
    with tempfile.TemporaryDirectory(prefix="preloaded-", dir=modules) as directory:
        for name in sorted(loaded - installed):
            path = early[name]
            os.link(path, Path(directory) / path.name)
        check = subprocess.run(
            [options.depmod, *args, "-e", "-n"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        sys.stderr.write(check.stderr)
        if check.returncode or "needs unknown symbol" in check.stderr:
            return check.returncode or 1

    # Validation above covers the preloaded providers; generate installation
    # metadata from the files that remain accessible in the running system.
    args = ["-a" if arg == "-ae" else arg for arg in args if arg != "-e"]
    os.execv(options.depmod, [options.depmod, *args])


if __name__ == "__main__":
    sys.exit(main())
