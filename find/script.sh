#!/bin/bash

set -e

export PATH="/usr/local/opt/openal-soft/bin:$PATH"

mkdir find/temp && cd find/temp

cmake $@ ..
