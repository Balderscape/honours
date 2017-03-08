#!/bin/bash

set -e

. /usr/share/modules/init/bash

module load conda3
module load gromacs

jupyter notebook
