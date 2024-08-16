#!/usr/bin/env bash

for example in ../release/*.json; do
    python3 remove_release_data.py "$example"
done
