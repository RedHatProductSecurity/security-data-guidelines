#!/usr/bin/env bash

for example in *.json; do
    python3 from-koji.py "$@" "${example%.spdx.json}"
done
