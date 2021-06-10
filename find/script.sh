#!/bin/bash

set -e

#export PATH="/usr/local/opt/openal-soft/bin:$PATH"

mkdir find/temp && cd find/temp

export OPENALDIR="/usr/local/opt/openal-soft/bin"
cmake $@ ..

export OPENALDIR="/usr/local/opt/openal-soft"
cmake $@ ..

export OPENALDIR="/usr/local/opt"
cmake $@ ..
