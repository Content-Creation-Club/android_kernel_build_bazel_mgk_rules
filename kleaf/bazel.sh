#!/bin/bash
set -euo pipefail

# Android names sources from the ROM root; Bazel labels are workspace-relative.
args=("$@")
for i in "${!args[@]}"; do
    case "${args[$i]}" in
        //kernel/platform/kernel-*/*:*)
            args[$i]="//${args[$i]#//kernel/platform/kernel-*/}"
            ;;
    esac
done

exec "$(dirname "$(readlink -f "$0")")/../../kernel/kleaf/bazel.sh" "${args[@]}"
