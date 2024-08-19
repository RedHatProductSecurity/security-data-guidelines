#!/usr/bin/env bash

for example in ../build/*.json; do
    python3 add_release_data.py "$example"
done
