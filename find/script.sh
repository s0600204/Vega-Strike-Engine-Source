#!/bin/bash

set -e

mkdir find/temp && cd find/temp

cmake $@ ..
