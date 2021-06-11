#!/bin/bash

set -e


mkdir find/temp && cd find/temp

# This one is the winner!
export OPENALDIR="/usr/local/opt/openal-soft"
cmake $@ ..
