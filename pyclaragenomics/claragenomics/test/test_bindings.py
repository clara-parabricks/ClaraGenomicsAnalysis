#
# Copyright (c) 2019, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

from difflib import SequenceMatcher
import pytest
import random

from claragenomics.bindings.cudapoa import CudaPoaBatch
from claragenomics.bindings.cuda import CudaStream

@pytest.mark.gpu
def test_cudapoa_simple_batch():
    batch = CudaPoaBatch(10, 10)
    windows = list()
    windows.append(["ACTGACTG", "ACTTACTG", "ACGGACTG", "ATCGACTG"])
    windows.append(["ACTGAC", "ACTTAC", "ACGGAC", "ATCGAC"])
    batch.add_poas(windows)
    batch.generate_poa()
    consensus = batch.get_consensus()

    assert(len(consensus) == len(windows))
    assert(batch.total_poas == len(windows))

@pytest.mark.gpu
def test_cudapoa_reset_batch():
    batch = CudaPoaBatch(10, 10)
    windows = list()
    windows.append(["ACTGACTG", "ACTTACTG", "ACGGACTG", "ATCGACTG"])
    batch.add_poas(windows)
    batch.generate_poa()
    consensus = batch.get_consensus()

    assert(batch.total_poas == 1)

    batch.reset()

    assert(batch.total_poas == 0)

@pytest.mark.gpu
def test_cudapoa_complex_batch():
    read_len = 500
    ref = ''.join([random.choice(['A','C', 'G', 'T']) for _ in range(read_len)])
    num_reads=100
    mutation_rate=0.02
    reads = []
    for _ in range(num_reads):
        new_read = ''.join([r if random.random() > mutation_rate else random.choice(['A','C', 'G', 'T']) for r in ref])
        reads.append(new_read)
    
    stream = CudaStream()
    batch = CudaPoaBatch(10, 1000, stream)
    batch.add_poas(reads)
    batch.generate_poa()
    consensus = batch.get_consensus()[0].decode('utf-8')
    match_ratio = SequenceMatcher(None, ref, consensus).ratio()
    print("Similarity beteen original string and consensus is ", match_ratio)
    assert(match_ratio == 1.0)
