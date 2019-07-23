#!/bin/bash
#
# Copyright (c) 2019, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

######################################
# ClaraGenomicsAnalysis CPU/GPU conda build script for CI #
######################################
set -e

PYCLARAGENOMICS_DIR=$1
cd $PYCLARAGENOMICS_DIR

#Install external dependencies.
python3 -m pip install -r requirements.txt
python3 setup.py develop

# Run tests.
if [ "$GPU_TEST" == '1' ]; then
    python3 -m pytest -m gpu -s
else
    python3 -m pytest -m cpu -s
fi
