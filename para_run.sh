#!/bin/bash

for i in {0..4}; do
    for ((j=i; j<=4; j++)); do
        echo $i $j
    done
done | parallel --colsep ' ' python3 procrustes_sim.py -a {1} -b {2}
