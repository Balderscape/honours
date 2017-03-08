#!/bin/bash

set -e

export PATH=$CONDA_DIR/bin:$PATH
jupyter notebook
