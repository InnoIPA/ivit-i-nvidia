#!/bin/bash
printf "\n"
printf "# Build Plugin \n"

cd /workspace/plugins
make clean && make > /dev/null 2>&1