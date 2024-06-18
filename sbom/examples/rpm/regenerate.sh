#!/bin/bash
for example in *.json; do
    python from-koji.py "$@" "${example%.spdx.json}"
done
