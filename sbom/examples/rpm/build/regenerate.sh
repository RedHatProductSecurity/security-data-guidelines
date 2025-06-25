#!/usr/bin/env bash

packages=("openssl-3.0.7-18.el9_2" "openshift-pipelines-client-1.14.3-11352.el8" "poppler-21.01.0-19.el9" "go-toolset-rhel8-8060020250609110611.97d7f71f")

for example in "${packages[@]}"; do
    python3 from-koji.py "$@" "${example}"
done
