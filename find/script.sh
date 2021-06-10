#!/bin/bash

set -e

mkdir temp && cd temp

cmake $@ ..
